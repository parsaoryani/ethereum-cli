import json
import logging
import time
from pathlib import Path
from typing import Dict, Any
import rlp
from eth_account import Account
from eth_utils import to_bytes, to_hex, to_checksum_address

from rpc_client import RPCClient
from wallet import WalletManager

# Configuration path
CONFIG_PATH = Path(__file__).parent.parent / 'config' / 'settings.json'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TransactionManager:
    def __init__(self):
        """
        Initialize TransactionManager with configuration and dependencies.
        Loads network settings from config file and initializes RPC client and wallet manager.
        """
        with open(CONFIG_PATH, 'r') as f:
            self.config = json.load(f)

        self.rpc_client = RPCClient(
            rpc_url=self.config['network']['rpc_url'],
            chain_id=self.config['network']['chain_id'],
            timeout=10,
            max_retries=3
        )
        self.wallet_manager = WalletManager()

        self.default_gas_limit = self.config.get('transaction', {}).get('default_gas_limit', 21000)
        self.max_gas_price_gwei = self.config.get('transaction', {}).get('max_gas_price_gwei', 100)
        self.default_gas_price_gwei = self.config.get('transaction', {}).get('default_gas_price_gwei', 1.0)

        logger.info("✅ TransactionManager initialized")

    def _build_transaction(self, from_address: str, to_address: str, value_ether: float) -> Dict[str, Any]:
        """
        Build a raw Ethereum transaction with custom gas estimation.
        Validates addresses and amount, fetches nonce, and estimates gas.
        """
        if not self.wallet_manager._is_valid_address(to_address):
            raise ValueError(f"Invalid recipient address: {to_address}")
        if not self.wallet_manager._is_valid_address(from_address):
            raise ValueError(f"Invalid sender address: {from_address}")
        if value_ether <= 0:
            raise ValueError("Amount must be positive")

        to_address = to_checksum_address(to_address)
        from_address = to_checksum_address(from_address)
        value_wei = int(value_ether * 1_000_000_000_000_000_000)
        balance_wei = self.rpc_client.get_balance(from_address, 'wei')
        if balance_wei < value_wei:
            raise ValueError(f"Insufficient balance: {balance_wei / 1e18:.6f} ETH available")

        # Fetch nonce with retry logic
        nonce = None
        for attempt in range(3):
            try:
                nonce = self.rpc_client.get_nonce(from_address)
                break
            except Exception as e:
                logger.warning(f"Nonce fetch attempt {attempt + 1} failed: {e}")
                if attempt == 2:
                    raise ValueError("Failed to fetch nonce after retries")
                time.sleep(1)

        chain_id = self.rpc_client.get_chain_id()
        gas_price = int(max(
            min(self.rpc_client.get_gas_price('gwei'), self.max_gas_price_gwei),
            self.default_gas_price_gwei
        ) * 1_000_000_000)

        try:
            gas_limit = self.rpc_client.estimate_gas({
                'to': to_address,
                'value': to_hex(value_wei),
                'from': from_address
            })
        except Exception as e:
            logger.warning(f"Gas estimation failed: {e}, using default gas limit {self.default_gas_limit}")
            gas_limit = self.default_gas_limit

        gas_cost_wei = gas_limit * gas_price
        if balance_wei < (value_wei + gas_cost_wei):
            raise ValueError(f"Insufficient funds for gas: {balance_wei / 1e18:.6f} ETH available")

        transaction = {
            'nonce': nonce,
            'to': to_address,
            'value': value_wei,
            'gas': gas_limit,
            'gasPrice': gas_price,
            'chainId': chain_id,
            'data': b''
        }

        logger.info(
            f"Built transaction: nonce={nonce}, to={to_address}, value={value_ether} ETH, "
            f"gas={gas_limit}, gasPrice={gas_price} wei")
        return transaction

    def _sign_transaction(self, transaction: Dict[str, Any], private_key_hex: str) -> bytes:
        """
        Sign a transaction with manual RLP encoding for compliance with task requirements.
        Validates private key and transaction fields, then signs and serializes the transaction.
        """
        try:
            private_key = to_bytes(hexstr=private_key_hex)
            account = Account.from_key(private_key)
            expected_address = account.address
            logger.info(f"Expected address from private key: {expected_address}")
        except ValueError as e:
            logger.error(f"Invalid private key format: {e}")
            raise ValueError("Invalid private key format")

        # Validate transaction fields
        required_fields = ['nonce', 'gasPrice', 'gas', 'to', 'value', 'chainId']
        for field in required_fields:
            if field not in transaction:
                raise ValueError(f"Missing transaction field: {field}")

        # Prepare transaction for signing
        tx = {
            'nonce': transaction['nonce'],
            'gasPrice': transaction['gasPrice'],
            'gas': transaction['gas'],
            'to': to_bytes(hexstr=transaction['to']) if transaction['to'] else b'',
            'value': transaction['value'],
            'data': transaction['data'],
            'chainId': transaction['chainId']
        }

        # Sign transaction using eth_account
        signed_tx = Account.sign_transaction(tx, private_key)
        signed_tx_raw = rlp.encode([
            tx['nonce'],
            tx['gasPrice'],
            tx['gas'],
            tx['to'],
            tx['value'],
            tx['data'],
            signed_tx.v,
            signed_tx.r,
            signed_tx.s
        ])

        logger.info(f"Signed transaction: {to_hex(signed_tx_raw)[:50]}...")

        # Verify signature
        recovered_address = Account.recover_transaction(to_hex(signed_tx_raw))
        if recovered_address.lower() != expected_address.lower():
            logger.error(f"Signature verification failed: recovered={recovered_address}, expected={expected_address}")
            raise ValueError(f"Signature verification failed: recovered {recovered_address}, expected {expected_address}")

        return signed_tx_raw

    def send_transaction(self, from_address: str, to_address: str, value_ether: float, password: str) -> str:
        """
        Send an ETH transaction to the Sepolia testnet.
        Builds, signs, and broadcasts the transaction, returning the transaction hash.
        Supports CLI command: ./cli send --to [address] --amount [eth_amount]
        """
        logger.info(f"Attempting to get wallet info for {from_address}")
        wallet_info = self.wallet_manager.get_wallet_info(from_address, password)
        logger.info(f"Wallet info retrieved: private_key_available={wallet_info.get('private_key_available')}")
        if not wallet_info.get('private_key_available', False):
            raise ValueError(wallet_info.get('decryption_error', 'Failed to access private key'))

        logger.info("Building transaction...")
        transaction = self._build_transaction(from_address, to_address, value_ether)

        # Convert bytes and numeric fields to hex for JSON serialization
        log_transaction = transaction.copy()
        log_transaction['data'] = to_hex(log_transaction['data'])
        log_transaction['value'] = to_hex(log_transaction['value'])
        log_transaction['gas'] = to_hex(log_transaction['gas'])
        log_transaction['gasPrice'] = to_hex(log_transaction['gasPrice'])
        log_transaction['nonce'] = to_hex(log_transaction['nonce'])
        log_transaction['chainId'] = to_hex(log_transaction['chainId'])
        logger.info(f"Transaction built:\n{json.dumps(log_transaction, indent=2)}")

        logger.info("Signing transaction...")
        signed_tx = self._sign_transaction(transaction, wallet_info['private_key'])
        signed_tx_hex = to_hex(signed_tx)
        logger.info(f"Signed transaction hex: {signed_tx_hex[:50]}...")

        logger.info("Sending transaction to network...")
        for attempt in range(3):
            try:
                tx_hash = self.rpc_client.send_raw_transaction(signed_tx_hex)
                logger.info(f"Transaction sent: {from_address} -> {to_address}, amount={value_ether} ETH, tx_hash={tx_hash}")
                return tx_hash
            except ValueError as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == 2:
                    raise
                time.sleep(5)  # Increased delay for rate limiting
        raise ValueError("Failed to send transaction after retries")

    def check_transaction_status(self, tx_hash: str) -> Dict[str, Any]:
        """
        Check the status of a transaction by its hash.
        Supports CLI command: ./cli tx status --hash [tx_hash]
        """
        try:
            status = self.rpc_client.get_transaction_status(tx_hash)
            logger.info(f"Transaction status for {tx_hash}: {status['status']}")
            return status
        except ValueError as e:
            logger.error(f"Failed to check transaction status: {e}")
            raise ValueError(f"Failed to check transaction status: {e}")

    def close(self):
        """
        Clean up resources by closing the RPC client.
        """
        self.rpc_client.close()
        logger.info("TransactionManager closed")

