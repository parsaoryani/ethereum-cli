import json
import requests
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

# Load configuration from settings.json
CONFIG_PATH = Path(__file__).parent.parent / 'config' / 'settings.json'
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

RPC_URL = config['network']['rpc_url']
CHAIN_ID = config['network']['chain_id']

# Setup simple logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Simple network names
NETWORK_NAMES = {
    11155111: 'Sepolia Testnet'
}


class RPCClient:
    """
    Simple Ethereum RPC Client for learning.
    Features:
    - Basic RPC calls with error handling
    - Balance with unit conversion
    - Gas estimation
    - Transaction monitoring
    - Basic retry logic
    """

    def __init__(self, rpc_url=RPC_URL, chain_id=CHAIN_ID, timeout=10, max_retries=2):
        """
        Initialize RPC Client with basic settings.

        Args:
            rpc_url: Ethereum RPC endpoint
            chain_id: Expected network chain ID
            timeout: Request timeout in seconds
            max_retries: Number of retry attempts
        """
        self.rpc_url = rpc_url
        self.expected_chain_id = chain_id
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers = {'Content-Type': 'application/json'}

        # Simple metrics tracking
        self.call_count = 0
        self.success_count = 0

        # Test connection
        try:
            self.get_chain_id()
            logger.info(f"✅ Connected to {self.rpc_url} (Chain ID: {chain_id})")
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            raise

    def _make_rpc_call(self, method: str, params: List[Any] = None) -> Any:
        """
        Make a JSON-RPC call with basic retry logic.

        Args:
            method: RPC method name (like 'eth_getBalance')
            params: List of parameters for the method

        Returns:
            RPC result (string, int, dict, etc.)

        Raises:
            ValueError: RPC error
            ConnectionError: Network issues
        """
        if params is None:
            params = []

        self.call_count += 1
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }

        logger.info(f"🔄 Calling {method} with params: {params}")

        # Simple retry logic
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.rpc_url,
                    headers=self.headers,
                    data=json.dumps(payload),
                    timeout=self.timeout
                )
                response.raise_for_status()  # Raises HTTPError for bad status

                result = response.json()

                # Check for RPC errors
                if 'error' in result:
                    error_msg = result['error'].get('message', 'Unknown error')
                    logger.error(f"❌ RPC Error {method}: {error_msg}")
                    raise ValueError(f"RPC error: {error_msg}")

                # Success!
                self.success_count += 1
                logger.info(f"✅ {method} succeeded")
                return result['result']

            except requests.exceptions.Timeout:
                logger.warning(f"⏰ Timeout on attempt {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)  # Wait 1 second before retry
                    continue
                raise ConnectionError("Request timed out after all retries")

            except requests.exceptions.RequestException as e:
                logger.warning(f"🌐 Network error on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise ConnectionError(f"Network error: {e}")

            except json.JSONDecodeError:
                raise ValueError("Invalid JSON response from RPC")

        # If we get here, all retries failed
        raise ConnectionError(f"Failed after {self.max_retries} attempts")

    #  Network Information
    def get_chain_id(self) -> int:
        """Get and validate the chain ID."""
        chain_id_hex = self._make_rpc_call('eth_chainId')
        chain_id = int(chain_id_hex, 16)  # Convert hex to int

        if chain_id != self.expected_chain_id:
            raise ValueError(
                f"Wrong network! Expected {self.expected_chain_id} ({NETWORK_NAMES.get(self.expected_chain_id)}), "
                f"got {chain_id}"
            )
        return chain_id

    def get_network_info(self) -> Dict[str, Any]:
        """Get basic network information."""
        try:
            chain_id = self.get_chain_id()
            block_number = self.get_block_number()
            gas_price = self.get_gas_price()

            return {
                'chain_id': chain_id,
                'network': NETWORK_NAMES.get(chain_id, 'Unknown'),
                'latest_block': block_number,
                'gas_price_gwei': round(gas_price / 10 ** 9, 2)
            }
        except Exception as e:
            return {'error': str(e), 'connected': False}

    #  Balance Operations
    def _validate_address(self, address: str) -> bool:
        """Check if address is valid format."""
        return (address.startswith('0x') and
                len(address) == 42 and
                all(c in '0123456789abcdefABCDEF' for c in address[2:]))

    def get_balance(self, address: str, unit: str = 'ether') -> Union[int, float]:
        """
        Get balance of an address.

        Args:
            address: Ethereum address (0x...)
            unit: 'wei', 'gwei', or 'ether'

        Returns:
            Balance in requested unit
        """
        if not self._validate_address(address):
            raise ValueError(f"Invalid address: {address}")

        if unit not in ['wei', 'gwei', 'ether']:
            raise ValueError("Unit must be 'wei', 'gwei', or 'ether'")

        # Get balance in wei (smallest unit)
        balance_wei_hex = self._make_rpc_call('eth_getBalance', [address, 'latest'])
        balance_wei = int(balance_wei_hex, 16)

        # Convert to requested unit
        if unit == 'wei':
            return balance_wei
        elif unit == 'gwei':
            return balance_wei / 1_000_000_000  # 10^9
        else:  # ether
            return balance_wei / 1_000_000_000_000_000_000  # 10^18

    #  Transaction Preparation
    def get_nonce(self, address: str) -> int:
        """Get the next transaction nonce for an address."""
        if not self._validate_address(address):
            raise ValueError(f"Invalid address: {address}")

        nonce_hex = self._make_rpc_call('eth_getTransactionCount', [address, 'pending'])
        return int(nonce_hex, 16)

    def get_gas_price(self, unit: str = 'gwei') -> Union[int, float]:
        """Get current gas price."""
        gas_price_wei_hex = self._make_rpc_call('eth_gasPrice')
        gas_price_wei = int(gas_price_wei_hex, 16)

        if unit == 'wei':
            return gas_price_wei
        elif unit == 'gwei':
            return gas_price_wei / 1_000_000_000
        else:
            return gas_price_wei / 1_000_000_000_000_000_000

    def estimate_gas(self, transaction: Dict[str, Any]) -> int:
        """
        Estimate gas for a transaction.

        Args:
            transaction: Dict with 'to', 'value', optional 'data'

        Returns:
            Estimated gas (simple approach)
        """
        if not isinstance(transaction, dict):
            raise ValueError("Transaction must be a dictionary")

        if 'to' not in transaction:
            raise ValueError("Transaction missing 'to' address")

        # Simple fallback: use RPC estimate if possible, else static
        try:
            gas_hex = self._make_rpc_call('eth_estimateGas', [transaction])
            gas = int(gas_hex, 16)
            if gas > 0:
                return gas
        except Exception as e:
            logger.warning(f"Gas estimation failed: {e}, using static estimate")

        # Static fallback based on transaction type
        if transaction.get('data') and len(transaction['data']) > 2:
            # Contract call
            data_bytes = (len(transaction['data']) - 2) // 2  # Remove 0x
            return 21_000 + (data_bytes * 16)  # Base + data cost
        else:
            # Simple ETH transfer
            return 21_000

    #  Transaction Sending
    def send_raw_transaction(self, signed_tx_hex: str) -> str:
        """Send a signed transaction to the network."""
        if not signed_tx_hex.startswith('0x'):
            raise ValueError("Transaction must start with 0x")

        if len(signed_tx_hex) < 100:  # Very rough check
            logger.warning("Transaction looks unusually short")

        tx_hash = self._make_rpc_call('eth_sendRawTransaction', [signed_tx_hex])
        logger.info(f"📤 Transaction sent: {tx_hash}")
        return tx_hash

    #  Transaction Monitoring
    def get_transaction_status(self, tx_hash: str) -> Dict[str, Any]:
        """
        Check transaction status (pending, confirmed, or not found).

        Args:
            tx_hash: Transaction hash (0x...)

        Returns:
            Status dictionary
        """
        if not tx_hash.startswith('0x') or len(tx_hash) != 66:
            raise ValueError("Invalid transaction hash")

        try:
            # First check if transaction exists
            tx = self._make_rpc_call('eth_getTransactionByHash', [tx_hash])
            if not tx:
                return {'status': 'not_found', 'message': 'Transaction not found'}

            # Check if confirmed (has receipt)
            receipt = self._make_rpc_call('eth_getTransactionReceipt', [tx_hash])
            if receipt:
                status = 'success' if receipt['status'] == '0x1' else 'failed'
                block_num = int(receipt['blockNumber'], 16) if receipt['blockNumber'] else 0
                return {
                    'status': status,
                    'message': f"Confirmed in block {block_num}",
                    'gas_used': int(receipt.get('gasUsed', '0x0'), 16)
                }
            else:
                return {'status': 'pending', 'message': 'Transaction pending'}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    #  Block Information
    def get_block_number(self) -> int:
        """Get the latest block number."""
        block_hex = self._make_rpc_call('eth_blockNumber')
        return int(block_hex, 16)

    def get_block_info(self, block_number: int) -> Dict[str, Any]:
        """Get basic info about a block."""
        if block_number < 0:
            raise ValueError("Block number cannot be negative")

        block_hex = hex(block_number)
        block_data = self._make_rpc_call('eth_getBlockByNumber', [block_hex, False])

        if not block_data:
            raise ValueError(f"Block {block_number} not found")

        return {
            'number': block_number,
            'timestamp': int(block_data['timestamp'], 16),
            'miner': block_data.get('miner', '0x0'),
            'gas_used': int(block_data.get('gasUsed', '0x0'), 16),
            'transaction_count': len(block_data.get('transactions', []))
        }

    # Simple Stats
    def get_stats(self) -> Dict[str, Any]:
        """Get basic usage statistics."""
        success_rate = (self.success_count / self.call_count * 100) if self.call_count > 0 else 0
        return {
            'total_calls': self.call_count,
            'successful_calls': self.success_count,
            'success_rate': round(success_rate, 1),
            'network': NETWORK_NAMES.get(self.expected_chain_id, 'Unknown')
        }

    def close(self):
        """Clean up resources."""
        logger.info("🔌 RPC Client closed")

