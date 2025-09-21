
# Ethereum CLI Command Reference

This document provides a detailed reference for all commands supported by the **Ethereum CLI** for the Sepolia testnet.  
Each command is described with its purpose, arguments, usage examples, and expected outputs.

---

## 📖 Overview

The Ethereum CLI supports:
- Wallet management
- Balance queries
- Transaction operations  

Commands are executed using the `./cli` script, and most commands rely on a configured `.env` file with a valid Sepolia RPC URL (`RPC_URL`) and Etherscan API key (`ETHERSCAN_API_KEY`).

Run:
```bash
./cli --help
````

to see all available commands.

---

## 🔑 Wallet Management Commands

### `wallet generate`

Generate a new Ethereum wallet and store it encrypted.

**Syntax**

```bash
./cli wallet generate --password <password>
```

**Arguments**

* `--password` (required): Password for encrypting the private key (minimum 8 characters).

**Example**

```bash
./cli wallet generate --password "Parsa1382@"
```

**Output**

```
Wallet generated successfully!
Address: 0x...
Saved to: wallets/0x....json
```

**Error Cases**

* Password too short → `Error: Password must be at least 8 characters long`

---

### `wallet import`

Import an existing wallet using a private key.

**Syntax**

```bash
./cli wallet import --private-key <key> --password <password>
```

**Arguments**

* `--private-key` (required): The private key (hex string, with or without 0x prefix).
* `--password` (required): Password for encrypting the private key.

**Example**

```bash
./cli wallet import --private-key "0x37947b..." --password "Parsa1382@"
```

**Output**

```
Wallet imported successfully!
Address: 0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b
Saved to: wallets/0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b.json
```

**Error Cases**

* Invalid private key → `Error: Invalid private key format`
* Password too short → `Error: Password must be at least 8 characters long`

---

### `wallet show`

Display information about a wallet (default or specified).

**Syntax**

```bash
./cli wallet show [--address <address>] [--password <password>]
```

**Arguments**

* `--address` (optional): Wallet address (uses default wallet if not provided).
* `--password` (optional): Required to decrypt and display the private key.

**Example (default wallet)**

```bash
./cli wallet show --password "Parsa1382@"
```

**Output**

```
Wallet Address: 0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b
Balance: 0.109895 ETH
Created: 2025-09-19T12:59:24Z
Imported: True
Private Key: 0x37947b...
```

**Error Cases**

* No default wallet → `No default wallet set. Use './cli wallet use' to set a default wallet.`
* Invalid address → `Error: Invalid address: <address>`
* Wrong password → `Error: Invalid password or corrupted wallet data`

---

### `wallet list`

List all stored wallets.

**Syntax**

```bash
./cli wallet list
```

**Example**

```bash
./cli wallet list
```

**Output**

```
Available wallets:
- 0x7e4dd6856aa001b78f1f2fe1a4a1f0e5b2cce5f7 (Created: 2025-09-19T12:59:24Z)
- 0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b (Created: 2025-09-19T12:59:24Z, Default)
```

---

### `wallet use`

Set a wallet as the default.

**Syntax**

```bash
./cli wallet use --address <address>
```

**Arguments**

* `--address` (required): Wallet address to set as default.

**Example**

```bash
./cli wallet use --address 0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b
```

**Output**

```
Default wallet set to: 0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b
```

---

## 💰 Balance Queries

### `balance`

Check the balance of a wallet.

**Syntax**

```bash
./cli balance [--address <address>]
```

**Arguments**

* `--address` (optional): Wallet address (default wallet if not provided).

**Example**

```bash
./cli balance
```

**Output**

```
Address: 0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b
Balance: 0.109895 ETH
Balance: 109,895,123,456,789,123 Wei
```

---

## 🔗 Transaction Operations

### `send`

Send ETH to an address.

**Syntax**

```bash
./cli send --to <address> --amount <eth_amount> --password <password> [--from <address>]
```

**Arguments**

* `--to` (required): Recipient address
* `--amount` (required): Amount in ETH
* `--password` (required): Sender wallet password
* `--from` (optional): Sender address (uses default if not set)

**Example**

```bash
./cli send --to 0x7e4dd... --amount 0.01 --password "Parsa1382@"
```

**Output**

```
Transaction sent successfully!
Hash: 0x...
Check transaction on Sepolia Etherscan: https://sepolia.etherscan.io/tx/0x...
```

---

### `tx status`

Check the status of a transaction.

**Syntax**

```bash
./cli tx status --hash <tx_hash>
```

**Arguments**

* `--hash` (required): Transaction hash

**Example**

```bash
./cli tx status --hash 0xYourTransactionHash
```

**Output**

```
Transaction Hash: 0x...
Status: success
Message: Confirmed in block 123456
Gas Used: 21000
Block Number: 123456
```

---

### `tx history`

Retrieve transaction history.

**Syntax**

```bash
./cli tx history [--address <address>]
```

**Arguments**

* `--address` (optional): Wallet address (default if not set)

**Example**

```bash
./cli tx history --address 0xb0b51e4...
```

**Output**

```
Retrieved 2 transactions for 0xb0b51e4...:
--------------------------------------------------
Hash: 0x...
From: 0x...
To: 0x...
Value: 0.01 ETH
Gas Used: 21000
Gas Price: 1000000000 wei
Block Number: 123456
--------------------------------------------------
```

---

### `tx export`

Export transaction history to JSON.

**Syntax**

```bash
./cli tx export [--address <address>] [--output <filename>]
```

**Arguments**

* `--address` (optional): Wallet address
* `--output` (optional): Output filename (default: `tx_history_<address>.json`)

**Example**

```bash
./cli tx export --address 0xb0b51e4... --output custom_history.json
```

**Output**

```
Transaction history exported to: exports/custom_history.json
```

---

## ⚠️ Notes

* All commands require a valid **`config/settings.json`** with a Sepolia RPC URL and Etherscan API key.
* Use **strong passwords** for wallet encryption.
* This CLI is for **Sepolia testnet only**. Do not use with mainnet private keys.
