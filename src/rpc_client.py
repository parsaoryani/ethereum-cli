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


#  Simple Tests
if __name__ == '__main__':
    print("🚀 Starting Simple RPC Client Tests")
    print("=" * 50)

    # Create client
    client = RPCClient(timeout=5, max_retries=2)

    # Test 1: Network Connection
    print("\n1️⃣ Testing Network Connection...")
    try:
        info = client.get_network_info()
        print(f"   ✅ Connected to {info['network']}")
        print(f"   ✅ Latest Block: {info['latest_block']:,}")
        print(f"   ✅ Gas Price: {info['gas_price_gwei']} Gwei")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")

    # Test 2: Balance Check
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

    # Test 3: Transaction Preparation
    print("\n3️⃣ Testing Transaction Preparation...")
    try:
        nonce = client.get_nonce(zero_address)
        gas_price = client.get_gas_price('gwei')
        print(f"   ✅ Nonce: {nonce}")
        print(f"   ✅ Gas Price: {gas_price:.2f} Gwei")

        # Simple gas estimation
        sample_tx = {
            'to': '0x742d35Cc6634C0532925a3b8D7C4aE7B6733E6B5',
            'value': '0x16345785d8a0000'  # 0.1 ETH
        }
        gas_estimate = client.estimate_gas(sample_tx)
        print(f"   ✅ Gas Estimate: {gas_estimate:,}")
    except Exception as e:
        print(f"   ❌ Transaction prep failed: {e}")

    # Test 4: Transaction Status
    print("\n4️⃣ Testing Transaction Status...")
    test_hash = '0x0000000000000000000000000000000000000000000000000000000000000000'
    try:
        status = client.get_transaction_status(test_hash)
        print(f"   ✅ Status: {status['status']} - {status['message']}")
    except Exception as e:
        print(f"   ❌ Status test failed: {e}")

    # Test 5: Block Information
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

    # Test 6: Input Validation
    print("\n6️⃣ Testing Input Validation...")
    test_cases = [
        ('invalid_addr', "Invalid address"),
        ('0xshort', "Invalid address"),
        ('0x' + 'a' * 40, "Valid format but random")  # This should work
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

    # Test 7: Stats
    print("\n7️⃣ Testing Statistics...")
    stats = client.get_stats()
    print(f"   ✅ Total Calls: {stats['total_calls']}")
    print(f"   ✅ Success Rate: {stats['success_rate']}%")

    # Cleanup
    client.close()
    print("\n🎉 All Tests Completed!")
    print("=" * 50)


# 🧪 Comprehensive Function Tests
# Testing all functions in RPCClient
# Each section is separated for clarity

print("\n=================== Comprehensive Function Tests ===================")

# Test Section 1: get_chain_id
print("\nSection 1: Testing get_chain_id")
try:
    chain_id = client.get_chain_id()
    print(f"   ✅ Chain ID: {chain_id}")
    print(f"   ✅ Expected: {client.expected_chain_id}")
except Exception as e:
    print(f"   ❌ get_chain_id failed: {e}")

# Test Section 2: get_network_info
print("\nSection 2: Testing get_network_info")
try:
    info = client.get_network_info()
    if 'error' in info:
        print(f"   ❌ Error: {info['error']}")
    else:
        print(f"   ✅ Chain ID: {info['chain_id']}")
        print(f"   ✅ Network: {info['network']}")
        print(f"   ✅ Latest Block: {info['latest_block']:,}")
        print(f"   ✅ Gas Price Gwei: {info['gas_price_gwei']}")
except Exception as e:
    print(f"   ❌ get_network_info failed: {e}")

# Test Section 3: _validate_address (private, but testing directly)
print("\nSection 3: Testing _validate_address")
test_addresses = [
    ('0x0000000000000000000000000000000000000000', True),  # Valid zero address
    ('0x742d35Cc6634C0532925a3b8D7C4aE7B6733E6B5', True),  # Valid random address
    ('invalid_addr', False),  # Invalid no 0x
    ('0xshort', False),  # Too short
    ('0x' + 'a' * 40, True),  # Valid hex format
    ('0x742d35xyz', False)  # Invalid chars
]
for addr, expected in test_addresses:
    result = client._validate_address(addr)
    status = "✅" if result == expected else "❌"
    print(f"   {status} Address '{addr[:10]}...': Expected {expected}, Got {result}")

# Test Section 4: get_balance
print("\nSection 4: Testing get_balance")
test_address = '0x0000000000000000000000000000000000000000'  # Zero address
units = ['ether', 'wei', 'gwei']
for unit in units:
    try:
        balance = client.get_balance(test_address, unit)
        print(f"   ✅ Balance in {unit}: {balance}")
    except Exception as e:
        print(f"   ❌ get_balance ({unit}) failed: {e}")

# Test Section 5: get_nonce
print("\nSection 5: Testing get_nonce")
try:
    nonce = client.get_nonce(test_address)
    print(f"   ✅ Nonce for {test_address[:10]}...: {nonce}")
except Exception as e:
    print(f"   ❌ get_nonce failed: {e}")

# Test Section 6: get_gas_price
print("\nSection 6: Testing get_gas_price")
units = ['gwei', 'wei', 'ether']
for unit in units:
    try:
        gas_price = client.get_gas_price(unit)
        print(f"   ✅ Gas Price in {unit}: {gas_price}")
    except Exception as e:
        print(f"   ❌ get_gas_price ({unit}) failed: {e}")

# Test Section 7: estimate_gas
print("\nSection 7: Testing estimate_gas")
sample_tx = {
    'to': '0x742d35Cc6634C0532925a3b8D7C4aE7B6733E6B5',
    'value': '0x16345785d8a0000'  # 0.1 ETH
}
try:
    gas = client.estimate_gas(sample_tx)
    print(f"   ✅ Estimated Gas for sample tx: {gas:,}")
except Exception as e:
    print(f"   ❌ estimate_gas failed: {e}")

# Test Section 8: send_raw_transaction
print("\nSection 8: Testing send_raw_transaction")
# Note: We can't send real tx without signed data, so test validation only
try:
    # Invalid input test
    client.send_raw_transaction('invalid_tx_hex')
    print("   ❌ Should have raised error but didn't")
except ValueError as e:
    print(f"   ✅ Validation caught invalid tx: {e}")

# Test Section 9: get_transaction_status
print("\nSection 9: Testing get_transaction_status")
test_hash = '0x0000000000000000000000000000000000000000000000000000000000000000'  # Invalid hash
try:
    status = client.get_transaction_status(test_hash)
    print(f"   ✅ Status: {status['status']} - {status['message']}")
except Exception as e:
    print(f"   ❌ get_transaction_status failed: {e}")

# Test Section 10: get_block_number
print("\nSection 10: Testing get_block_number")
try:
    block_num = client.get_block_number()
    print(f"   ✅ Latest Block Number: {block_num:,}")
except Exception as e:
    print(f"   ❌ get_block_number failed: {e}")

# Test Section 11: get_block_info
print("\nSection 11: Testing get_block_info")
try:
    block_num = client.get_block_number()
    block_info = client.get_block_info(block_num - 1)  # Previous block
    print(f"   ✅ Block Number: {block_info['number']:,}")
    print(f"   ✅ Timestamp: {block_info['timestamp']} (Unix)")
    print(f"   ✅ Miner: {block_info['miner']}")
    print(f"   ✅ Gas Used: {block_info['gas_used']:,}")
    print(f"   ✅ Transaction Count: {block_info['transaction_count']}")
except Exception as e:
    print(f"   ❌ get_block_info failed: {e}")

# Test Section 12: get_stats
print("\nSection 12: Testing get_stats")
try:
    stats = client.get_stats()
    print(f"   ✅ Total Calls: {stats['total_calls']}")
    print(f"   ✅ Successful Calls: {stats['successful_calls']}")
    print(f"   ✅ Success Rate: {stats['success_rate']}%")
    print(f"   ✅ Network: {stats['network']}")
except Exception as e:
    print(f"   ❌ get_stats failed: {e}")

# Test Section 13: close
print("\nSection 13: Testing close")
try:
    client.close()
    print("   ✅ Close succeeded (check log for 🔌 RPC Client closed)")
except Exception as e:
    print(f"   ❌ close failed: {e}")

print("\n=================== End of Comprehensive Function Tests ===================")