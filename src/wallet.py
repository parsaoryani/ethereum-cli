import json
import os
import secrets
import time
import base64
from pathlib import Path
from typing import Dict, Tuple, Optional, List, Any

from _pysha3 import keccak_256
from ecdsa import SigningKey, SECP256k1
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# Wallet storage configuration
WALLET_DIR = Path(__file__).parent.parent / 'wallets'
DEFAULT_WALLET_FILE = WALLET_DIR / 'default.txt'
CONFIG_PATH = Path(__file__).parent.parent / 'config' / 'settings.json'




class WalletManager:
    """
    Manages Ethereum wallet operations including key generation,
    secure storage, and wallet management.

    Provides secure encryption of private keys using Fernet symmetric encryption
    with PBKDF2 key derivation from user passwords.
    """

    def __init__(self):
        """
        Initialize WalletManager.

        Creates necessary directories and loads configuration.
        """
        # Load configuration
        with open(CONFIG_PATH, 'r') as f:
            self.config = json.load(f)

        # Wallet storage settings
        self.wallet_dir = WALLET_DIR
        self.default_wallet_file = DEFAULT_WALLET_FILE

        # Ensure default wallet file exists
        if not self.default_wallet_file.exists():
            self.default_wallet_file.write_text('')

    def generate_wallet(self, password: str) -> Dict[str, str]:
        """
        Generate a new Ethereum wallet.

        Args:
            password: Password for encrypting the private key

        Returns:
            Dictionary containing address and encrypted wallet data

        Raises:
            ValueError: If password is too weak
        """
        # Validate password strength
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        # Generate 32-byte random private key
        private_key_bytes = secrets.token_bytes(32)

        # Create signing key from private key bytes
        signing_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)

        # Get verifying key (public key)
        verifying_key = signing_key.verifying_key

        # Get uncompressed public key (04 + x + y coordinates)
        public_key_bytes = b'\x04' + verifying_key.to_string()

        # Generate Ethereum address using Keccak-256 hash (CORRECT)
        hash_result = keccak_256(public_key_bytes[1:]).digest()
        address_bytes = hash_result[-20:]  # Last 20 bytes
        address = '0x' + address_bytes.hex()

        # Encrypt private key with password
        encrypted_data = self._encrypt_private_key(private_key_bytes, password)

        # Create wallet metadata
        wallet_data = {
            'address': address,
            'salt': encrypted_data['salt'].hex(),
            'encrypted_private_key': encrypted_data['encrypted_key'].hex(),
            'created_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        }

        # Save wallet to secure file
        self._save_wallet(address, wallet_data)

        # Set as default wallet if none exists
        if not self.get_default_wallet():
            self.set_default_wallet(address)

        return {
            'address': address,
            'message': 'Wallet generated successfully. Save your password securely!'
        }

    def import_wallet(self, private_key_hex: str, password: str) -> Dict[str, str]:
        """
        Import an existing wallet from private key.

        Args:
            private_key_hex: 64-character hexadecimal private key
            password: Password for encrypting the private key

        Returns:
            Dictionary with import status and address

        Raises:
            ValueError: Invalid private key format or weak password
        """
        # Validate private key format
        if len(private_key_hex) != 64 or not all(c in '0123456789abcdefABCDEF' for c in private_key_hex):
            raise ValueError("Private key must be 64 hexadecimal characters")

        # Convert hex to bytes
        try:
            private_key_bytes = bytes.fromhex(private_key_hex)
        except ValueError:
            raise ValueError("Invalid private key format")

        # Validate password
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        # Derive address from private key
        address = self._private_key_to_address(private_key_bytes)

        # Check if wallet already exists
        if self._wallet_file_exists(address):
            raise ValueError(f"Wallet with address {address} already exists")

        # Encrypt private key
        encrypted_data = self._encrypt_private_key(private_key_bytes, password)

        # Create wallet metadata
        wallet_data = {
            'address': address,
            'salt': encrypted_data['salt'].hex(),
            'encrypted_private_key': encrypted_data['encrypted_key'].hex(),
            'created_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'imported': True
        }

        # Save wallet
        self._save_wallet(address, wallet_data)

        return {
            'address': address,
            'message': 'Wallet imported successfully. Save your password securely!'
        }

    def get_wallet_info(self, address: str, password: Optional[str] = None) -> Dict[str, Any]:
        """
        Get wallet information including balance and metadata.

        Args:
            address: Ethereum wallet address
            password: Password to decrypt private key (optional)

        Returns:
            Dictionary with wallet information and balance

        Raises:
            FileNotFoundError: Wallet file not found
            ValueError: Invalid password or corrupted data
        """
        # Load wallet metadata from secure JSON file
        wallet_data = self._load_wallet(address)

        # Get current balance from Ethereum network using RPC client
        from src.rpc_client import RPCClient
        client = RPCClient()
        try:
            # Get balance in different units
            balance_eth = client.get_balance(address, 'ether')  # Human readable
            balance_wei = client.get_balance(address, 'wei')  # Smallest unit
        finally:
            client.close()  # Always close RPC connection

        # Prepare base wallet information structure
        wallet_info = {
            'address': address,
            'balance': {
                'ether': round(balance_eth, 6),  # 6 decimal places for display
                'wei': balance_wei,  # Raw wei value
                'gwei': round(balance_wei / 1_000_000_000, 2)  # Gwei for gas calculations
            },
            'created_at': wallet_data.get('created_at', 'Unknown'),  # Creation timestamp
            'imported': wallet_data.get('imported', False),  # Generated vs imported
            'private_key_available': password is not None  # Whether private key can be decrypted
        }

        # Attempt to decrypt private key if password provided
        if password:
            try:
                # Decrypt private key using provided password
                private_key = self._decrypt_private_key(wallet_data, password)
                wallet_info['private_key'] = private_key.hex()  # Return as hex string
                wallet_info['private_key_available'] = True
            except ValueError:
                # Invalid password or corrupted data
                wallet_info['private_key_available'] = False
                wallet_info['decryption_error'] = "Invalid password"

        return wallet_info

    def list_wallets(self) -> List[Dict[str, str]]:
        """
        List all available wallets with basic information.

        Returns:
            List of wallet dictionaries with address and creation date
        """
        wallets = []

        # Scan wallet directory
        for wallet_file in self.wallet_dir.glob('*.json'):
            try:
                address = wallet_file.stem  # Filename without .json
                if self._is_valid_address(address):
                    wallet_data = self._load_wallet(address)
                    wallets.append({
                        'address': address,
                        'created_at': wallet_data.get('created_at', 'Unknown'),
                        'imported': wallet_data.get('imported', False)
                    })
            except (json.JSONDecodeError, KeyError):
                # Skip corrupted files
                continue

        # Sort by creation date
        wallets.sort(key=lambda x: x['created_at'], reverse=True)
        return wallets

    def set_default_wallet(self, address: str) -> bool:
        if not self._is_valid_address(address):
            raise ValueError("Invalid address")
        if not self._wallet_file_exists(address):
            raise FileNotFoundError(f"Wallet file not found for address: {address}")
        self.default_wallet_file.write_text(address)
        self.config['wallet']['default_wallet'] = address
        with open(CONFIG_PATH, 'w') as f:
            json.dump(self.config, f, indent=2)
        return True

    def get_default_wallet(self) -> Optional[str]:
        """
        Get the default wallet address.

        Returns:
            Default wallet address if set.

        Raises:
            ValueError: If no default wallet is set or the wallet file does not exist.
        """
        try:
            default_address = self.default_wallet_file.read_text().strip()
            if default_address and self._wallet_file_exists(default_address):
                return default_address
            raise ValueError("No default wallet set")
        except (FileNotFoundError, ValueError):
            raise ValueError("No default wallet set")


    def _private_key_to_address(self, private_key_bytes: bytes) -> str:
        """
        Derive Ethereum address from private key bytes using correct Keccak-256.

        Args:
            private_key_bytes: 32-byte private key

        Returns:
            40-character hexadecimal Ethereum address
        """
        # Create signing key
        signing_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
        verifying_key = signing_key.verifying_key

        # Get uncompressed public key
        public_key_bytes = b'\x04' + verifying_key.to_string()

        # Keccak-256 hash (CORRECT implementation)
        hash_result = keccak_256(public_key_bytes[1:]).digest()  # 32 bytes
        address_bytes = hash_result[-20:]  # Last 20 bytes (160 bits)

        return '0x' + address_bytes.hex()

    def _is_valid_address(self, address: str) -> bool:
        """
        Validate Ethereum address format.

        Args:
            address: Address to validate

        Returns:
            True if valid Ethereum address format
        """
        return (address.startswith('0x') and
                len(address) == 42 and
                all(c in '0123456789abcdefABCDEF' for c in address[2:]))

    def _wallet_file_exists(self, address: str) -> bool:
        """
        Check if wallet file exists for given address.

        Args:
            address: Ethereum address

        Returns:
            True if wallet file exists
        """
        wallet_file = self.wallet_dir / f"{address}.json"
        return wallet_file.exists()

    def _save_wallet(self, address: str, wallet_data: Dict[str, Any]) -> None:
        """
        Save wallet data to secure JSON file.

        Args:
            address: Ethereum address
            wallet_data: Dictionary containing wallet metadata
        """
        wallet_file = self.wallet_dir / f"{address}.json"

        # Ensure file permissions are secure (owner read/write only)
        wallet_file.write_text(json.dumps(wallet_data, indent=2))
        os.chmod(wallet_file, 0o600)  # Owner read/write only

    def _load_wallet(self, address: str) -> Dict[str, Any]:
        """
        Load wallet data from secure JSON file.

        Args:
            address: Ethereum address

        Returns:
            Wallet metadata dictionary

        Raises:
            FileNotFoundError: Wallet file not found
            json.JSONDecodeError: Corrupted wallet file
        """
        wallet_file = self.wallet_dir / f"{address}.json"

        if not wallet_file.exists():
            raise FileNotFoundError(f"Wallet file not found: {wallet_file}")

        with open(wallet_file, 'r') as f:
            return json.load(f)

    def _encrypt_private_key(self, private_key_bytes: bytes, password: str) -> Dict[str, bytes]:
        """
        Encrypt private key using Fernet symmetric encryption.

        Args:
            private_key_bytes: 32-byte private key
            password: User password

        Returns:
            Dictionary with salt and encrypted key
        """
        # Generate random salt for PBKDF2
        salt = os.urandom(16)

        # Derive encryption key from password using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(password.encode())

        # Generate Fernet key from derived key
        fernet_key = base64.urlsafe_b64encode(key)
        fernet = Fernet(fernet_key)

        # Encrypt private key
        encrypted_key = fernet.encrypt(private_key_bytes)

        return {
            'salt': salt,
            'encrypted_key': encrypted_key
        }

    def _decrypt_private_key(self, wallet_data: Dict[str, Any], password: str) -> bytes:
        """
        Decrypt private key using provided password.

        Args:
            wallet_data: Wallet metadata dictionary
            password: User password

        Returns:
            32-byte decrypted private key

        Raises:
            ValueError: Invalid password or corrupted data
        """
        try:
            # Convert hex strings back to bytes
            salt = bytes.fromhex(wallet_data['salt'])
            encrypted_key = bytes.fromhex(wallet_data['encrypted_private_key'])

            # Derive key from password
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = kdf.derive(password.encode())

            # Generate Fernet key
            fernet_key = base64.urlsafe_b64encode(key)
            fernet = Fernet(fernet_key)

            # Decrypt private key
            private_key_bytes = fernet.decrypt(encrypted_key)

            # Validate decrypted key length
            if len(private_key_bytes) != 32:
                raise ValueError("Decrypted private key has invalid length")

            return private_key_bytes

        except Exception as e:
            raise ValueError("Invalid password or corrupted wallet data")




# CLI Interface for wallet commands
def wallet_generate(password: str) -> None:
    """
    CLI command: Generate new wallet.

    Args:
        password: Password for encryption
    """
    try:
        manager = WalletManager()
        result = manager.generate_wallet(password)
        print(f"Wallet Address: {result['address']}")
        print("IMPORTANT: Write down your password and keep it secure!")
        print("You will need it to access your funds.")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)


