
# Ethereum CLI (Sepolia Testnet)

A command-line interface (CLI) for interacting with the Ethereum Sepolia testnet.  
This tool enables users to manage Ethereum wallets, query account balances, send ETH transactions, and retrieve transaction history in a secure and modular way.

---

## 📖 Overview

The Ethereum CLI is built for developers and blockchain enthusiasts to perform essential Ethereum operations on the Sepolia testnet.  

It uses:
- **Direct JSON-RPC calls** for network interactions  
- **Encrypted wallet storage** for security  
- **Etherscan API** for efficient transaction history retrieval  

### ✨ Key Features
- Wallet management (generate, import, list, use, show)  
- Balance checking  
- Sending ETH transactions  
- Exporting transaction history to JSON  

---

## ⚙️ Prerequisites

- **Python**: Version 3.8 or higher  
- **Virtual Environment**: Recommended for dependency isolation  
- **Network Access**: A valid Sepolia RPC endpoint (e.g., Infura, Alchemy, or GetBlock)  
- **Etherscan API key**  
- **Dependencies**: Listed in `requirements.txt`  
- **Operating System**: macOS, Linux, or Windows (WSL recommended for Windows)  

---

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ethereum-cli.git
   cd ethereum-cli

2. **Set up a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure network settings**
   Create or edit `config/settings.json` in the project root:

   ```json
   {
     "network": {
       "name": "Sepolia Testnet",
       "chain_id": 11155111,
       "rpc_url": "https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID",
       "currency_symbol": "ETH",
       "block_explorer": "https://sepolia.etherscan.io"
     },
     "wallet": {
       "storage_path": "./wallets/",
       "default_wallet": ""
     },
     "transaction": {
       "default_gas_limit": 21000,
       "max_gas_price_gwei": 100,
       "default_gas_price_gwei": 1.0,
       "etherscan_api_key": "YOUR_ETHERSCAN_API_KEY"
     }
 
   }
   ```

   * Replace `YOUR_INFURA_PROJECT_ID` with your Infura/Alchemy/GetBlock project ID.
   * Replace `YOUR_ETHERSCAN_API_KEY` with a valid Etherscan API key (from [etherscan.io](https://etherscan.io)).

5. **Make the CLI executable**

   ```bash
   chmod +x cli
   ```

---

## 🛠️ Usage

Run `./cli --help` for a full command reference.

### 🔑 Wallet Management

**Generate a new wallet**

```bash
./cli wallet generate --password "your_secure_password"
```

Example output:

```
Wallet generated successfully!
Address: 0x...
Saved to: wallets/0x....json
```

**Import an existing wallet**

```bash
./cli wallet import --private-key "0xYourPrivateKey" --password "your_secure_password"
```

**Show wallet information**

```bash
./cli wallet show [--address 0xYourAddress] [--password "your_secure_password"]
```

**List all wallets**

```bash
./cli wallet list
```

**Set default wallet**

```bash
./cli wallet use --address 0xYourAddress
```

---

### 💰 Balance Queries

**Check balance**

```bash
./cli balance [--address 0xYourAddress]
```

Example output:

```
Address: 0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b
Balance: 0.109895 ETH
Balance: 109,895,123,456,789,123 Wei
```

---

### 🔗 Transaction Operations

**Send ETH**

```bash
./cli send --to 0xRecipientAddress --amount 0.01 --password "your_secure_password" [--from 0xSenderAddress]
```

**Check transaction status**

```bash
./cli tx status --hash 0xYourTransactionHash
```

**Show transaction history**

```bash
./cli tx history [--address 0xYourAddress]
```

**Export transaction history**

```bash
./cli tx export [--address 0xYourAddress] [--output custom_filename.json]
```

---

## 📂 Project Structure

```
ethereum-cli/
├── src/
│   ├── wallet.py         # Wallet creation, import, and storage
│   ├── transaction.py    # Transaction handling
│   ├── rpc_client.py     # JSON-RPC interactions
│   └── main.py           # CLI command parsing
├── config/               # Configuration files
├── wallets/              # Encrypted wallet JSON files
├── exports/              # Exported transaction history JSON files
├── tests/                # Unit tests
└── cli                   # Executable CLI entry point
```

---
Got it 👍 You don’t need to copy all those details into your README.
Here’s a **short and clear section** you can add so contributors know how to run tests:

## 🧪 Running Tests

Tests are located in the `tests/` directory and use Python's built-in **unittest** framework.

### Run all tests
````
python -m unittest discover -s tests -v
````

### Run a specific test file

```bash
python -m unittest tests.test_wallet -v
```

### Run a specific test case

```bash
python -m unittest tests.test_wallet.TestWalletManager.test_set_default_wallet_success -v
```

> ⚠️ Note: Tests create and use files inside `tests/test_config/` and `tests/test_wallet/`.
> Your main config files (e.g., `config/settings.json`, `wallets/default.txt`) will be backed up and restored automatically.




---

## 📚 Additional Documentation

* **API.md** → Detailed CLI command reference
* **ARCHITECTURE.md** → Design decisions and architecture
* **DEMO.md** → Sample outputs and demo instructions (optional)

---

## ⚠️ Notes

* This CLI is for the **Sepolia testnet only** (not mainnet).
* Ensure a **stable RPC endpoint** to avoid connection errors.
* Use **strong passwords** for wallet encryption.
* For issues with Infura, try providers like **Alchemy** or **GetBlock**.

---

## 📬 Contact

For issues, feature requests, or contributions, please open an issue on the GitHub repository.