if __name__ == '__main__':
    print("🚀 Testing TransactionManager Transaction Sending")
    print("=" * 50)
    try:
        tx_manager = TransactionManager()
        print("✅ TransactionManager initialized successfully")
        network_info = tx_manager.rpc_client.get_network_info()
        print(f"Network: {network_info['network']}, Chain ID: {network_info['chain_id']}")
        test_address = "0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b"
        balance = tx_manager.rpc_client.get_balance(test_address, "ether")
        print(f"Test address balance: {balance:.6f} SepoliaETH")

        to_address = "0x7e4dd6856aa001b78f1f2fe1a4a1f0e5b2cce5f7"
        value_ether = 0.01
        password = "Parsa1382@"  # Replace with actual password

        print(f"\n1️⃣ Attempting to send {value_ether} SepoliaETH from {test_address} to {to_address}")
        try:
            tx = tx_manager._build_transaction(test_address, to_address, value_ether)
            # Convert bytes and numeric fields to hex for JSON serialization
            log_tx = tx.copy()
            log_tx['data'] = to_hex(log_tx['data'])
            log_tx['value'] = to_hex(log_tx['value'])
            log_tx['gas'] = to_hex(log_tx['gas'])
            log_tx['gasPrice'] = to_hex(log_tx['gasPrice'])
            log_tx['nonce'] = to_hex(log_tx['nonce'])
            log_tx['chainId'] = to_hex(log_tx['chainId'])
            print(f"✅ Transaction built:\n{json.dumps(log_tx, indent=2)}")

            tx_hash = tx_manager.send_transaction(
                from_address=test_address,
                to_address=to_address,
                value_ether=value_ether,
                password=password
            )
            print(f"✅ Transaction sent successfully! Hash: {tx_hash}")
            print(f"Check transaction on Sepolia Etherscan: https://sepolia.etherscan.io/tx/{tx_hash}")

            print("\n2️⃣ Monitoring transaction status...")
            max_attempts = 10
            attempt = 1
            while attempt <= max_attempts:
                try:
                    status = tx_manager.check_transaction_status(tx_hash)
                    print(f"Attempt {attempt}:")
                    print(f"  Status: {status['status']}")
                    print(f"  Message: {status['message']}")
                    if status['status'] == 'success':
                        print(f"  Gas Used: {status.get('gas_used', 0):,}")
                        print(f"  Block Number: {status.get('block_number', 'N/A')}")
                        break
                    elif status['status'] == 'failed':
                        print("  Transaction failed!")
                        break
                except ValueError as e:
                    print(f"  Error checking status: {e}")
                print("  Waiting 5 seconds before next check...")
                time.sleep(5)
                attempt += 1

            if attempt > max_attempts:
                print("❌ Max attempts reached. Transaction may still be pending.")

            print("\n3️⃣ Checking final balance")
            new_balance = tx_manager.rpc_client.get_balance(test_address, "ether")
            print(f"New balance for {test_address}: {new_balance:.6f} SepoliaETH")

        except (ValueError, Exception) as e:
            print(f"❌ Transaction send failed: {e}")
            logger.error(f"Error in send_transaction: {e}", exc_info=True)

    except Exception as e:
        print(f"❌ Setup failed: {e}")
        logger.error(f"Exception in setup: {e}", exc_info=True)
    finally:
        tx_manager.close()
        print("\nAll Tests Completed!")
        print("=" * 50)