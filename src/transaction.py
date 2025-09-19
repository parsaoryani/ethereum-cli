import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import rlp
from ecdsa import SigningKey, SECP256k1
from _pysha3 import keccak_256

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
    """
    Manages Ethereum transaction operations including construction, signing,
    broadcasting, and history retrieval for Sepolia testnet.
    """

    def __init__(self):
        """
        Initialize TransactionManager with configuration and dependencies.
        """
        # Load configuration
        with open(CONFIG_PATH, 'r') as f:
            self.config = json.load(f)

        # Initialize dependencies
        self.rpc_client = RPCClient(
            rpc_url=self.config['network']['rpc_url'],
            chain_id=self.config['network']['chain_id']
        )
        self.wallet_manager = WalletManager()

        # Gas settings from config
        self.default_gas_limit = self.config.get('transaction', {}).get('default_gas_limit', 21000)
        self.max_gas_price_gwei = self.config.get('transaction', {}).get('max_gas_price_gwei', 100)
        self.history_block_limit = self.config.get('transaction', {}).get('history_block_limit', 1000)

        logger.info("✅ TransactionManager initialized")

    def _build_transaction(self, from_address: str, to_address: str, value_ether: float) -> Dict[str, Any]:
        """
        Build a raw Ethereum transaction.

        Args:
            from_address: Sender's Ethereum address
            to_address: Recipient's Ethereum address
            value_ether: Amount to send in ETH

        Returns:
            Transaction dictionary

        Raises:
            ValueError: Invalid inputs or insufficient balance
        """
        if not self.wallet_manager._is_valid_address(to_address):
            raise ValueError(f"Invalid recipient address: {to_address}")
        if not self.wallet_manager._is_valid_address(from_address):
            raise ValueError(f"Invalid sender address: {from_address}")
        if value_ether <= 0:
            raise ValueError("Amount must be positive")

        # Convert ETH to Wei
        value_wei = int(value_ether * 1_000_000_000_000_000_000)

        # Check balance
        balance_wei = self.rpc_client.get_balance(from_address, 'wei')
        if balance_wei < value_wei:
            raise ValueError(f"Insufficient balance: {balance_wei / 1e18:.6f} ETH available")

        # Build transaction
        nonce = self.rpc_client.get_nonce(from_address)
        chain_id = self.rpc_client.get_chain_id()
        gas_price = int(self.rpc_client.get_gas_price('wei'))
        gas_limit = self.default_gas_limit  # Will be refined in next stage

        transaction = {
            'nonce': nonce,
            'to': to_address,
            'value': value_wei,
            'gas': gas_limit,
            'gasPrice': gas_price,
            'chainId': chain_id,
            'data': b''  # Empty for simple ETH transfer
        }

        logger.info(f"Built transaction: nonce={nonce}, to={to_address}, value={value_ether} ETH")
        return transaction

    def _sign_transaction(self, transaction: Dict[str, Any], private_key_hex: str) -> bytes:
        """
        Sign a transaction using ECDSA and serialize to RLP.

        Args:
            transaction: Transaction dictionary
            private_key_hex: Private key in hex format

        Returns:
            RLP-encoded signed transaction bytes
        """
        try:
            private_key = bytes.fromhex(private_key_hex)
            signing_key = SigningKey.from_string(private_key, curve=SECP256k1)
        except ValueError:
            raise ValueError("Invalid private key format")

        # Prepare transaction for RLP encoding
        tx_fields = [
            transaction['nonce'],
            transaction['gasPrice'],
            transaction['gas'],
            bytes.fromhex(transaction['to'][2:]),  # Remove 0x
            transaction['value'],
            transaction['data'],
            transaction['chainId'], 0, 0  # EIP-155: chainId, v, r, s (v=chainId for unsigned)
        ]

        # Encode unsigned transaction
        encoded_tx = rlp.encode(tx_fields)

        # Sign the hash of the encoded transaction
        tx_hash = keccak_256(encoded_tx).digest()
        signature = signing_key.sign_digest_deterministic(tx_hash, sigencode=lambda v, r, s: (v, r, s))

        # Extract v, r, s
        v = signature[64] + 27 + (transaction['chainId'] * 2)  # EIP-155
        r = int.from_bytes(signature[0:32], 'big')
        s = int.from_bytes(signature[32:64], 'big')

        # Encode signed transaction
        signed_tx_fields = tx_fields[:-3] + [v, r, s]
        signed_tx = rlp.encode(signed_tx_fields)

        logger.info("Transaction signed successfully")
        return signed_tx

    def close(self):
        """
        Clean up resources by closing RPC client.
        """
        self.rpc_client.close()
        logger.info("TransactionManager closed")

if __name__ == '__main__':
    print("🚀 Testing TransactionManager Setup and Transaction Building")
    try:
        tx_manager = TransactionManager()
        print("✅ TransactionManager initialized successfully")
        network_info = tx_manager.rpc_client.get_network_info()
        print(f"Network: {network_info['network']}, Chain ID: {network_info['chain_id']}")
        balance = tx_manager.rpc_client.get_balance("0x7e4dd6856aa001b78f1f2fe1a4a1f0e5b2cce5f7", "ether")
        print(f"Test address balance: {balance:.6f} SepoliaETH")

        # Test transaction building
        test_address = "0x7e4dd6856aa001b78f1f2fe1a4a1f0e5b2cce5f7"
        try:
            tx = tx_manager._build_transaction(
                from_address=test_address,
                to_address="0x742d35Cc6634C0532925a3b8D7C4aE7B6733E6B5",
                value_ether=0.01
            )
            print(f"✅ Transaction built: {tx}")
        except ValueError as e:
            print(f"❌ Transaction build failed: {e}")

        # Note: Signing test requires a valid private key and wallet file
        tx_manager.close()
    except Exception as e:
        print(f"❌ Setup failed: {e}")