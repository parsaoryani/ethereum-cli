import unittest
import json
from unittest.mock import patch, MagicMock

import requests

from src.rpc_client import RPCClient
from pathlib import Path

class TestRPCClient(unittest.TestCase):
    def setUp(self):
        # Define test directories and files
        self.test_base_dir = Path(__file__).resolve().parent
        self.test_config_dir = self.test_base_dir / 'test_config'
        self.settings_file = self.test_config_dir / 'test_settings.json'
        self.main_settings_file = self.test_base_dir.parent / 'config' / 'settings.json'

        # Ensure test directories exist
        try:
            self.test_config_dir.mkdir(exist_ok=True)
        except OSError as e:
            self.fail(f"Failed to create test_config directory: {e}")

        # Backup original test_settings.json if it exists
        self.original_settings = {}
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    self.original_settings = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            self.fail(f"Failed to backup test_settings.json: {e}")

        # Backup original main settings.json as both JSON and raw string to preserve formatting
        self.original_main_settings = {}
        self.original_main_settings_raw = None
        try:
            if self.main_settings_file.exists():
                with open(self.main_settings_file, 'r') as f:
                    self.original_main_settings = json.load(f)
                    f.seek(0)
                    self.original_main_settings_raw = f.read()
        except (OSError, json.JSONDecodeError) as e:
            self.fail(f"Failed to backup main settings.json: {e}")

        # Create or reset test_settings.json
        try:
            with open(self.settings_file, 'w') as f:
                json.dump({
                    "network": {
                        "name": "Sepolia Testnet",
                        "chain_id": 11155111,
                        "rpc_url": "https://mock-rpc-url",
                        "currency_symbol": "ETH",
                        "block_explorer": "https://sepolia.etherscan.io"
                    },
                    "wallet": {
                        "storage_path": str(self.test_base_dir / 'test_wallet'),
                        "default_wallet": ""
                    },
                    "transaction": {
                        "default_gas_limit": 21000,
                        "max_gas_price_gwei": 100,
                        "default_gas_price_gwei": 1.0,
                        "etherscan_api_key": "mock-api-key"
                    }
                }, f, indent=4)
        except (OSError, json.JSONDecodeError) as e:
            self.fail(f"Failed to create test_settings.json: {e}")

        # Patch CONFIG_PATH and requests.Session.post
        try:
            self.patcher1 = patch('src.rpc_client.CONFIG_PATH', self.settings_file)
            self.patcher2 = patch('requests.Session.post', new=MagicMock())
            self.patcher1.start()
            self.patcher2.start()

            # Verify CONFIG_PATH patch
            import src.rpc_client
            self.assertEqual(str(src.rpc_client.CONFIG_PATH), str(self.settings_file),
                             f"CONFIG_PATH patch failed: expected {self.settings_file}, got {src.rpc_client.CONFIG_PATH}")

            # Configure mock response for eth_chainId in setUp
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": "0xaa36a7"}  # Chain ID 11155111
            self.patcher2.start().return_value = mock_response

            # Initialize RPCClient with mock settings
            self.client = RPCClient(rpc_url="https://mock-rpc-url", chain_id=11155111)
        except Exception as e:
            self.fail(f"Failed to initialize RPCClient: {e}")

    def tearDown(self):
        # Stop patchers
        try:
            self.patcher1.stop()
            self.patcher2.stop()
        except Exception as e:
            self.fail(f"Failed to stop patchers: {e}")

        # Restore original test_settings.json
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.original_settings, f, indent=4)
        except (OSError, json.JSONDecodeError) as e:
            self.fail(f"Failed to restore test_settings.json: {e}")

        # Restore original main settings.json with original formatting
        try:
            if self.original_main_settings_raw is not None:
                with open(self.main_settings_file, 'w') as f:
                    f.write(self.original_main_settings_raw)
            elif self.main_settings_file.exists():
                self.main_settings_file.unlink()
        except (OSError, json.JSONDecodeError) as e:
            self.fail(f"Failed to restore main settings.json: {e}")

        # Verify main settings.json hasn't changed
        try:
            if self.main_settings_file.exists():
                with open(self.main_settings_file, 'r') as f:
                    current_main_settings_raw = f.read()
                self.assertEqual(current_main_settings_raw, self.original_main_settings_raw,
                                 f"Main settings.json was modified unexpectedly: {current_main_settings_raw}")
        except (OSError, json.JSONDecodeError) as e:
            self.fail(f"Failed to verify main settings.json: {e}")

    def test_init_success(self):
        """Test successful initialization of RPCClient."""
        # Mock response for eth_chainId
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": "0x1"}
        self.patcher2.start().return_value = mock_response

        # Test initialization
        client = RPCClient(rpc_url="https://mock-rpc-url", chain_id=1)
        self.assertEqual(client.rpc_url, "https://mock-rpc-url")
        self.assertEqual(client.expected_chain_id, 1)
        self.assertEqual(client.timeout, 10)
        self.assertEqual(client.max_retries, 5)
        self.assertEqual(client.call_count, 1)
        self.assertEqual(client.success_count, 1)

    def test_get_chain_id_success(self):
        """Test retrieving chain ID successfully."""
        # Mock eth_chainId response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": "0xaa36a7"}
        self.patcher2.start().return_value = mock_response

        chain_id = self.client.get_chain_id()
        self.assertEqual(chain_id, 11155111)

    def test_get_chain_id_wrong_network(self):
        """Test chain ID retrieval with incorrect network."""
        # Mock eth_chainId with wrong chain ID
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": "0x1"}
        self.patcher2.start().return_value = mock_response

        with self.assertRaises(ValueError) as cm:
            self.client.get_chain_id()
        self.assertIn("Wrong network! Expected 11155111", str(cm.exception))

    def test_get_network_info_success(self):
        """Test retrieving network information successfully."""
        # Mock responses
        mock_response_chain = MagicMock()
        mock_response_chain.status_code = 200
        mock_response_chain.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": "0xaa36a7"}
        mock_response_block = MagicMock()
        mock_response_block.status_code = 200
        mock_response_block.json.return_value = {"jsonrpc": "2.0", "id": 2, "result": "0x123"}
        mock_response_gas = MagicMock()
        mock_response_gas.status_code = 200
        mock_response_gas.json.return_value = {"jsonrpc": "2.0", "id": 3, "result": "0x3b9aca00"}  # 1 Gwei
        self.patcher2.start().side_effect = [mock_response_chain, mock_response_block, mock_response_gas]

        info = self.client.get_network_info()
        self.assertEqual(info, {
            'chain_id': 11155111,
            'network': 'Sepolia Testnet',
            'latest_block': 0x123,
            'gas_price_gwei': 1.0
        })

    def test_get_network_info_failure(self):
        """Test network info retrieval with network error."""
        # Mock failure with RequestException
        mock_response = MagicMock()
        mock_response.side_effect = requests.exceptions.RequestException("Network error")
        self.patcher2.start().side_effect = mock_response

        info = self.client.get_network_info()
        self.assertEqual(info['connected'], False)
        self.assertIn('Network error', info['error'])
        self.assertEqual(info['network'], 'Unknown')

    def test_get_balance_success(self):
        """Test retrieving balance in different units."""
        # Mock eth_getBalance response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": "0x1bc16d674ec80000"}  # 2 ETH
        self.patcher2.start().return_value = mock_response

        balance = self.client.get_balance("0x1234567890123456789012345678901234567890", unit='ether')
        self.assertEqual(balance, 2.0)

        balance_wei = self.client.get_balance("0x1234567890123456789012345678901234567890", unit='wei')
        self.assertEqual(balance_wei, 2000000000000000000)

        balance_gwei = self.client.get_balance("0x1234567890123456789012345678901234567890", unit='gwei')
        self.assertEqual(balance_gwei, 2000000000.0)

    def test_get_balance_invalid_address(self):
        """Test balance retrieval with invalid address."""
        with self.assertRaises(ValueError) as cm:
            self.client.get_balance("invalid_address")
        self.assertEqual(str(cm.exception), "Invalid address: invalid_address")

    def test_get_balance_invalid_unit(self):
        """Test balance retrieval with invalid unit."""
        with self.assertRaises(ValueError) as cm:
            self.client.get_balance("0x1234567890123456789012345678901234567890", unit='invalid')
        self.assertEqual(str(cm.exception), "Unit must be 'wei', 'gwei', or 'ether'")

    def test_get_nonce_success(self):
        """Test retrieving transaction nonce successfully."""
        # Mock eth_getTransactionCount response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": "0x5"}
        self.patcher2.start().return_value = mock_response

        nonce = self.client.get_nonce("0x1234567890123456789012345678901234567890")
        self.assertEqual(nonce, 5)

    def test_get_nonce_invalid_address(self):
        """Test nonce retrieval with invalid address."""
        with self.assertRaises(ValueError) as cm:
            self.client.get_nonce("invalid_address")
        self.assertEqual(str(cm.exception), "Invalid address: invalid_address")

    def test_get_gas_price_success(self):
        """Test retrieving gas price in different units."""
        # Mock eth_gasPrice response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": "0x3b9aca00"}  # 1 Gwei
        self.patcher2.start().return_value = mock_response

        gas_price = self.client.get_gas_price(unit='gwei')
        self.assertEqual(gas_price, 1.0)

        gas_price_wei = self.client.get_gas_price(unit='wei')
        self.assertEqual(gas_price_wei, 1000000000)

        gas_price_ether = self.client.get_gas_price(unit='ether')
        self.assertEqual(gas_price_ether, 0.000000001)

    def test_get_gas_price_zero_fallback(self):
        """Test gas price retrieval with zero value fallback."""
        # Mock eth_gasPrice returning 0
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": "0x0"}
        self.patcher2.start().return_value = mock_response

        gas_price = self.client.get_gas_price(unit='gwei')
        self.assertEqual(gas_price, 1.0)  # Should use default from test_settings.json

    def test_estimate_gas_success(self):
        """Test estimating gas for a transaction."""
        # Mock eth_estimateGas response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": "0x5208"}  # 21000
        self.patcher2.start().return_value = mock_response

        tx = {"to": "0x1234567890123456789012345678901234567890", "value": "0x1"}
        gas = self.client.estimate_gas(tx)
        self.assertEqual(gas, 21000)

    def test_estimate_gas_invalid_transaction(self):
        """Test gas estimation with invalid transaction."""
        with self.assertRaises(ValueError) as cm:
            self.client.estimate_gas("invalid")
        self.assertEqual(str(cm.exception), "Transaction must be a dictionary")

        with self.assertRaises(ValueError) as cm:
            self.client.estimate_gas({})
        self.assertEqual(str(cm.exception), "Transaction missing 'to' address")

    def test_send_raw_transaction_success(self):
        """Test sending a raw transaction successfully."""
        # Mock eth_sendRawTransaction response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": "0x" + "1" * 64}
        self.patcher2.start().return_value = mock_response

        tx_hash = self.client.send_raw_transaction("0x" + "f" * 100)
        self.assertEqual(tx_hash, "0x" + "1" * 64)

    def test_send_raw_transaction_invalid(self):
        """Test sending an invalid raw transaction."""
        with self.assertRaises(ValueError) as cm:
            self.client.send_raw_transaction("invalid")
        self.assertEqual(str(cm.exception), "Transaction must start with 0x")

    def test_get_transaction_status_success(self):
        """Test retrieving successful transaction status."""
        # Mock eth_getTransactionByHash and eth_getTransactionReceipt
        mock_response_tx = MagicMock()
        mock_response_tx.status_code = 200
        mock_response_tx.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": {"hash": "0x" + "1" * 64}}
        mock_response_receipt = MagicMock()
        mock_response_receipt.status_code = 200
        mock_response_receipt.json.return_value = {
            "jsonrpc": "2.0", "id": 2, "result": {
                "status": "0x1",
                "blockNumber": "0x123",
                "gasUsed": "0x5208"
            }
        }
        self.patcher2.start().side_effect = [mock_response_tx, mock_response_receipt]

        status = self.client.get_transaction_status("0x" + "1" * 64)
        self.assertEqual(status, {
            'status': 'success',
            'message': 'Confirmed in block 291',
            'gas_used': 21000,
            'block_number': 291
        })

    def test_get_transaction_status_pending(self):
        """Test retrieving status of a pending transaction."""
        # Mock eth_getTransactionByHash (exists) and eth_getTransactionReceipt (None)
        mock_response_tx = MagicMock()
        mock_response_tx.status_code = 200
        mock_response_tx.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": {"hash": "0x" + "1" * 64}}
        mock_response_receipt = MagicMock()
        mock_response_receipt.status_code = 200
        mock_response_receipt.json.return_value = {"jsonrpc": "2.0", "id": 2, "result": None}
        self.patcher2.start().side_effect = [mock_response_tx, mock_response_receipt]

        status = self.client.get_transaction_status("0x" + "1" * 64)
        self.assertEqual(status, {
            'status': 'pending',
            'message': 'Transaction pending',
            'gas_used': 0,
            'block_number': 'N/A'
        })

    def test_get_transaction_status_not_found(self):
        """Test retrieving status of a non-existent transaction."""
        # Mock eth_getTransactionByHash (None)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": None}
        self.patcher2.start().return_value = mock_response

        status = self.client.get_transaction_status("0x" + "1" * 64)
        self.assertEqual(status, {
            'status': 'not_found',
            'message': 'Transaction not found',
            'gas_used': 0,
            'block_number': 'N/A'
        })

    def test_get_transaction_status_invalid_hash(self):
        """Test transaction status with invalid hash."""
        with self.assertRaises(ValueError) as cm:
            self.client.get_transaction_status("invalid")
        self.assertEqual(str(cm.exception), "Invalid transaction hash")

    def test_get_block_number_success(self):
        """Test retrieving the latest block number."""
        # Mock eth_blockNumber response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": "0x123"}
        self.patcher2.start().return_value = mock_response

        block_number = self.client.get_block_number()
        self.assertEqual(block_number, 0x123)

    def test_get_block_info_success(self):
        """Test retrieving block information successfully."""
        # Mock eth_getBlockByNumber response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "timestamp": "0x5f5e100",
                "miner": "0x1234567890123456789012345678901234567890",
                "gasUsed": "0x5208",
                "transactions": ["0x" + "1" * 64]
            }
        }
        self.patcher2.start().return_value = mock_response

        block_info = self.client.get_block_info(100)
        self.assertEqual(block_info, {
            'number': 100,
            'timestamp': 0x5f5e100,
            'miner': "0x1234567890123456789012345678901234567890",
            'gas_used': 21000,
            'transaction_count': 1
        })

    def test_get_block_info_invalid_block(self):
        """Test block info retrieval for non-existent block."""
        # Mock eth_getBlockByNumber not found
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": None}
        self.patcher2.start().return_value = mock_response

        with self.assertRaises(ValueError) as cm:
            self.client.get_block_info(100)
        self.assertEqual(str(cm.exception), "Block 100 not found")

    def test_get_block_info_negative_block(self):
        """Test block info retrieval with negative block number."""
        with self.assertRaises(ValueError) as cm:
            self.client.get_block_info(-1)
        self.assertEqual(str(cm.exception), "Block number cannot be negative")

    def test_get_stats(self):
        """Test retrieving RPC client statistics."""
        # Mock two successful calls
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": "0xaa36a7"}
        self.patcher2.start().return_value = mock_response

        # Make two calls
        self.client.get_chain_id()
        self.client.get_block_number()

        stats = self.client.get_stats()
        self.assertEqual(stats, {
            'total_calls': 3,  # Including initial call in __init__
            'successful_calls': 3,
            'success_rate': 100.0,
            'network': 'Sepolia Testnet'
        })

if __name__ == '__main__':
    unittest.main()