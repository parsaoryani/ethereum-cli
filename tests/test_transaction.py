import os
import unittest
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO
import requests
from eth_utils import to_bytes, to_hex

# Add project root to sys.path to resolve imports
project_root = str(Path(__file__).resolve().parent.parent)
print(f"Adding project root to sys.path: {project_root}")
print(f"sys.path before: {sys.path}")
sys.path.append(project_root)
print(f"sys.path after: {sys.path}")

from src.transaction import TransactionManager, transaction_send, transaction_status, transaction_history, transaction_export

class TestTransactionManager(unittest.TestCase):
    def setUp(self):
        # Define test directories and files
        self.test_base_dir = Path(__file__).resolve().parent
        print(f"Current working directory: {Path.cwd()}")
        print(f"Looking for src directory: {self.test_base_dir.parent / 'src'}")
        self.test_config_dir = self.test_base_dir / 'test_config'
        self.settings_file = self.test_config_dir / 'test_settings.json'
        self.main_settings_file = self.test_base_dir.parent / 'config' / 'settings.json'
        self.test_export_dir = self.test_base_dir / 'test_exports'
        os.environ["ETHERSCAN_API_KEY"] = "mock-api-key"
        os.environ["RPC_URL"] = "mock-rpc-url"
        # Ensure test directories exist
        self.test_config_dir.mkdir(exist_ok=True)
        self.test_export_dir.mkdir(exist_ok=True)

        # Backup original test_settings.json if it exists
        self.original_settings = {}
        if self.settings_file.exists():
            with open(self.settings_file, 'r') as f:
                self.original_settings = json.load(f)

        # Backup original main settings.json as both JSON and raw string to preserve formatting
        self.original_main_settings = {}
        self.original_main_settings_raw = None
        if self.main_settings_file.exists():
            with open(self.main_settings_file, 'r') as f:
                self.original_main_settings = json.load(f)
                f.seek(0)
                self.original_main_settings_raw = f.read()

        # Create or reset test_settings.json
        with open(self.settings_file, 'w') as f:
            json.dump({
                "network": {
                    "name": "Sepolia Testnet",
                    "chain_id": 11155111,
                    "currency_symbol": "ETH",
                    "block_explorer": "https://sepolia.etherscan.io"
                },
                "wallet": {
                    "storage_path": str(self.test_base_dir / 'test_wallet'),
                    "default_wallet": "0x1234567890123456789012345678901234567890"
                },
                "transaction": {
                    "default_gas_limit": 21000,
                    "max_gas_price_gwei": 100,
                    "default_gas_price_gwei": 1.0

                }
            }, f, indent=4)

        # Patch dependencies
        self.patcher1 = patch('src.transaction.CONFIG_PATH', self.settings_file)
        self.patcher2 = patch('src.transaction.EXPORT_PATH', self.test_export_dir)
        self.patcher3 = patch('src.transaction.RPCClient')
        self.patcher4 = patch('src.transaction.WalletManager')
        self.patcher5 = patch('requests.get')
        self.patcher1.start()
        self.patcher2.start()
        self.mock_rpc_client = self.patcher3.start()
        self.mock_wallet_manager = self.patcher4.start()
        self.mock_requests_get = self.patcher5.start()

        # Configure mock RPCClient
        self.mock_rpc_instance = MagicMock()
        self.mock_rpc_client.return_value = self.mock_rpc_instance
        self.mock_rpc_instance.get_chain_id.return_value = 11155111
        self.mock_rpc_instance.get_nonce.return_value = 5
        self.mock_rpc_instance.get_balance.return_value = 2000000000000000000  # 2 ETH in wei
        self.mock_rpc_instance.get_gas_price.return_value = 1.0  # 1 Gwei
        self.mock_rpc_instance.estimate_gas.return_value = 21000
        self.mock_rpc_instance.send_raw_transaction.return_value = "0x" + "1" * 64
        self.mock_rpc_instance.get_transaction_status.return_value = {
            'status': 'success',
            'message': 'Confirmed in block 291',
            'gas_used': 21000,
            'block_number': 291
        }

        # Configure mock WalletManager
        self.mock_wallet_instance = MagicMock()
        self.mock_wallet_manager.return_value = self.mock_wallet_instance
        self.mock_wallet_instance._is_valid_address.return_value = True
        self.mock_wallet_instance.get_wallet_info.return_value = {
            'private_key_available': True,
            'private_key': "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            'address': "0x1234567890123456789012345678901234567890"
        }
        self.mock_wallet_instance.get_default_wallet.return_value = "0x1234567890123456789012345678901234567890"

        # Initialize TransactionManager
        self.manager = TransactionManager()

    def tearDown(self):
        # Stop patchers
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()
        self.patcher4.stop()
        self.patcher5.stop()

        # Restore original test_settings.json
        with open(self.settings_file, 'w') as f:
            json.dump(self.original_settings, f, indent=4)

        # Restore original main settings.json with original formatting
        if self.original_main_settings_raw is not None:
            with open(self.main_settings_file, 'w') as f:
                f.write(self.original_main_settings_raw)
        elif self.main_settings_file.exists():
            self.main_settings_file.unlink()

        # Verify main settings.json hasn't changed
        if self.main_settings_file.exists():
            with open(self.main_settings_file, 'r') as f:
                current_main_settings_raw = f.read()
            self.assertEqual(current_main_settings_raw, self.original_main_settings_raw,
                             f"Main settings.json was modified unexpectedly: {current_main_settings_raw}")

    def test_init_success(self):
        self.assertIsNotNone(self.manager.rpc_client)
        self.assertIsNotNone(self.manager.wallet_manager)
        self.assertEqual(self.manager.default_gas_limit, 21000)
        self.assertEqual(self.manager.max_gas_price_gwei, 100)
        self.assertEqual(self.manager.default_gas_price_gwei, 1.0)
        self.assertEqual(self.manager.etherscan_api_key, "mock-api-key")

    def test_init_missing_config_file(self):
        with patch('src.transaction.CONFIG_PATH', self.test_base_dir / 'nonexistent.json'):
            with self.assertRaises(ValueError) as cm:
                TransactionManager()
            self.assertIn("Configuration file not found", str(cm.exception))

    def test_init_invalid_json(self):
        with open(self.settings_file, 'w') as f:
            f.write("invalid json")
        with self.assertRaises(ValueError) as cm:
            TransactionManager()
        self.assertIn("Invalid JSON format", str(cm.exception))

    def test_init_missing_config_keys(self):
        with open(self.settings_file, 'w') as f:
            json.dump({"wrong_key": {}}, f)
        with self.assertRaises(ValueError) as cm:
            TransactionManager()
        self.assertIn("Missing required configuration key", str(cm.exception))

    def test_build_transaction_success(self):
        tx = self.manager._build_transaction(
            from_address="0x1234567890123456789012345678901234567890",
            to_address="0x0987654321098765432109876543210987654321",
            value_ether=1.0
        )
        self.assertEqual(tx['nonce'], 5)
        self.assertEqual(tx['to'], "0x0987654321098765432109876543210987654321")
        self.assertEqual(tx['value'], 1000000000000000000)  # 1 ETH in wei
        self.assertEqual(tx['gas'], 21000)
        self.assertEqual(tx['gasPrice'], 1000000000)  # 1 Gwei
        self.assertEqual(tx['chainId'], 11155111)
        self.assertEqual(tx['data'], b'')

    def test_build_transaction_invalid_addresses(self):
        # Test invalid recipient address
        with self.assertRaises(ValueError) as cm:
            self.mock_wallet_instance._is_valid_address.side_effect = [False, True]
            self.manager._build_transaction(
                from_address="0x7e4dd6856aa001b78f1f2fe1a4a1f0e5b2cce5f7",
                to_address="invalid",
                value_ether=1.0
            )
        self.assertIn("Invalid recipient address", str(cm.exception))

        # Test invalid sender address
        with self.assertRaises(ValueError) as cm:
            self.mock_wallet_instance._is_valid_address.side_effect = [True, False]
            self.manager._build_transaction(
                from_address="invalid",
                to_address="0x7e4dd6856aa001b78f1f2fe1a4a1f0e5b2cce5f7",
                value_ether=1.0
            )
        self.assertIn("Invalid sender address", str(cm.exception))
    def test_build_transaction_negative_amount(self):
        with self.assertRaises(ValueError) as cm:
            self.manager._build_transaction(
                from_address="0x1234567890123456789012345678901234567890",
                to_address="0x0987654321098765432109876543210987654321",
                value_ether=-1.0
            )
        self.assertIn("Amount must be positive", str(cm.exception))

    def test_build_transaction_insufficient_balance(self):
        self.mock_rpc_instance.get_balance.return_value = 500000000000000000  # 0.5 ETH in wei
        with self.assertRaises(ValueError) as cm:
            self.manager._build_transaction(
                from_address="0x1234567890123456789012345678901234567890",
                to_address="0x0987654321098765432109876543210987654321",
                value_ether=1.0
            )
        self.assertIn("Insufficient balance", str(cm.exception))


    def test_build_transaction_nonce_failure(self):
        self.mock_rpc_instance.get_nonce.side_effect = ValueError("Nonce error")
        with self.assertRaises(ValueError) as cm:
            self.manager._build_transaction(
                from_address="0x1234567890123456789012345678901234567890",
                to_address="0x0987654321098765432109876543210987654321",
                value_ether=1.0
            )
        self.assertIn("Failed to fetch nonce after retries", str(cm.exception))

    def test_build_transaction_gas_estimation_failure(self):
        self.mock_rpc_instance.estimate_gas.side_effect = ValueError("Gas estimation error")
        tx = self.manager._build_transaction(
            from_address="0x1234567890123456789012345678901234567890",
            to_address="0x0987654321098765432109876543210987654321",
            value_ether=1.0
        )
        self.assertEqual(tx['gas'], 21000)  # Fallback to default gas limit

    def test_sign_transaction_success(self):
        transaction = {
            'nonce': 5,
            'to': "0x0987654321098765432109876543210987654321",
            'value': 1000000000000000000,  # 1 ETH in wei
            'gas': 21000,
            'gasPrice': 1000000000,  # 1 Gwei
            'chainId': 11155111,
            'data': b''
        }
        private_key = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        with patch('src.transaction.Account') as mock_account:
            mock_account.from_key.return_value.address = "0x1234567890123456789012345678901234567890"
            mock_account.sign_transaction.return_value = MagicMock(v=27, r=123, s=456)
            mock_account.recover_transaction.return_value = "0x1234567890123456789012345678901234567890"
            signed_tx = self.manager._sign_transaction(transaction, private_key)
            self.assertTrue(isinstance(signed_tx, bytes))
            self.assertTrue(len(signed_tx) > 0)

    def test_sign_transaction_invalid_private_key(self):
        transaction = {
            'nonce': 5,
            'to': "0x0987654321098765432109876543210987654321",
            'value': 1000000000000000000,
            'gas': 21000,
            'gasPrice': 1000000000,
            'chainId': 11155111,
            'data': b''
        }
        with self.assertRaises(ValueError) as cm:
            self.manager._sign_transaction(transaction, "invalid_key")
        self.assertIn("Invalid private key format", str(cm.exception))

    def test_sign_transaction_missing_field(self):
        transaction = {
            'nonce': 5,
            'to': "0x0987654321098765432109876543210987654321",
            'value': 1000000000000000000,
            'gas': 21000,
            # Missing gasPrice
            'chainId': 11155111,
            'data': b''
        }
        with self.assertRaises(ValueError) as cm:
            self.manager._sign_transaction(transaction, "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
        self.assertIn("Missing transaction field", str(cm.exception))

    def test_sign_transaction_signature_verification_failure(self):
        transaction = {
            'nonce': 5,
            'to': "0x0987654321098765432109876543210987654321",
            'value': 1000000000000000000,
            'gas': 21000,
            'gasPrice': 1000000000,
            'chainId': 11155111,
            'data': b''
        }
        with patch('src.transaction.Account') as mock_account:
            mock_account.from_key.return_value.address = "0x1234567890123456789012345678901234567890"
            mock_account.sign_transaction.return_value = MagicMock(v=27, r=123, s=456)
            mock_account.recover_transaction.return_value = "0x0987654321098765432109876543210987654321"  # Wrong address
            with self.assertRaises(ValueError) as cm:
                self.manager._sign_transaction(transaction, "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
            self.assertIn("Signature verification failed", str(cm.exception))

    def test_send_transaction_success(self):
        tx_hash = self.manager.send_transaction(
            from_address="0x1234567890123456789012345678901234567890",
            to_address="0x0987654321098765432109876543210987654321",
            value_ether=1.0,
            password="password"
        )
        self.assertEqual(tx_hash, "0x" + "1" * 64)

    def test_send_transaction_invalid_wallet(self):
        self.mock_wallet_instance.get_wallet_info.return_value = {
            'private_key_available': False,
            'decryption_error': "Invalid password"
        }
        with self.assertRaises(ValueError) as cm:
            self.manager.send_transaction(
                from_address="0x1234567890123456789012345678901234567890",
                to_address="0x0987654321098765432109876543210987654321",
                value_ether=1.0,
                password="wrong_password"
            )
        self.assertIn("Invalid password", str(cm.exception))

    def test_send_transaction_network_failure(self):
        self.mock_rpc_instance.send_raw_transaction.side_effect = ValueError("Network error")
        with self.assertRaises(ValueError) as cm:
            self.manager.send_transaction(
                from_address="0x1234567890123456789012345678901234567890",
                to_address="0x0987654321098765432109876543210987654321",
                value_ether=1.0,
                password="password"
            )
        self.assertIn("Network error", str(cm.exception))

    def test_check_transaction_status_success(self):
        status = self.manager.check_transaction_status("0x" + "1" * 64)
        self.assertEqual(status, {
            'status': 'success',
            'message': 'Confirmed in block 291',
            'gas_used': 21000,
            'block_number': 291
        })

    def test_check_transaction_status_failure(self):
        self.mock_rpc_instance.get_transaction_status.side_effect = ValueError("Invalid hash")
        with self.assertRaises(ValueError) as cm:
            self.manager.check_transaction_status("0x" + "1" * 64)
        self.assertIn("Failed to check transaction status", str(cm.exception))

    def test_get_transaction_history_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "1",
            "message": "OK",
            "result": [
                {
                    "hash": "0x" + "1" * 64,
                    "from": "0x1234567890123456789012345678901234567890",
                    "to": "0x0987654321098765432109876543210987654321",
                    "value": "1000000000000000000",  # 1 ETH
                    "gasUsed": "21000",
                    "gasPrice": "1000000000",  # 1 Gwei
                    "blockNumber": "291"
                }
            ]
        }
        self.mock_requests_get.return_value = mock_response
        history = self.manager.get_transaction_history("0x1234567890123456789012345678901234567890")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0], {
            'hash': "0x" + "1" * 64,
            'from': "0x1234567890123456789012345678901234567890",
            'to': "0x0987654321098765432109876543210987654321",
            'value': 1.0,
            'gas': 21000,
            'gasPrice': 1000000000,
            'blockNumber': 291
        })

    def test_get_transaction_history_invalid_address(self):
        self.mock_wallet_instance._is_valid_address.return_value = False
        with self.assertRaises(ValueError) as cm:
            self.manager.get_transaction_history("invalid_address")
        self.assertIn("Invalid address", str(cm.exception))

    def test_get_transaction_history_no_api_key(self):

        if "ETHERSCAN_API_KEY" in os.environ:
            del os.environ["ETHERSCAN_API_KEY"]
        if "RPC_URL" in os.environ:
            del os.environ["RPC_URL"]

        with open(self.settings_file, 'w') as f:
            json.dump({
                "network": {"name": "Sepolia Testnet", "chain_id": 11155111, "rpc_url": "https://mock-rpc-url"},
                "wallet": {"storage_path": str(self.test_base_dir / 'test_wallet'), "default_wallet": ""},
                "transaction": {"default_gas_limit": 21000, "max_gas_price_gwei": 100, "default_gas_price_gwei": 1.0}
            }, f, indent=4)

        with self.assertRaises(ValueError) as cm:
            TransactionManager().get_transaction_history("0x1234567890123456789012345678901234567890")

        self.assertIn("Etherscan API key not configured", str(cm.exception))

    def test_get_transaction_history_api_failure(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "0", "message": "API error", "result": "Error"}
        self.mock_requests_get.return_value = mock_response
        with self.assertRaises(ValueError) as cm:
            self.manager.get_transaction_history("0x1234567890123456789012345678901234567890")
        self.assertIn("Etherscan API error", str(cm.exception))

    def test_get_transaction_history_network_failure(self):
        self.mock_requests_get.side_effect = requests.RequestException("Network error")
        with self.assertRaises(ValueError) as cm:
            self.manager.get_transaction_history("0x1234567890123456789012345678901234567890")
        self.assertIn("Failed to fetch transaction history after retries", str(cm.exception))

    def test_export_transaction_history_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "1",
            "message": "OK",
            "result": [
                {
                    "hash": "0x" + "1" * 64,
                    "from": "0x1234567890123456789012345678901234567890",
                    "to": "0x0987654321098765432109876543210987654321",
                    "value": "1000000000000000000",
                    "gasUsed": "21000",
                    "gasPrice": "1000000000",
                    "blockNumber": "291"
                }
            ]
        }
        self.mock_requests_get.return_value = mock_response
        output_file = "test_export.json"
        self.manager.export_transaction_history("0x1234567890123456789012345678901234567890", output_file)
        output_path = self.test_export_dir / output_file
        self.assertTrue(output_path.exists())
        with open(output_path, 'r') as f:
            exported_data = json.load(f)
        self.assertEqual(len(exported_data), 1)
        self.assertEqual(exported_data[0]['hash'], "0x" + "1" * 64)

    def test_export_transaction_history_failure(self):
        self.mock_requests_get.side_effect = ValueError("API error")
        with self.assertRaises(ValueError) as cm:
            self.manager.export_transaction_history("0x1234567890123456789012345678901234567890")
        self.assertIn("API error", str(cm.exception))

    def test_close(self):
        self.manager.close()
        self.mock_rpc_instance.close.assert_called_once()

    def test_transaction_send_success(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            transaction_send(
                to_address="0x0987654321098765432109876543210987654321",
                amount=1.0,
                password="password",
                from_address="0x1234567890123456789012345678901234567890"
            )
            output = fake_out.getvalue()
            self.assertIn("Transaction sent successfully!", output)
            self.assertIn("0x" + "1" * 64, output)
            self.assertIn("https://sepolia.etherscan.io/tx/0x" + "1" * 64, output)

    def test_transaction_send_no_default_wallet(self):
        self.mock_wallet_instance.get_default_wallet.return_value = None
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with self.assertRaises(SystemExit):
                transaction_send(
                    to_address="0x0987654321098765432109876543210987654321",
                    amount=1.0,
                    password="password"
                )
            self.assertIn("No default wallet set", fake_out.getvalue())

    def test_transaction_send_negative_amount(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with self.assertRaises(SystemExit):
                transaction_send(
                    to_address="0x0987654321098765432109876543210987654321",
                    amount=-1.0,
                    password="password",
                    from_address="0x1234567890123456789012345678901234567890"
                )
            self.assertIn("Amount must be positive", fake_out.getvalue())

    def test_transaction_send_failure(self):
        self.mock_rpc_instance.send_raw_transaction.side_effect = ValueError("Network error")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with self.assertRaises(SystemExit):
                transaction_send(
                    to_address="0x0987654321098765432109876543210987654321",
                    amount=1.0,
                    password="password",
                    from_address="0x1234567890123456789012345678901234567890"
                )
            self.assertIn("Error: Network error", fake_out.getvalue())

    def test_transaction_status_success(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            transaction_status("0x" + "1" * 64)
            output = fake_out.getvalue()
            self.assertIn("Transaction Hash: 0x" + "1" * 64, output)
            self.assertIn("Status: success", output)
            self.assertIn("Message: Confirmed in block 291", output)
            self.assertIn("Gas Used: 21,000", output)
            self.assertIn("Block Number: 291", output)

    def test_transaction_status_failure(self):
        self.mock_rpc_instance.get_transaction_status.side_effect = ValueError("Invalid hash")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with self.assertRaises(SystemExit):
                transaction_status("0x" + "1" * 64)
            self.assertIn("Error: Failed to check transaction status", fake_out.getvalue())

    def test_transaction_history_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "1",
            "message": "OK",
            "result": [
                {
                    "hash": "0x" + "1" * 64,
                    "from": "0x1234567890123456789012345678901234567890",
                    "to": "0x0987654321098765432109876543210987654321",
                    "value": "1000000000000000000",
                    "gasUsed": "21000",
                    "gasPrice": "1000000000",
                    "blockNumber": "291"
                }
            ]
        }
        self.mock_requests_get.return_value = mock_response
        with patch('sys.stdout', new=StringIO()) as fake_out:
            transaction_history("0x1234567890123456789012345678901234567890")
            output = fake_out.getvalue()
            self.assertIn("Retrieved 1 transactions", output)
            self.assertIn("Hash: 0x" + "1" * 64, output)
            self.assertIn("Value: 1.000000 ETH", output)
            self.assertIn("Gas Used: 21,000", output)
            self.assertIn("Block Number: 291", output)

    def test_transaction_history_no_default_wallet(self):
        self.mock_wallet_instance.get_default_wallet.return_value = None
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with self.assertRaises(SystemExit):
                transaction_history()
            self.assertIn("No default wallet set", fake_out.getvalue())

    def test_transaction_export_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "1",
            "message": "OK",
            "result": [
                {
                    "hash": "0x" + "1" * 64,
                    "from": "0x1234567890123456789012345678901234567890",
                    "to": "0x0987654321098765432109876543210987654321",
                    "value": "1000000000000000000",
                    "gasUsed": "21000",
                    "gasPrice": "1000000000",
                    "blockNumber": "291"
                }
            ]
        }
        self.mock_requests_get.return_value = mock_response
        with patch('sys.stdout', new=StringIO()) as fake_out:
            transaction_export("0x1234567890123456789012345678901234567890", "test_export.json")
            output = fake_out.getvalue()
            self.assertIn("Transaction history exported to", output)
            self.assertIn("test_export.json", output)
        output_path = self.test_export_dir / "test_export.json"
        self.assertTrue(output_path.exists())

    def test_transaction_export_no_default_wallet(self):
        self.mock_wallet_instance.get_default_wallet.return_value = None
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with self.assertRaises(SystemExit):
                transaction_export()
            self.assertIn("No default wallet set", fake_out.getvalue())

if __name__ == '__main__':
    unittest.main()