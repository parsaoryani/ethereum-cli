import unittest
import os
import json
from unittest.mock import patch
from src.wallet import WalletManager
from pathlib import Path

class TestWalletManager(unittest.TestCase):
    def setUp(self):
        # Define test directories and files
        self.test_base_dir = Path(__file__).resolve().parent
        self.test_wallet_dir = self.test_base_dir / 'test_wallet'
        self.test_config_dir = self.test_base_dir / 'test_config'
        self.settings_file = self.test_config_dir / 'test_settings.json'
        self.default_file = self.test_wallet_dir / 'test_default.txt'
        self.main_default_file = self.test_base_dir.parent / 'wallets' / 'default.txt'
        self.main_settings_file = self.test_base_dir.parent / 'config' / 'settings.json'

        # Ensure test directories exist
        try:
            os.makedirs(self.test_wallet_dir, exist_ok=True)
            os.makedirs(self.test_config_dir, exist_ok=True)
        except OSError as e:
            self.fail(f"Failed to create test directories: {e}")

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
                    f.seek(0)  # Reset file pointer to read raw content
                    self.original_main_settings_raw = f.read()
        except (OSError, json.JSONDecodeError) as e:
            self.fail(f"Failed to backup main settings.json: {e}")

        # Backup original test_default.txt if it exists
        self.original_default = None
        try:
            if self.default_file.exists():
                with open(self.default_file, 'r') as f:
                    self.original_default = f.read()
        except OSError as e:
            self.fail(f"Failed to backup test_default.txt: {e}")

        # Backup original main default.txt if it exists
        self.original_main_default = None
        try:
            if self.main_default_file.exists():
                with open(self.main_default_file, 'r') as f:
                    self.original_main_default = f.read().strip()
        except OSError as e:
            self.fail(f"Failed to backup main default.txt: {e}")

        # Backup existing wallet files
        self.original_wallet_files = {}
        try:
            for wallet_file in self.test_wallet_dir.glob("*.json"):
                with open(wallet_file, 'r') as f:
                    self.original_wallet_files[str(wallet_file)] = f.read()
        except OSError as e:
            self.fail(f"Failed to backup wallet files: {e}")

        # Create or reset test_settings.json
        try:
            with open(self.settings_file, 'w') as f:
                json.dump({
                    "network": {
                        "name": "Sepolia Testnet",
                        "chain_id": 11155111,
                        "rpc_url": "https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80",
                        "currency_symbol": "ETH",
                        "block_explorer": "https://sepolia.etherscan.io"
                    },
                    "wallet": {
                        "storage_path": str(self.test_wallet_dir),
                        "default_wallet": ""
                    },
                    "transaction": {
                        "default_gas_limit": 21000,
                        "max_gas_price_gwei": 100,
                        "default_gas_price_gwei": 1.0,
                        "etherscan_api_key": "4S5126VMHX7QTAI3WMI3C13SBR8W8K6RWJ"
                    }
                }, f, indent=4)  # Preserve formatting
        except (OSError, json.JSONDecodeError) as e:
            self.fail(f"Failed to create test_settings.json: {e}")

        # Remove test_default.txt to ensure no default wallet
        try:
            if self.default_file.exists():
                os.remove(self.default_file)
        except OSError as e:
            self.fail(f"Failed to remove test_default.txt: {e}")

        # Remove any existing wallet files in test_wallet_dir
        try:
            for wallet_file in self.test_wallet_dir.glob("*.json"):
                os.remove(wallet_file)
        except OSError as e:
            self.fail(f"Failed to remove wallet files: {e}")

        # Patch WALLET_DIR, CONFIG_PATH, and DEFAULT_WALLET_FILE to use test directories
        try:
            self.patcher1 = patch('src.wallet.WALLET_DIR', self.test_wallet_dir)
            self.patcher2 = patch('src.wallet.CONFIG_PATH', self.settings_file)
            self.patcher3 = patch('src.wallet.DEFAULT_WALLET_FILE', self.default_file)
            self.patcher1.start()
            self.patcher2.start()
            self.patcher3.start()
            # Verify patch
            import src.wallet
            self.assertEqual(str(src.wallet.CONFIG_PATH), str(self.settings_file),
                             f"CONFIG_PATH patch failed: expected {self.settings_file}, got {src.wallet.CONFIG_PATH}")
            self.manager = WalletManager()
        except Exception as e:
            self.fail(f"Failed to initialize WalletManager: {e}")

    def tearDown(self):
        # Stop patchers
        try:
            self.patcher1.stop()
            self.patcher2.stop()
            self.patcher3.stop()
        except Exception as e:
            self.fail(f"Failed to stop patchers: {e}")

        # Restore original test_settings.json
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.original_settings, f, indent=4)  # Preserve formatting
        except (OSError, json.JSONDecodeError) as e:
            self.fail(f"Failed to restore test_settings.json: {e}")

        # Restore original main settings.json with original formatting
        try:
            if self.original_main_settings_raw is not None:
                with open(self.main_settings_file, 'w') as f:
                    f.write(self.original_main_settings_raw)
            elif self.main_settings_file.exists():
                os.remove(self.main_settings_file)
        except (OSError, json.JSONDecodeError) as e:
            self.fail(f"Failed to restore main settings.json: {e}")

        # Restore original test_default.txt
        try:
            if self.original_default is not None:
                with open(self.default_file, 'w') as f:
                    f.write(self.original_default)
            elif self.default_file.exists():
                os.remove(self.default_file)
        except OSError as e:
            self.fail(f"Failed to restore test_default.txt: {e}")

        # Restore original main default.txt
        try:
            if self.original_main_default is not None:
                with open(self.main_default_file, 'w') as f:
                    f.write(self.original_main_default)
            elif self.main_default_file.exists():
                os.remove(self.main_default_file)
        except OSError as e:
            self.fail(f"Failed to restore main default.txt: {e}")

        # Restore original wallet files
        try:
            for wallet_file in self.test_wallet_dir.glob("*.json"):
                os.remove(wallet_file)
            for file_path, content in self.original_wallet_files.items():
                with open(file_path, 'w') as f:
                    f.write(content)
        except OSError as e:
            self.fail(f"Failed to restore wallet files: {e}")

        # Verify main settings.json hasn't changed (content and format)
        try:
            if self.main_settings_file.exists():
                with open(self.main_settings_file, 'r') as f:
                    current_main_settings_raw = f.read()
                self.assertEqual(current_main_settings_raw, self.original_main_settings_raw,
                                 f"Main settings.json was modified unexpectedly: {current_main_settings_raw}")
        except (OSError, json.JSONDecodeError) as e:
            self.fail(f"Failed to verify main settings.json: {e}")

    @patch('src.rpc_client.RPCClient')
    def test_generate_wallet_success(self, mock_rpc_client):
        # Mock balance to avoid real RPC calls
        mock_client_instance = mock_rpc_client.return_value
        mock_client_instance.get_balance.side_effect = [
            0.0,  # For 'ether'
            0     # For 'wei'
        ]

        # Test generating a wallet with valid password
        result = self.manager.generate_wallet("Parsa1382@")
        address = result['address'].lower()

        # Verify address format
        self.assertTrue(self.manager._is_valid_address(address),
                        f"Address {address} is not valid")
        self.assertEqual(len(address), 42, f"Address {address} length is not 42")
        self.assertTrue(address.startswith("0x"), f"Address {address} does not start with 0x")

        # Verify wallet file exists
        wallet_file = self.test_wallet_dir / f"{address}.json"
        self.assertTrue(wallet_file.exists(), f"Wallet file {wallet_file} does not exist")

        # Verify wallet file content
        try:
            with open(wallet_file, "r") as f:
                wallet_data = json.load(f)
                self.assertEqual(wallet_data['address'].lower(), address,
                                 f"Wallet address {wallet_data['address']} does not match {address}")
                self.assertIn("salt", wallet_data, "Salt not found in wallet data")
                self.assertIn("encrypted_private_key", wallet_data, "Encrypted private key not found")
                self.assertIn("created_at", wallet_data, "Created_at not found")
                self.assertFalse(wallet_data.get("imported", False), "Wallet marked as imported")
        except (OSError, json.JSONDecodeError) as e:
            self.fail(f"Failed to read wallet file {wallet_file}: {e}")

    def test_generate_wallet_short_password(self):
        # Test generating with short password
        with self.assertRaises(ValueError) as cm:
            self.manager.generate_wallet("short")
        self.assertEqual(str(cm.exception), "Password must be at least 8 characters long")

    @patch('src.rpc_client.RPCClient')
    def test_import_wallet_success(self, mock_rpc_client):
        # Mock balance
        mock_client_instance = mock_rpc_client.return_value
        mock_client_instance.get_balance.side_effect = [
            0.0,  # For 'ether'
            0     # For 'wei'
        ]

        # Test importing with valid private key
        private_key = "cc347ec1f2d4a9e13bcce7016dee94b4a0463a37871e4489c8ea60ab67a0b96d"
        result = self.manager.import_wallet(private_key, "Parsa1382@")
        address = result['address'].lower()

        # Verify address format
        self.assertTrue(self.manager._is_valid_address(address),
                        f"Address {address} is not valid")

        # Verify wallet file
        wallet_file = self.test_wallet_dir / f"{address}.json"
        self.assertTrue(wallet_file.exists(), f"Wallet file {wallet_file} does not exist")

        # Verify wallet file content
        try:
            with open(wallet_file, "r") as f:
                wallet_data = json.load(f)
                self.assertTrue(wallet_data.get("imported", False), "Wallet not marked as imported")
        except (OSError, json.JSONDecodeError) as e:
            self.fail(f"Failed to read wallet file {wallet_file}: {e}")

    def test_import_wallet_invalid_key(self):
        # Test importing with invalid private key
        with self.assertRaises(ValueError) as cm:
            self.manager.import_wallet("invalid_key", "Parsa1382@")
        self.assertEqual(str(cm.exception), "Private key must be 64 hexadecimal characters")

    def test_import_wallet_short_password(self):
        # Test importing with short password
        private_key = "cc347ec1f2d4a9e13bcce7016dee94b4a0463a37871e4489c8ea60ab67a0b96d"
        with self.assertRaises(ValueError) as cm:
            self.manager.import_wallet(private_key, "short")
        self.assertEqual(str(cm.exception), "Password must be at least 8 characters long")

    @patch('src.rpc_client.RPCClient')
    def test_get_wallet_info_success(self, mock_rpc_client):
        # Mock balance to handle multiple get_balance calls
        mock_client_instance = mock_rpc_client.return_value
        mock_client_instance.get_balance.side_effect = [
            0.109895, 109895000000000000,  # For first get_wallet_info (with password)
            0.109895, 109895000000000000  # For second get_wallet_info (without password)
        ]

        # Set up a default wallet to avoid "No default wallet set" error
        default_wallet = self.manager.import_wallet(
            "cc347ec1f2d4a9e13bcce7016dee94b4a0463a37871e4489c8ea60ab67a0b96d",
            "Parsa1382@"
        )
        default_address = default_wallet['address'].lower()
        self.assertEqual(default_address, "0x7e4dd6856aa001b78f1f2fe1a4a1f0e5b2cce5f7",
                         f"Default wallet address is not 0x7e4dd6856aa001b78f1f2fe1a4a1f0e5b2cce5f7, got {default_address}")
        self.manager.set_default_wallet(default_address)

        # Create a wallet for testing
        result = self.manager.generate_wallet("Parsa1382@")
        address = result['address'].lower()

        # Test getting wallet info with password
        info = self.manager.get_wallet_info(address, "Parsa1382@")
        self.assertEqual(info['address'].lower(), address,
                         f"Wallet address {info['address']} does not match {address}")
        self.assertEqual(info['balance']['ether'], 0.109895,
                         f"Balance ether {info['balance']['ether']} does not match 0.109895")
        self.assertIn('created_at', info, "Created_at not found in wallet info")
        self.assertFalse(info['imported'], "Wallet marked as imported")
        self.assertTrue('private_key' in info, "Private key not found")
        self.assertTrue(info['private_key_available'], "Private key not available")

        # Test without password
        info = self.manager.get_wallet_info(address)
        self.assertEqual(info['address'].lower(), address,
                         f"Wallet address {info['address']} does not match {address}")
        self.assertEqual(info['balance']['ether'], 0.109895,
                         f"Balance ether {info['balance']['ether']} does not match 0.109895")
        self.assertFalse('private_key' in info, "Private key found without password")
        self.assertFalse(info['private_key_available'], "Private key available without password")

    @patch('src.rpc_client.RPCClient')
    def test_get_wallet_info_wrong_password(self, mock_rpc_client):
        # Mock balance
        mock_client_instance = mock_rpc_client.return_value
        mock_client_instance.get_balance.side_effect = [
            0.0,  # For 'ether'
            0     # For 'wei'
        ]

        # Create a wallet
        result = self.manager.generate_wallet("Parsa1382@")
        address = result['address'].lower()

        # Test with wrong password
        info = self.manager.get_wallet_info(address, "WrongPassword")
        self.assertEqual(info['address'].lower(), address,
                         f"Wallet address {info['address']} does not match {address}")
        self.assertFalse(info['private_key_available'], "Private key available with wrong password")
        self.assertEqual(info['decryption_error'], "Invalid password",
                         f"Expected decryption_error 'Invalid password', got {info['decryption_error']}")

    def test_get_wallet_info_nonexistent(self):
        # Test with nonexistent address
        nonexistent_address = "0x0000000000000000000000000000000000000000"
        with self.assertRaises(FileNotFoundError) as cm:
            self.manager.get_wallet_info(nonexistent_address)
        self.assertEqual(str(cm.exception), f"Wallet file not found: {self.test_wallet_dir / f'{nonexistent_address}.json'}")

    @patch('src.rpc_client.RPCClient')
    def test_list_wallets(self, mock_rpc_client):
        # Mock balance
        mock_client_instance = mock_rpc_client.return_value
        mock_client_instance.get_balance.side_effect = [
            0.0, 0,  # For first wallet
            0.0, 0   # For second wallet
        ]

        # Create two wallets
        wallet1 = self.manager.import_wallet(
            "cc347ec1f2d4a9e13bcce7016dee94b4a0463a37871e4489c8ea60ab67a0b96d",
            "Parsa1382@"
        )
        wallet2 = self.manager.import_wallet(
            "5ab4b4b363db0e5597bb60e33e5a07b34762e1a36ad63e77a947778feb869f74",
            "Parsa1382@"
        )

        # Test listing wallets
        wallets = self.manager.list_wallets()
        self.assertEqual(len(wallets), 2, f"Expected 2 wallets, got {len(wallets)}")

        # Extract addresses from wallets list
        wallet_addresses = [wallet['address'].lower() for wallet in wallets]

        # Verify that both wallet addresses are present, regardless of order
        self.assertIn(wallet1['address'].lower(), wallet_addresses,
                      f"Wallet1 address {wallet1['address']} not in {wallet_addresses}")
        self.assertIn(wallet2['address'].lower(), wallet_addresses,
                      f"Wallet2 address {wallet2['address']} not in {wallet_addresses}")

    def test_list_wallets_empty(self):
        # Ensure no wallets exist in the test directory
        try:
            for wallet_file in self.test_wallet_dir.glob("*.json"):
                os.remove(wallet_file)
        except OSError as e:
            self.fail(f"Failed to remove wallet files: {e}")

        # Test listing when no wallets exist
        wallets = self.manager.list_wallets()
        self.assertEqual(len(wallets), 0, f"Expected 0 wallets, got {len(wallets)}")

    @patch('src.rpc_client.RPCClient')
    def test_set_default_wallet_success(self, mock_rpc_client):
        # Mock balance
        mock_client_instance = mock_rpc_client.return_value
        mock_client_instance.get_balance.side_effect = [
            0.0,  # For 'ether'
            0     # For 'wei'
        ]

        # Create a wallet
        wallet = self.manager.import_wallet(
            "cc347ec1f2d4a9e13bcce7016dee94b4a0463a37871e4489c8ea60ab67a0b96d",
            "Parsa1382@"
        )
        address = wallet['address'].lower()

        # Set as default
        success = self.manager.set_default_wallet(address)
        self.assertTrue(success, "set_default_wallet failed to return True")

        # Verify test_default.txt
        for _ in range(10):  # Retry up to 10 times to ensure file is written
            if self.default_file.exists():
                try:
                    with open(self.default_file, 'r') as f:
                        default_address = f.read().strip().lower()
                        self.assertEqual(default_address, address,
                                         f"Expected default_address to be {address}, but got {default_address}")
                        break
                except OSError as e:
                    self.fail(f"Failed to read test_default.txt: {e}")
            import time
            time.sleep(0.01)
        else:
            self.fail(f"Default wallet file {self.default_file} not found after retries")

    def test_set_default_wallet_invalid_address(self):
        # Test with invalid address
        with self.assertRaises(ValueError) as cm:
            self.manager.set_default_wallet("0xInvalid")
        self.assertEqual(str(cm.exception), "Invalid address")

    def test_set_default_wallet_nonexistent(self):
        # Test with nonexistent address
        nonexistent_address = "0x0000000000000000000000000000000000000000"
        with self.assertRaises(FileNotFoundError) as cm:
            self.manager.set_default_wallet(nonexistent_address)
        self.assertEqual(str(cm.exception), f"Wallet file not found for address: {nonexistent_address}")

    @patch('src.rpc_client.RPCClient')
    def test_get_default_wallet(self, mock_rpc_client):
        # Mock balance
        mock_client_instance = mock_rpc_client.return_value
        mock_client_instance.get_balance.side_effect = [
            0.0,  # For 'ether'
            0     # For 'wei'
        ]

        # Create a wallet and set as default
        wallet = self.manager.import_wallet(
            "cc347ec1f2d4a9e13bcce7016dee94b4a0463a37871e4489c8ea60ab67a0b96d",
            "Parsa1382@"
        )
        address = wallet['address'].lower()
        self.manager.set_default_wallet(address)

        # Verify default wallet
        default = self.manager.get_default_wallet()
        self.assertEqual(default.lower(), address,
                         f"Expected default wallet to be {address}, but got {default}")

    def test_is_valid_address(self):
        # Test valid and invalid addresses
        self.assertTrue(self.manager._is_valid_address("0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7"),
                        "Valid address 0x7E4Dd685... failed validation")
        self.assertTrue(self.manager._is_valid_address("0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b"),
                        "Valid address 0xB0b51E4... failed validation")
        self.assertFalse(self.manager._is_valid_address("0xInvalid"), "Invalid address passed validation")
        self.assertFalse(self.manager._is_valid_address("invalid"), "Non-hex address passed validation")

if __name__ == '__main__':
    unittest.main()