def wallet_import(private_key: str, password: str) -> None:
    """
    CLI command: Import existing wallet.

    Args:
        private_key: Private key to import
        password: Password for encryption
    """
    try:
        manager = WalletManager()
        result = manager.import_wallet(private_key, password)
        print(f"Imported Wallet: {result['address']}")
        print("IMPORTANT: Write down your password and keep it secure!")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)


def wallet_show(address: Optional[str] = None, password: Optional[str] = None) -> None:
    """
    CLI command: Show wallet information.

    Args:
        address: Specific wallet address (optional)
        password: Password for private key access (optional)
    """
    try:
        manager = WalletManager()

        # Use default wallet if no address specified
        if not address:
            address = manager.get_default_wallet()
            if not address:
                print("No default wallet set. Use 'wallet list' to see available wallets.")
                exit(1)

        # Get wallet info
        wallet_info = manager.get_wallet_info(address, password)

        print(f"Wallet Address: {wallet_info['address']}")
        print(f"Balance: {wallet_info['balance']['ether']:.6f} ETH")
        print(f"Created: {wallet_info['created_at']}")
        print(f"Imported: {wallet_info['imported']}")

        if wallet_info.get('private_key_available', False):
            print(f"Private Key: {wallet_info['private_key'][:10]}...")
        else:
            print("Private Key: [Enter password to view]")

    except Exception as e:
        print(f"Error: {e}")
        exit(1)


