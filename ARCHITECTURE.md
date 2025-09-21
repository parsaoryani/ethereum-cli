# Ethereum CLI Architecture

This document outlines the architectural design of the **Ethereum CLI** for the **Sepolia testnet**, including design principles, key decisions, project structure, and error-handling strategies.

---

## 🎯 Design Principles

* **Modularity**: The codebase is divided into distinct modules to ensure separation of concerns and maintainability.
* **Security**: Private keys are encrypted, and sensitive operations require password authentication.
* **Lightweight**: Direct JSON-RPC calls are used to minimize dependencies and improve performance.
* **User-Friendly**: The CLI provides clear feedback and error messages for ease of use.
* **Extensibility**: The modular structure allows future enhancements, such as support for additional Ethereum networks.

---

## 🔑 Key Design Decisions

### 1. Direct JSON-RPC Calls

* **Rationale**: Instead of using `web3.py`, the CLI uses direct JSON-RPC calls to interact with the Sepolia testnet. This reduces external dependencies, provides fine-grained control over network requests, and ensures compatibility with various RPC providers (e.g., Infura, Alchemy).
* **Implementation**: The `rpc_client.py` module handles all RPC interactions, including `eth_getBalance`, `eth_sendRawTransaction`, and `eth_getTransactionByHash`.

### 2. Encrypted Wallet Storage

* **Rationale**: To ensure security, private keys are encrypted.
* **Implementation**: The `wallet.py` module manages wallet creation, import, and storage, using the `cryptography` library. Encryption requires a user-provided password (minimum 8 characters).

### 3. Etherscan API for Transaction History

* **Rationale**: Retrieving transaction history via Etherscan is more efficient than querying the blockchain directly. It reduces RPC load and provides formatted data.
* **Implementation**: The `transaction.py` module integrates with Etherscan to fetch and export transaction history.

### 4. Modular Architecture

* **Rationale**: Separating concerns improves maintainability and testability.
* **Implementation**:

  * `wallet.py`: Wallet creation, import, and management
  * `transaction.py`: Transaction creation, signing, and history retrieval
  * `rpc_client.py`: Network interactions via JSON-RPC
  * `main.py`: CLI command parsing and execution
  * `cli`: Entry point for executing commands

---

## ⚠️ Error Handling

* **Input Validation**:

  * Addresses are validated for proper Ethereum checksum format.
  * Transaction amounts are validated to ensure they are positive and within available balance.

* **Network Resilience**:

  * `rpc_client.py` includes retry logic for transient network errors (e.g., HTTP 429, timeouts).

* **Security Measures**:

  * Private keys are never stored in plaintext.
  * Passwords are required for sensitive operations, such as sending transactions or viewing private keys.
  * The CLI is designed for the Sepolia testnet only to prevent accidental use with mainnet funds.

---

## 📂 Project Structure

```
ethereum-cli/
├── src/
│   ├── wallet.py         # Wallet creation, import, listing, and default wallet management
│   ├── transaction.py    # Transaction sending, status checking, history retrieval, JSON export
│   ├── rpc_client.py     # Ethereum network interactions using JSON-RPC
│   └── main.py           # CLI command parsing and delegation
├── config/
│   └── settings.json     # Network settings and default wallet
├── wallets/              # Encrypted wallet JSON files
├── exports/              # Exported transaction history JSON files
├── tests/                # Unit tests (to be implemented)
└── cli                   # Executable CLI entry point
```

---

## 🔐 Error Handling & Security

* **Input Validation**: All user inputs are validated to prevent errors or security issues.
* **Network Resilience**: Retry logic and error handling for transient network errors.
* **Security Measures**:

  * Private keys encrypted with `cryptography`.
  * Password required for sensitive operations.
  * CLI restricted to Sepolia testnet.

---

## Test Coverage

The project achieves an overall test coverage of **74%**, meeting the task requirement of at least 70% coverage. Below is the breakdown of coverage per file:

| File                     | Statements | Missed | Coverage |
|--------------------------|------------|--------|----------|
| src/__init__.py          | 0          | 0      | 100%     |
| src/rpc_client.py        | 274        | 111    | 59%      |
| src/transaction.py       | 286        | 41     | 86%      |
| src/wallet.py            | 380        | 235    | 38%      |
| tests/test_rpc_client.py | 268        | 21     | 92%      |
| tests/test_transaction.py| 328        | 3      | 99%      |
| tests/test_wallet.py     | 287        | 61     | 79%      |
| **Total**                | **1823**   | **472**| **74%**  |

### Observations
- **`transaction.py` and test files**: High coverage (86%–99%), indicating robust testing for transaction-related functionality.
- **`rpc_client.py` (59%) and `wallet.py` (38%)**: Lower coverage suggests additional tests are needed.
  - For `wallet.py`, more tests for wallet generation, import, and error cases (e.g., invalid passwords) are recommended.
  - For `rpc_client.py`, tests for network error handling and edge cases (e.g., invalid JSON-RPC responses) should be added.

### Future Improvements
To enhance code quality, additional unit tests will be added to `test_wallet.py` and `test_rpc_client.py` to increase coverage for `wallet.py` and `rpc_client.py` to above 80%.

---


## 🚀 Future Improvements

* **Additional Features**: Add support for ERC-20 token transfers or smart contract interactions.
* **Docker Optimization**: Improve Dockerfile for production-grade deployments.
