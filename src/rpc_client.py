import json
import requests
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import warnings
warnings.filterwarnings("ignore", category=Warning)

# Configuration path
CONFIG_PATH = Path(__file__).parent.parent / 'config' / 'settings.json'

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
    Improved Ethereum RPC Client with enhanced rate limiting handling.
    Features:
    - Basic RPC calls with exponential backoff for 429 errors
    - Balance with unit conversion
    - Gas estimation
    - Transaction monitoring
    - Simple rate limiting to prevent 429 errors
    """

    def __init__(self, rpc_url: str = None, chain_id: int = None, timeout: int = 10, max_retries: int = 5):
        """
        Initialize RPC Client with basic settings.

        Args:
            rpc_url: Ethereum RPC endpoint
            chain_id: Expected network chain ID
            timeout: Request timeout in seconds
            max_retries: Number of retry attempts
        """
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        self.rpc_url = rpc_url or config['network']['rpc_url']
        self.expected_chain_id = chain_id or config['network']['chain_id']
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers = {'Content-Type': 'application/json'}
        self.session = requests.Session()
        self.request_id = 0
        self.last_request_time = 0
        self.min_request_interval = 0.5  # Minimum 0.5 seconds between requests

        # Simple metrics tracking
        self.call_count = 0
        self.success_count = 0

        # Test connection
        try:
            self.get_chain_id()
            logger.info(f"✅ Connected to {self.rpc_url} (Chain ID: {self.expected_chain_id})")
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            raise

    def _make_rpc_call(self, method: str, params: List[Any] = None) -> Any:
        """
        Make a JSON-RPC call with exponential backoff for 429 errors and rate limiting.
        """
        if params is None:
            params = []

        self.call_count += 1
        self.request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": self.request_id
        }

        logger.info(f"🔄 Calling {method} with params: {params}")

        # Enforce minimum interval between requests
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            logger.debug(f"Rate limiting: waiting {sleep_time:.2f}s before request")
            time.sleep(sleep_time)

        for attempt in range(self.max_retries):
            try:
                response = self.session.post(
                    self.rpc_url,
                    headers=self.headers,
                    data=json.dumps(payload),
                    timeout=self.timeout
                )
                response.raise_for_status()
                result = response.json()

                logger.debug(f"Raw response for {method}: {result}")

                if 'error' in result:
                    error_msg = result['error'].get('message', 'Unknown error')
                    logger.error(f"❌ RPC Error {method}: {error_msg}")
                    raise ValueError(f"RPC error: {error_msg}")

                self.success_count += 1
                self.last_request_time = time.time()
                logger.info(f"✅ {method} succeeded")
                logger.info(f"Raw result for {method}: {result.get('result', 'None')}")
                return result['result']

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    # Exponential backoff: 5 * 2^attempt seconds
                    backoff_time = 5 * (2 ** attempt)
                    logger.warning(f"⏰ 429 Too Many Requests on attempt {attempt + 1}/{self.max_retries}. Waiting {backoff_time}s")
                    time.sleep(backoff_time)
                    continue
                logger.warning(f"🌐 HTTP error on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(5)
                    continue
                raise ConnectionError(f"HTTP error: {e}")

            except requests.exceptions.Timeout:
                logger.warning(f"⏰ Timeout on attempt {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    time.sleep(5)
                    continue
                raise ConnectionError("Request timed out after retries")

            except requests.exceptions.RequestException as e:
                logger.warning(f"🌐 Network error on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(5)
                    continue
                raise ConnectionError(f"Network error: {e}")

            except json.JSONDecodeError:
                raise ValueError("Invalid JSON response from RPC")

        raise ConnectionError(f"Failed after {self.max_retries} attempts")

    def get_chain_id(self) -> int:
        """Get and validate the chain ID."""
        chain_id_hex = self._make_rpc_call('eth_chainId')
        chain_id = int(chain_id_hex, 16)
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
            gas_price = self.get_gas_price(unit='gwei')
            if gas_price < 0.001:
                logger.warning(f"Gas price very low ({gas_price:.6f} Gwei) - may cause slow confirmations")
            return {
                'chain_id': chain_id,
                'network': NETWORK_NAMES.get(chain_id, 'Unknown'),
                'latest_block': block_number,
                'gas_price_gwei': round(gas_price, 6)
            }
        except Exception as e:
            logger.error(f"Failed to get network info: {e}")
            return {
                'error': str(e),
                'connected': False,
                'network': 'Unknown',
                'chain_id': None,
                'latest_block': None,
                'gas_price_gwei': None
            }

    def _validate_address(self, address: str) -> bool:
        """Check if address is valid format."""
        return (address.startswith('0x') and
                len(address) == 42 and
                all(c in '0123456789abcdefABCDEF' for c in address[2:]))

    def get_balance(self, address: str, unit: str = 'ether') -> Union[int, float]:
        """
        Get balance of an address.
        """
        if not self._validate_address(address):
            raise ValueError(f"Invalid address: {address}")

        if unit not in ['wei', 'gwei', 'ether']:
            raise ValueError("Unit must be 'wei', 'gwei', or 'ether'")

        balance_wei_hex = self._make_rpc_call('eth_getBalance', [address, 'latest'])
        balance_wei = int(balance_wei_hex, 16)

        if unit == 'wei':
            return balance_wei
        elif unit == 'gwei':
            return balance_wei / 1_000_000_000
        else:  # ether
            return balance_wei / 1_000_000_000_000_000_000

    def get_nonce(self, address: str) -> int:
        """Get the next transaction nonce for an address."""
        if not self._validate_address(address):
            raise ValueError(f"Invalid address: {address}")

        nonce_hex = self._make_rpc_call('eth_getTransactionCount', [address, 'pending'])
        return int(nonce_hex, 16)

    def get_gas_price(self, unit: str = 'gwei') -> Union[int, float]:
        """Get current gas price with fallback for zero values only."""
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        default_gas_price_gwei = config.get('transaction', {}).get('default_gas_price_gwei', 1.0)
        default_gas_price_wei = default_gas_price_gwei * 1_000_000_000

        gas_price_wei_hex = self._make_rpc_call('eth_gasPrice')
        logger.info(f"Raw eth_gasPrice hex: {gas_price_wei_hex}")
        gas_price_wei = int(gas_price_wei_hex, 16)

        if gas_price_wei == 0:
            logger.warning(f"Zero gas price received, using default {default_gas_price_gwei} Gwei")
            gas_price_wei = default_gas_price_wei

        if unit == 'wei':
            return gas_price_wei
        elif unit == 'gwei':
            return gas_price_wei / 1_000_000_000
        else:
            return gas_price_wei / 1_000_000_000_000_000_000

    def estimate_gas(self, transaction: Dict[str, Any]) -> int:
        """
        Estimate gas for a transaction.
        """
        if not isinstance(transaction, dict):
            raise ValueError("Transaction must be a dictionary")

        if 'to' not in transaction:
            raise ValueError("Transaction missing 'to' address")

        try:
            gas_hex = self._make_rpc_call('eth_estimateGas', [transaction])
            gas = int(gas_hex, 16)
            if gas > 0:
                return gas
        except Exception as e:
            logger.warning(f"Gas estimation failed: {e}, using static estimate")

        if transaction.get('data') and len(transaction['data']) > 2:
            data_bytes = (len(transaction['data']) - 2) // 2
            return 21_000 + (data_bytes * 16)
        else:
            return 21_000

    def send_raw_transaction(self, signed_tx_hex: str) -> str:
        """Send a signed transaction to the network."""
        if not signed_tx_hex.startswith('0x'):
            raise ValueError("Transaction must start with 0x")

        if len(signed_tx_hex) < 100:
            logger.warning("Transaction looks unusually short")

        tx_hash = self._make_rpc_call('eth_sendRawTransaction', [signed_tx_hex])
        logger.info(f"📤 Transaction sent: {tx_hash}")
        return tx_hash

    def get_transaction_status(self, tx_hash: str) -> Dict[str, Any]:
        """
        Check transaction status (pending, confirmed, or not found).
        """
        if not tx_hash.startswith('0x') or len(tx_hash) != 66:
            raise ValueError("Invalid transaction hash")
        try:
            tx = self._make_rpc_call('eth_getTransactionByHash', [tx_hash])
            if not tx:
                return {
                    'status': 'not_found',
                    'message': 'Transaction not found',
                    'gas_used': 0,
                    'block_number': 'N/A'
                }
            receipt = self._make_rpc_call('eth_getTransactionReceipt', [tx_hash])
            if receipt:
                status = 'success' if receipt['status'] == '0x1' else 'failed'
                block_num = int(receipt['blockNumber'], 16) if receipt['blockNumber'] else 0
                return {
                    'status': status,
                    'message': f"Confirmed in block {block_num}",
                    'gas_used': int(receipt.get('gasUsed', '0x0'), 16),
                    'block_number': block_num
                }
            else:
                return {
                    'status': 'pending',
                    'message': 'Transaction pending',
                    'gas_used': 0,
                    'block_number': 'N/A'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'gas_used': 0,
                'block_number': 'N/A'
            }

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
            'timestamp': int(block_data['timestamp'], 16) if block_data.get('timestamp') else 0,
            'miner': block_data.get('miner', '0x0'),
            'gas_used': int(block_data.get('gasUsed', '0x0'), 16),
            'transaction_count': len(block_data.get('transactions', []))
        }

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
        self.session.close()
        logger.info("RPC Client closed")

if __name__ == '__main__':
    print("🚀 Starting Simple RPC Client Tests")
    print("=" * 50)

    client = RPCClient(timeout=5, max_retries=5)

    print("\n1️⃣ Testing Network Connection...")
    try:
        info = client.get_network_info()
        print(f"   ✅ Connected to {info['network']}")
        print(f"   ✅ Latest Block: {info['latest_block']:,}")
        print(f"   ✅ Gas Price: {info['gas_price_gwei']:.6f} Gwei")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")

    print("\n2️⃣ Testing Balance Operations...")
    zero_address = '0x0000000000000000000000000000000000000000'
    try:
        eth_balance = client.get_balance(zero_address, 'ether')
        wei_balance = client.get_balance(zero_address, 'wei')
        print(f"   ✅ Zero Address:")
        print(f"      ETH: {eth_balance:,.4f}")
        print(f"      Wei: {wei_balance:,}")
    except Exception as e:
        print(f"   ❌ Balance test failed: {e}")

    print("\n3️⃣ Testing Transaction Preparation...")
    try:
        nonce = client.get_nonce(zero_address)
        gas_price = client.get_gas_price('gwei')
        print(f"   ✅ Nonce: {nonce}")
        print(f"   ✅ Gas Price: {gas_price:.6f} Gwei")

        sample_tx = {
            'to': '0x742d35Cc6634C0532925a3b8D7C4aE7B6733E6B5',
            'value': '0x16345785d8a0000'  # 0.1 ETH
        }
        gas_estimate = client.estimate_gas(sample_tx)
        print(f"   ✅ Gas Estimate: {gas_estimate:,}")
    except Exception as e:
        print(f"   ❌ Transaction prep failed: {e}")

    print("\n4️⃣ Testing Transaction Status...")
    test_hash = '0xb54d72c08764463ee2a101ef63640855abed01cc7cb040be1e04b2c9c3e2dfd3'
    try:
        status = client.get_transaction_status(test_hash)
        print(f"   ✅ Status: {status['status']} - {status['message']}")
    except Exception as e:
        print(f"   ❌ Status test failed: {e}")

    print("\n5️⃣ Testing Block Information...")
    try:
        block_num = client.get_block_number()
        block_info = client.get_block_info(block_num - 1)
        print(f"   ✅ Latest Block: {block_num}")
        print(f"   ✅ Previous Block: {block_info['number']}")
        print(f"   ✅ Transactions: {block_info['transaction_count']}")
        print(f"   ✅ Gas Used: {block_info['gas_used']:,}")
    except Exception as e:
        print(f"   ❌ Block test failed: {e}")

    print("\n6️⃣ Testing Input Validation...")
    test_cases = [
        ('invalid_addr', "Invalid address"),
        ('0xshort', "Invalid address"),
        ('0x' + 'a' * 40, "Valid format but random")
    ]
    for addr, expected in test_cases:
        try:
            balance = client.get_balance(addr, 'ether')
            if expected == "Valid format but random":
                print(f"   ✅ {addr[:10]}...: {balance:.6f} ETH")
            else:
                print(f"   ❌ Validation failed for {addr}: should have raised error")
        except ValueError as e:
            if expected != "Valid format but random":
                print(f"   ✅ Validation caught: {addr} -> {e}")
            else:
                print(f"   ❌ Unexpected error for valid format: {e}")

    print("\n7️⃣ Testing Statistics...")
    stats = client.get_stats()
    print(f"   ✅ Total Calls: {stats['total_calls']}")
    print(f"   ✅ Success Rate: {stats['success_rate']}%")

    print("\n8️⃣ Testing Retry Logic...")
    try:
        temp_client = RPCClient(timeout=0.001, max_retries=2)
        temp_client.get_chain_id()
        print("   ❌ Should have raised timeout error")
    except ConnectionError as e:
        print(f"   ✅ Retry caught: {e}")

    client.close()
    print("\nAll Tests Completed!")
    print("=" * 50)