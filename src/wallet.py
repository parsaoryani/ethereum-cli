import json
import os
import secrets
import hashlib
import time
import base64
from pathlib import Path
from typing import Dict, Tuple, Optional, List, Any
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

        # Generate Ethereum address using Keccak-256 hash
        keccak = hashlib.new('sha3_256')
        keccak.update(public_key_bytes[1:])
        address_bytes = keccak.digest()[-20:]  # Last 20 bytes
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
        # Load wallet data
        wallet_data = self._load_wallet(address)

        # Get balance from RPC client
        from rpc_client import RPCClient
        client = RPCClient()
        try:
            balance_eth = client.get_balance(address, 'ether')
            balance_wei = client.get_balance(address, 'wei')
        finally:
            client.close()

        # Prepare wallet info
        wallet_info = {
            'address': address,
            'balance': {
                'ether': round(balance_eth, 6),
                'wei': balance_wei,
                'gwei': round(balance_wei / 1_000_000_000, 2)
            },
            'created_at': wallet_data.get('created_at', 'Unknown'),
            'imported': wallet_data.get('imported', False),
            'private_key_available': password is not None
        }

        # Decrypt private key if password provided
        if password:
            try:
                private_key = self._decrypt_private_key(wallet_data, password)
                wallet_info['private_key'] = private_key.hex()
                wallet_info['private_key_available'] = True
            except ValueError:
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
        """
        Set the default wallet address.

        Args:
            address: Ethereum wallet address

        Returns:
            True if successful, False if address not found
        """
        if not self._wallet_file_exists(address):
            return False

        # Update default wallet file
        self.default_wallet_file.write_text(address)

        # Update configuration
        self.config['wallet']['default_wallet'] = address
        with open(CONFIG_PATH, 'w') as f:
            json.dump(self.config, f, indent=2)

        return True

    def get_default_wallet(self) -> Optional[str]:
        """
        Get the default wallet address.

        Returns:
            Default wallet address or None if not set
        """
        try:
            default_address = self.default_wallet_file.read_text().strip()
            if default_address and self._wallet_file_exists(default_address):
                return default_address
        except (FileNotFoundError, ValueError):
            pass

        return None

    def _private_key_to_address(self, private_key_bytes: bytes) -> str:
        """
        Derive Ethereum address from private key bytes.

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

        # Keccak-256 hash of public key (excluding 04 prefix)
        keccak = hashlib.new('sha3_256')
        keccak.update(public_key_bytes[1:])
        address_bytes = keccak.digest()[-20:]  # Last 20 bytes

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