def wallet_list() -> None:
    """
    CLI command: List all available wallets.
    """
    try:
        manager = WalletManager()
        wallets = manager.list_wallets()

        if not wallets:
            print("No wallets found.")
            return

        print(f"Found {len(wallets)} wallet(s):")
        print("-" * 50)
        for wallet in wallets:
            print(f"Address: {wallet['address']}")
            print(f"Created: {wallet['created_at']}")
            print(f"Imported: {wallet['imported']}")
            print()

    except Exception as e:
        print(f"Error: {e}")
        exit(1)


def wallet_use(address: str) -> None:
    """
    CLI command: Set default wallet.

    Args:
        address: Wallet address to set as default
    """
    try:
        manager = WalletManager()
        success = manager.set_default_wallet(address)

        if success:
            print(f"Default wallet set to: {address}")
        else:
            print(f"Wallet not found: {address}")
            exit(1)

    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == '__main__':
    """Run comprehensive tests for all WalletManager methods."""
    print("Wallet Module - Comprehensive Tests")
    print("=" * 50)

    # Test generate_wallet
    print("\nTesting generate_wallet")
    try:
        manager = WalletManager()
        test_password = "testpassword123"
        result = manager.generate_wallet(test_password)
        print(f"Success: Generated wallet address: {result['address']}")
        wallet_file = WALLET_DIR / f"{result['address']}.json"
        print(f"Wallet file created: {wallet_file.exists()}")
        stat = os.stat(wallet_file)
        print(f"File permissions secure: {(stat.st_mode & 0o600) == 0o600}")
        test_address = result['address']
    except Exception as e:
        print(f"Failed: {e}")

    # Test import_wallet
    print("\nTesting import_wallet")
    try:
        manager = WalletManager()
        test_private_key = "cc347ec1f2d4a9e13bcce7016dee94b4a0463a37871e4489c8ea60ab67a0b96d"
        test_password = "Parsa1382@"
        result = manager.import_wallet(test_private_key, test_password)
        print(f"Success: Imported wallet address: {result['address']}")
        wallet_file = WALLET_DIR / f"{result['address']}.json"
        print(f"Wallet file created: {wallet_file.exists()}")
    except Exception as e:
        print(f"Failed: {e}")

    # Test get_wallet_info
    print("\nTesting get_wallet_info")
    try:
        manager = WalletManager()
        default_address = manager.get_default_wallet()
        if default_address:
            info = manager.get_wallet_info(default_address, test_password)
            print(f"Success: Address: {info['address']}")
            print(f"Balance: {info['balance']['ether']:.6f} ETH")
            print(f"Created: {info['created_at']}")
            print(f"Private key available: {info['private_key_available']}")
            if info.get('decryption_error'):
                print(f"Decryption error: {info['decryption_error']}")
        else:
            print("No default wallet found, skipping test")
    except Exception as e:
        print(f"Failed: {e}")

    # Test list_wallets
    print("\nTesting list_wallets")
    try:
        manager = WalletManager()
        wallets = manager.list_wallets()
        print(f"Success: Found {len(wallets)} wallet(s)")
        for i, wallet in enumerate(wallets, 1):
            print(f"  {i}. {wallet['address']}")
            print(f"     Created: {wallet['created_at']}")
            print(f"     Imported: {wallet['imported']}")
    except Exception as e:
        print(f"Failed: {e}")

    # Test set_default_wallet
    print("\nTesting set_default_wallet")
    try:
        manager = WalletManager()
        if test_address and manager.set_default_wallet(test_address):
            print(f"Success: Set default wallet to {test_address}")
            default = manager.get_default_wallet()
            print(f"Default wallet: {default}")
        else:
            print("No test address available or set_default_wallet failed")
    except Exception as e:
        print(f"Failed: {e}")

    # Test get_default_wallet
    print("\nTesting get_default_wallet")
    try:
        manager = WalletManager()
        default = manager.get_default_wallet()
        print(f"Success: Default wallet: {default or 'None'}")
    except Exception as e:
        print(f"Failed: {e}")

    # Test _is_valid_address
    print("\nTesting _is_valid_address")
    try:
        manager = WalletManager()
        test_addresses = [
            ('0x0000000000000000000000000000000000000000', True),
            ('0x742d35Cc6634C0532925a3b8D7C4aE7B6733E6B5', True),
            ('invalid_address', False),
            ('0xshort', False),
            ('0x' + 'g' * 40, False),
            ('0x' + 'a' * 39, False)
        ]
        for addr, expected in test_addresses:
            result = manager._is_valid_address(addr)
            print(f"  {addr[:10]}...: {'Valid' if result else 'Invalid'} (Expected: {expected})")
    except Exception as e:
        print(f"Failed: {e}")

    # Test _private_key_to_address
    print("\nTesting _private_key_to_address")
    try:
        manager = WalletManager()
        test_private_key = bytes.fromhex("1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
        address = manager._private_key_to_address(test_private_key)
        print(f"Success: Derived address: {address}")
        print(f"Address valid: {manager._is_valid_address(address)}")
    except Exception as e:
        print(f"Failed: {e}")

    # Test _encrypt_private_key and _decrypt_private_key
    print("\nTesting _encrypt_private_key and _decrypt_private_key")
    try:
        manager = WalletManager()
        test_private_key = secrets.token_bytes(32)
        test_password = "testpassword123"
        encrypted = manager._encrypt_private_key(test_private_key, test_password)
        print(f"Encryption: Salt length: {len(encrypted['salt'])} bytes")
        print(f"Encryption: Key length: {len(encrypted['encrypted_key'])} bytes")
        wallet_data = {
            'salt': encrypted['salt'].hex(),
            'encrypted_private_key': encrypted['encrypted_key'].hex()
        }
        decrypted = manager._decrypt_private_key(wallet_data, test_password)
        print(f"Decryption: Key length: {len(decrypted)} bytes")
        print(f"Round trip: {decrypted == test_private_key}")
    except Exception as e:
        print(f"Failed: {e}")

    # Test _wallet_file_exists
    print("\nTesting _wallet_file_exists")
    try:
        manager = WalletManager()
        if test_address:
            exists = manager._wallet_file_exists(test_address)
            print(f"Success: Wallet file exists: {exists}")
        else:
            print("No test address available")
    except Exception as e:
        print(f"Failed: {e}")

    # Test _save_wallet
    print("\nTesting _save_wallet")
    try:
        manager = WalletManager()
        test_data = {
            'address': '0x' + '1' * 40,
            'salt': secrets.token_bytes(16).hex(),
            'encrypted_private_key': secrets.token_bytes(32).hex(),
            'created_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        }
        manager._save_wallet(test_data['address'], test_data)
        wallet_file = WALLET_DIR / f"{test_data['address']}.json"
        print(f"Success: File created: {wallet_file.exists()}")
        stat = os.stat(wallet_file)
        print(f"Permissions secure: {(stat.st_mode & 0o600) == 0o600}")
    except Exception as e:
        print(f"Failed: {e}")

    # Test _load_wallet
    print("\nTesting _load_wallet")
    try:
        manager = WalletManager()
        if test_address:
            wallet_data = manager._load_wallet(test_address)
            print(f"Success: Loaded wallet: {wallet_data['address']}")
            print(f"Created at: {wallet_data['created_at']}")
        else:
            print("No test address available")
    except Exception as e:
        print(f"Failed: {e}")

    # Test wallet_generate
    print("\nTesting wallet_generate")
    try:
        wallet_generate("clitestpassword123")
        print("Success: CLI wallet generation completed")
    except Exception as e:
        print(f"Failed: {e}")

    # Test wallet_import
    print("\nTesting wallet_import")
    try:
        test_private_key = "5ab4b4b363db0e5597bb60e33e5a07b34762e1a36ad63e77a947778feb869f74"
        wallet_import(test_private_key, "Parsa1382@")
        print("Success: CLI wallet import completed")
    except Exception as e:
        print(f"Failed: {e}")

    # Test wallet_show
    print("\nTesting wallet_show")
    try:
        wallet_show()
        print("Success: CLI wallet show completed")
    except Exception as e:
        print(f"Failed: {e}")

    # Test wallet_list
    print("\nTesting wallet_list")
    try:
        wallet_list()
        print("Success: CLI wallet list completed")
    except Exception as e:
        print(f"Failed: {e}")

    # Test wallet_use
    print("\nTesting wallet_use")
    try:
        if test_address:
            wallet_use(test_address)
            print("Success: CLI wallet use completed")
        else:
            print("No test address available")
    except Exception as e:
        print(f"Failed: {e}")

    print("\n" + "=" * 50)
    print("All wallet tests completed!")