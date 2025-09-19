import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
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

        logger.info("✅ TransactionManager initialized")

    def close(self):
        """
        Clean up resources by closing RPC client.
        """
        self.rpc_client.close()
        logger.info("TransactionManager closed")

if __name__ == '__main__':
    print("🚀 Testing TransactionManager Setup")
    try:
        tx_manager = TransactionManager()
        print("✅ TransactionManager initialized successfully")
        network_info = tx_manager.rpc_client.get_network_info()
        print(f"Network: {network_info['network']}, Chain ID: {network_info['chain_id']}, latest_block : {network_info['latest_block']},"
              f"gas_price_gwei : {network_info['gas_price_gwei']}")
        tx_manager.close()
    except Exception as e:
        print(f"❌ Setup failed: {e}")