import json
import logging
import time
from pathlib import Path
from typing import Dict, Any
import rlp
from ecdsa import SigningKey, SECP256k1
from _pysha3 import keccak_256
from eth_account import Account

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
        """
        with open(CONFIG_PATH, 'r') as f:
            self.config = json.load(f)

        self.rpc_client = RPCClient(
            rpc_url=self.config['network']['rpc_url'],
            chain_id=self.config['network']['chain_id']
        )
        self.wallet_manager = WalletManager()

        self.default_gas_limit = self.config.get('transaction', {}).get('default_gas_limit', 21000)
        self.max_gas_price_gwei = self.config.get('transaction', {}).get('max_gas_price_gwei', 100)
        self.history_block_limit = self.config.get('transaction', {}).get('history_block_limit', 1000)

        logger.info("✅ TransactionManager initialized")

    def _build_transaction(self, from_address: str, to_address: str, value_ether: float) -> Dict[str, Any]:
        """
        Build a raw Ethereum transaction with gas estimation.
        """
        if not self.wallet_manager._is_valid_address(to_address):
            raise ValueError(f"Invalid recipient address: {to_address}")
        if not self.wallet_manager._is_valid_address(from_address):
            raise ValueError(f"Invalid sender address: {from_address}")
        if value_ether <= 0:
            raise ValueError("Amount must be positive")

        value_wei = int(value_ether * 1_000_000_000_000_000_000)
        balance_wei = self.rpc_client.get_balance(from_address, 'wei')
        if balance_wei < value_wei:
            raise ValueError(f"Insufficient balance: {balance_wei / 1e18:.6f} ETH available")

        nonce = self.rpc_client.get_nonce(from_address)
        chain_id = self.rpc_client.get_chain_id()
        gas_price = int(min(self.rpc_client.get_gas_price('gwei'), self.max_gas_price_gwei) * 1_000_000_000)

        try:
            gas_limit = self.rpc_client.estimate_gas({
                'to': to_address,
                'value': hex(value_wei),
                'from': from_address
            })
        except Exception as e:
            logger.warning(f"Gas estimation failed: {e}, using default gas limit")
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

        logger.info(f"Built transaction: nonce={nonce}, to={to_address}, value={value_ether} ETH, gas={gas_limit}")
        return transaction

    def _sign_transaction(self, transaction: Dict[str, Any], private_key_hex: str) -> bytes:
        """
        Sign a transaction using ECDSA and serialize to RLP.
        """
        try:
            private_key = bytes.fromhex(private_key_hex)
            signing_key = SigningKey.from_string(private_key, curve=SECP256k1)
            logger.info("Signing key created successfully")
        except ValueError as e:
            logger.error(f"Invalid private key format: {e}")
            raise ValueError("Invalid private key format")

        chain_id = transaction['chainId']  # Use transaction['chainId'] (11155111 for Sepolia)
        logger.info(f"Using chainId for signing: {chain_id}")

        tx_fields = [
            transaction['nonce'],
            transaction['gasPrice'],
            transaction['gas'],
            bytes.fromhex(transaction['to'][2:]),
            transaction['value'],
            transaction['data'],
            chain_id, 0, 0  # EIP-155: chainId, v=0, r=0, s=0 for unsigned
        ]

        encoded_tx = rlp.encode(tx_fields)
        logger.info(f"Unsigned transaction encoded: {encoded_tx.hex()}")

        tx_hash = keccak_256(encoded_tx).digest()
        logger.info(f"Transaction hash: {tx_hash.hex()}")

        # Sign with deterministic signature (64 bytes: r + s)
        signature = signing_key.sign_digest_deterministic(tx_hash)
        if len(signature) != 64:
            raise ValueError(f"Invalid signature length: expected 64 bytes, got {len(signature)}")

        r = int.from_bytes(signature[:32], 'big')
        s = int.from_bytes(signature[32:], 'big')

        # Ensure canonical signature (low s)
        rec_id = 0
        if s > (SECP256k1.order // 2):
            s = SECP256k1.order - s
            rec_id = 1

        # Calculate v with EIP-155
        v = rec_id + 35 + (chain_id * 2)  # Use 35 instead of 27 for EIP-155
        logger.info(f"Signature components: v={v}, r={r}, s={s}")

        # Verify chainId in v
        derived_chain_id = (v - 35 - rec_id) // 2
        if derived_chain_id != chain_id:
            logger.error(f"Chain ID mismatch: derived={derived_chain_id}, expected={chain_id}")
            raise ValueError(f"Chain ID mismatch in signature: derived {derived_chain_id}, expected {chain_id}")

        signed_tx_fields = tx_fields[:-3] + [v, r, s]
        signed_tx = rlp.encode(signed_tx_fields)
        logger.info(f"Signed transaction: {signed_tx.hex()}")

        # Verify signature by recovering address
        expected_address = Account.from_key(private_key).address
        recovered_address = Account.recover_transaction('0x' + signed_tx.hex())
        if recovered_address.lower() != expected_address.lower():
            logger.error(f"Signature verification failed: recovered={recovered_address}, expected={expected_address}")
            raise ValueError(f"Signature verification failed: recovered {recovered_address}, expected {expected_address}")

        return signed_tx

    def send_transaction(self, from_address: str, to_address: str, value_ether: float, password: str) -> str:
        """
        Send an ETH transaction to the network.
        """
        logger.info(f"Attempting to get wallet info for {from_address}")
        wallet_info = self.wallet_manager.get_wallet_info(from_address, password)
        logger.info(f"Wallet info retrieved: private_key_available={wallet_info.get('private_key_available')}")
        if not wallet_info.get('private_key_available', False):
            raise ValueError(wallet_info.get('decryption_error', 'Failed to access private key'))

        logger.info("Building transaction...")
        transaction = self._build_transaction(from_address, to_address, value_ether)
        logger.info(f"Transaction built: {transaction}")

        logger.info("Signing transaction...")
        signed_tx = self._sign_transaction(transaction, wallet_info['private_key'])
        signed_tx_hex = '0x' + signed_tx.hex()
        logger.info(f"Signed transaction hex: {signed_tx_hex[:50]}...")

        logger.info("Sending transaction to network...")
        for attempt in range(3):
            try:
                tx_hash = self.rpc_client.send_raw_transaction(signed_tx_hex)
                logger.info(f"Transaction sent: {tx_hash}")
                return tx_hash
            except ValueError as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == 2:
                    raise
                time.sleep(2)
        raise ValueError("Failed to send transaction after retries")

    def close(self):
        """
        Clean up resources by closing RPC client.
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
        test_address = "0x7e4dd6856aa001b78f1f2fe1a4a1f0e5b2cce5f7"
        balance = tx_manager.rpc_client.get_balance(test_address, "ether")
        print(f"Test address balance: {balance:.6f} SepoliaETH")

        to_address = "0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b"
        value_ether = 0.01
        password = "Parsa1382@"  # Replace with actual password

        print(f"\n1️⃣ Attempting to send {value_ether} SepoliaETH from {test_address} to {to_address}")
        try:
            tx = tx_manager._build_transaction(test_address, to_address, value_ether)
            print(f"✅ Transaction built: {tx}")

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
                    status = tx_manager.rpc_client.get_transaction_status(tx_hash)
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