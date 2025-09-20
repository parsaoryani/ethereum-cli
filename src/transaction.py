import json
import logging
import time
from pathlib import Path
from typing import Dict, Any
import rlp
import requests
from eth_account import Account
from eth_utils import to_bytes, to_hex, to_checksum_address

from src.rpc_client import RPCClient
from src.wallet import WalletManager

# Configuration path
CONFIG_PATH = Path(__file__).parent.parent / 'config' / 'settings.json'
EXPORT_PATH = Path('/Users/parsaoryani/PycharmProjects/ethereum-cli/exports')

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
        try:
            with open(CONFIG_PATH, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            logger.error("Configuration file not found at: %s", CONFIG_PATH)
            raise ValueError(f"Configuration file not found at: {CONFIG_PATH}")
        except json.JSONDecodeError:
            logger.error("Invalid JSON format in configuration file: %s", CONFIG_PATH)
            raise ValueError(f"Invalid JSON format in configuration file: {CONFIG_PATH}")

        required_keys = ['network', 'transaction']
        for key in required_keys:
            if key not in self.config:
                logger.error("Missing required configuration key: %s", key)
                raise ValueError(f"Missing required configuration key: {key}")

        self.rpc_client = RPCClient(
            rpc_url=self.config['network'].get('rpc_url', ''),
            chain_id=self.config['network'].get('chain_id', 0),
            timeout=10,
            max_retries=3
        )
        self.wallet_manager = WalletManager()

        self.default_gas_limit = self.config['transaction'].get('default_gas_limit', 21000)
        self.max_gas_price_gwei = self.config['transaction'].get('max_gas_price_gwei', 100)
        self.default_gas_price_gwei = self.config['transaction'].get('default_gas_price_gwei', 1.0)
        self.etherscan_api_key = self.config['transaction'].get('etherscan_api_key', '')

        if not self.etherscan_api_key:
            logger.warning("Etherscan API key not configured in settings.json")

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

    def get_transaction_history(self, address: str) -> list:
        """
        Retrieve transaction history for an address using Etherscan API.
        Supports CLI command: ./cli tx history [--address [address]]
        """
        if not self.wallet_manager._is_valid_address(address):
            raise ValueError(f"Invalid address: {address}")
        if not self.etherscan_api_key:
            raise ValueError("Etherscan API key not configured in settings.json")

        address = to_checksum_address(address)
        url = (
            f"https://api-sepolia.etherscan.io/api?module=account&action=txlist"
            f"&address={address}&sort=desc&apikey={self.etherscan_api_key}"
        )
        logger.info(f"Fetching transaction history for {address} from Etherscan")
        for attempt in range(3):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                if data.get('status') != '1':
                    error_message = data.get('message', 'Unknown Etherscan API error')
                    error_result = data.get('result', 'No details provided')
                    logger.error(f"Etherscan API error: {error_message}, details: {error_result}")
                    raise ValueError(f"Etherscan API error: {error_message}, details: {error_result}")
                transactions = [{
                    'hash': tx['hash'],
                    'from': to_checksum_address(tx['from']),
                    'to': to_checksum_address(tx['to']) if tx.get('to') else '',
                    'value': int(tx['value']) / 1e18,  # Convert wei to ETH
                    'gas': int(tx['gasUsed']),
                    'gasPrice': int(tx['gasPrice']),
                    'blockNumber': int(tx['blockNumber'])
                } for tx in data['result']]
                logger.info(f"Retrieved {len(transactions)} transactions for {address}")
                return transactions
            except requests.RequestException as e:
                logger.warning(f"Etherscan fetch attempt {attempt + 1} failed: {e}")
                if attempt == 2:
                    raise ValueError(f"Failed to fetch transaction history after retries: {str(e)}")
                time.sleep(1)  # Delay to avoid rate limiting
        raise ValueError("Failed to fetch transaction history after retries")

    def export_transaction_history(self, address: str, output_file: str = None) -> None:
        """
        Export transaction history to a JSON file in the specified exports directory.
        Supports CLI command: ./cli tx export --output [filename]
        """
        transactions = self.get_transaction_history(address)
        # Use full wallet address in filename if output_file not provided
        output_file = output_file or f"tx_history_{address.lower().replace('0x', '')}.json"
        output_path = EXPORT_PATH / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with output_path.open('w') as f:
                json.dump(transactions, f, indent=2)
            logger.info(f"Transaction history exported to {output_path}")
        except Exception as e:
            logger.error(f"Failed to export transactions: {e}")
            raise ValueError(f"Failed to export transactions: {e}")

    def close(self):
        """
        Clean up resources by closing the RPC client.
        """
        self.rpc_client.close()
        logger.info("TransactionManager closed")

# CLI Interface for transaction commands
def transaction_send(to_address: str, amount: float, password: str, from_address: str = None) -> None:
    """
    CLI command: Send ETH to an address.
    Supports: ./cli send --to [address] --amount [eth_amount] [--from [address]] --password [password]
    """
    try:
        manager = TransactionManager()
        # Use default wallet if from_address not specified
        if not from_address:
            from_address = manager.wallet_manager.get_default_wallet()
            if not from_address:
                print("No default wallet set. Use 'wallet use' to set a default wallet.")
                exit(1)

        # Validate amount
        if amount <= 0:
            print("Error: Amount must be positive")
            exit(1)

        tx_hash = manager.send_transaction(from_address, to_address, amount, password)
        print(f"Transaction sent successfully! Hash: {tx_hash}")
        print(f"Check transaction on Sepolia Etherscan: https://sepolia.etherscan.io/tx/{tx_hash}")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    finally:
        manager.close()

def transaction_status(tx_hash: str) -> None:
    """
    CLI command: Check transaction status.
    Supports: ./cli tx status --hash [tx_hash]
    """
    try:
        manager = TransactionManager()
        status = manager.check_transaction_status(tx_hash)
        print(f"Transaction Hash: {tx_hash}")
        print(f"Status: {status['status']}")
        print(f"Message: {status['message']}")
        if status['status'] == 'success':
            print(f"Gas Used: {status.get('gas_used', 0):,}")
            print(f"Block Number: {status.get('block_number', 'N/A')}")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    finally:
        manager.close()

def transaction_history(address: str = None) -> None:
    """
    CLI command: Show transaction history for an address.
    Supports: ./cli tx history [--address [address]]
    """
    try:
        manager = TransactionManager()
        # Use default wallet if address not specified
        if not address:
            address = manager.wallet_manager.get_default_wallet()
            if not address:
                print("No default wallet set. Use 'wallet use' to set a default wallet.")
                exit(1)

        history = manager.get_transaction_history(address)
        print(f"Retrieved {len(history)} transactions for {address}:")
        print("-" * 50)
        for tx in history:
            print(f"Hash: {tx['hash']}")
            print(f"From: {tx['from']}")
            print(f"To: {tx['to']}")
            print(f"Value: {tx['value']:.6f} ETH")
            print(f"Gas Used: {tx['gas']:,}")
            print(f"Gas Price: {tx['gasPrice']:,} wei")
            print(f"Block Number: {tx['blockNumber']}")
            print("-" * 50)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    finally:
        manager.close()

def transaction_export(address: str = None, output: str = None) -> None:
    """
    CLI command: Export transaction history to JSON.
    Supports: ./cli tx export [--address [address]] [--output [filename]]
    """
    try:
        manager = TransactionManager()
        # Use default wallet if address not specified
        if not address:
            address = manager.wallet_manager.get_default_wallet()
            if not address:
                print("No default wallet set. Use 'wallet use' to set a default wallet.")
                exit(1)

        manager.export_transaction_history(address, output)
        filename = output or f"tx_history_{address.lower().replace('0x', '')}.json"
        print(f"Transaction history exported to: {EXPORT_PATH / filename}")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    finally:
        manager.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Ethereum CLI for Sepolia Testnet Transactions")
    subparsers = parser.add_subparsers(dest="command", help="Transaction commands")

    # Send transaction
    send_parser = subparsers.add_parser("send", help="Send ETH to an address")
    send_parser.add_argument("--to", required=True, help="Recipient address")
    send_parser.add_argument("--amount", type=float, required=True, help="Amount in ETH")
    send_parser.add_argument("--from", dest="from_address", help="Sender address (optional, uses default wallet if not specified)")
    send_parser.add_argument("--password", required=True, help="Wallet password")
    send_parser.set_defaults(func=transaction_send)

    # Transaction status
    status_parser = subparsers.add_parser("tx_status", help="Check transaction status")
    status_parser.add_argument("--hash", required=True, help="Transaction hash")
    status_parser.set_defaults(func=transaction_status)

    # Transaction history
    history_parser = subparsers.add_parser("tx_history", help="Fetch transaction history")
    history_parser.add_argument("--address", help="Wallet address (optional, uses default wallet if not specified)")
    history_parser.set_defaults(func=transaction_history)

    # Export transaction history
    export_parser = subparsers.add_parser("tx_export", help="Export transaction history to JSON")
    export_parser.add_argument("--address", help="Wallet address (optional, uses default wallet if not specified)")
    export_parser.add_argument("--output", help="Output filename (optional)")
    export_parser.set_defaults(func=transaction_export)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        exit(1)

    # Call the appropriate function with filtered arguments
    if args.command == "send":
        args.func(args.to, args.amount, args.password, args.from_address)
    elif args.command == "tx_status":
        args.func(args.hash)
    elif args.command == "tx_history":
        args.func(args.address)
    elif args.command == "tx_export":
        args.func(args.address, args.output)