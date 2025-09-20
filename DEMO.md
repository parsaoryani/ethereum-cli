# Ethereum CLI Demonstration

This document shows the output of all CLI commands specified in the task, covering all possible cases.

## Wallet Commands

### 1. Wallet Generate
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli wallet generate --password "Parsa1382@"
```
```output
Wallet Address: 0x03ce7a235d4f49285067962921358d7800e6ce3c
IMPORTANT: Write down your password and keep it secure!
You will need it to access your funds.
```

### 2. Wallet Import (Private Key 1)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli wallet import --private-key "cc347ec1f2d4a9e13bcce7016dee94b4a0463a37871e4489c8ea60ab67a0b96d" --password "Parsa1382@"
```
```output
Error: Wallet with address 0x7e4dd6856aa001b78f1f2fe1a4a1f0e5b2cce5f7 already exists
```

### 3. Wallet Import (Private Key 2)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli wallet import --private-key "93786dc60ed49ef8c1c481910c439b0287aa5172c2c2d82892e8d2a58d0ead8f" --password "Parsa1382@"
```
```output
Imported Wallet: 0xb12c3270cf65489c19efb34b0bd36378234dd343
IMPORTANT: Write down your password and keep it secure!
```

### 4. Wallet Show (Valid Password)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli wallet show --password "Parsa1382@"
```
```output
Wallet Address: 0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b
Balance: 0.058790 ETH
Created: 2025-09-20T12:23:04Z
Imported: True
Private Key: 5ab4b4b363...
2025-09-20 22:54:38,449 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:54:39,389 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:54:39,389 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:54:39,389 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:54:39,389 - INFO - 🔄 Calling eth_getBalance with params: ['0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b', 'latest']
2025-09-20 22:54:40,117 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:54:40,117 - INFO - Raw result for eth_getBalance: 0xd0dd1420654a90
2025-09-20 22:54:40,117 - INFO - 🔄 Calling eth_getBalance with params: ['0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b', 'latest']
2025-09-20 22:54:40,898 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:54:40,898 - INFO - Raw result for eth_getBalance: 0xd0dd1420654a90
2025-09-20 22:54:40,899 - INFO - RPC Client closed
```

### 5. Wallet Show (Invalid Password)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli wallet show --password "wrong_password"
```
```output
Wallet Address: 0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b
Balance: 0.058790 ETH
Created: 2025-09-20T12:23:04Z
Imported: True
Private Key: [Enter password to view]
2025-09-20 22:54:41,285 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:54:42,641 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:54:42,641 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:54:42,641 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:54:42,641 - INFO - 🔄 Calling eth_getBalance with params: ['0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b', 'latest']
2025-09-20 22:54:43,360 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:54:43,360 - INFO - Raw result for eth_getBalance: 0xd0dd1420654a90
2025-09-20 22:54:43,360 - INFO - 🔄 Calling eth_getBalance with params: ['0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b', 'latest']
2025-09-20 22:54:44,083 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:54:44,083 - INFO - Raw result for eth_getBalance: 0xd0dd1420654a90
2025-09-20 22:54:44,084 - INFO - RPC Client closed
```

## Balance Commands

### 6. Balance (Default Wallet)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli balance
```
```output
Address: 0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b
Balance: 0.058790 ETH
Balance: 58,789,873,668,410,000 Wei
2025-09-20 22:54:44,471 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:54:45,540 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:54:45,540 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:54:45,540 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:54:45,540 - INFO - 🔄 Calling eth_getBalance with params: ['0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b', 'latest']
2025-09-20 22:54:46,431 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:54:46,431 - INFO - Raw result for eth_getBalance: 0xd0dd1420654a90
2025-09-20 22:54:46,431 - INFO - 🔄 Calling eth_getBalance with params: ['0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b', 'latest']
2025-09-20 22:54:47,279 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:54:47,280 - INFO - Raw result for eth_getBalance: 0xd0dd1420654a90
2025-09-20 22:54:47,283 - INFO - RPC Client closed
```

### 7. Balance (From Address)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli balance --address "0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b"
```
```output
Address: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Balance: 0.058790 ETH
Balance: 58,789,873,668,410,000 Wei
2025-09-20 22:54:47,634 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:54:48,651 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:54:48,651 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:54:48,651 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:54:48,651 - INFO - 🔄 Calling eth_getBalance with params: ['0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b', 'latest']
2025-09-20 22:54:49,392 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:54:49,393 - INFO - Raw result for eth_getBalance: 0xd0dd1420654a90
2025-09-20 22:54:49,393 - INFO - 🔄 Calling eth_getBalance with params: ['0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b', 'latest']
2025-09-20 22:54:50,130 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:54:50,130 - INFO - Raw result for eth_getBalance: 0xd0dd1420654a90
2025-09-20 22:54:50,133 - INFO - RPC Client closed
```

### 8. Balance (To Address)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli balance --address "0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7"
```
```output
Address: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Balance: 0.241000 ETH
Balance: 240,999,852,016,465,000 Wei
2025-09-20 22:54:50,506 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:54:51,594 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:54:51,595 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:54:51,595 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:54:51,595 - INFO - 🔄 Calling eth_getBalance with params: ['0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7', 'latest']
2025-09-20 22:54:52,534 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:54:52,534 - INFO - Raw result for eth_getBalance: 0x3583416aa5cf468
2025-09-20 22:54:52,534 - INFO - 🔄 Calling eth_getBalance with params: ['0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7', 'latest']
2025-09-20 22:54:53,390 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:54:53,390 - INFO - Raw result for eth_getBalance: 0x3583416aa5cf468
2025-09-20 22:54:53,392 - INFO - RPC Client closed
```

### 9. Balance (Invalid Address)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli balance --address "invalid"
```
```output
Error: Invalid address: invalid
2025-09-20 22:54:53,727 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:54:55,011 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:54:55,011 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:54:55,011 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:54:55,012 - INFO - RPC Client closed
```

## Transaction Commands

### 10. Send Transaction (Valid Amount)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli send --to "0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7" --amount 0.001 --password "Parsa1382@"
```
```output
Transaction sent successfully! Hash: 0x9052cd8f106a52e1680e790be79b86a068085e8358acb15575c73c5b21dd0a14
Check transaction on Sepolia Etherscan: https://sepolia.etherscan.io/tx/0x9052cd8f106a52e1680e790be79b86a068085e8358acb15575c73c5b21dd0a14
2025-09-20 22:54:55,345 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:54:56,123 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:54:56,123 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:54:56,123 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:54:56,124 - INFO - ✅ TransactionManager initialized
2025-09-20 22:54:56,124 - INFO - Attempting to get wallet info for 0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b
2025-09-20 22:54:56,125 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:54:56,968 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:54:56,968 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:54:56,969 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:54:56,969 - INFO - 🔄 Calling eth_getBalance with params: ['0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b', 'latest']
2025-09-20 22:54:57,777 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:54:57,777 - INFO - Raw result for eth_getBalance: 0xd0dd1420654a90
2025-09-20 22:54:57,777 - INFO - 🔄 Calling eth_getBalance with params: ['0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b', 'latest']
2025-09-20 22:54:58,471 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:54:58,471 - INFO - Raw result for eth_getBalance: 0xd0dd1420654a90
2025-09-20 22:54:58,473 - INFO - RPC Client closed
2025-09-20 22:54:58,538 - INFO - Wallet info retrieved: private_key_available=True
2025-09-20 22:54:58,538 - INFO - Building transaction...
2025-09-20 22:54:58,545 - INFO - 🔄 Calling eth_getBalance with params: ['0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b', 'latest']
2025-09-20 22:54:59,006 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:54:59,006 - INFO - Raw result for eth_getBalance: 0xd0dd1420654a90
2025-09-20 22:54:59,006 - INFO - 🔄 Calling eth_getTransactionCount with params: ['0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b', 'pending']
2025-09-20 22:54:59,727 - INFO - ✅ eth_getTransactionCount succeeded
2025-09-20 22:54:59,727 - INFO - Raw result for eth_getTransactionCount: 0x10
2025-09-20 22:54:59,727 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:00,466 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:00,466 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:00,466 - INFO - 🔄 Calling eth_gasPrice with params: []
2025-09-20 22:55:01,187 - INFO - ✅ eth_gasPrice succeeded
2025-09-20 22:55:01,188 - INFO - Raw result for eth_gasPrice: 0xf58e5
2025-09-20 22:55:01,188 - INFO - Raw eth_gasPrice hex: 0xf58e5
2025-09-20 22:55:01,188 - INFO - 🔄 Calling eth_estimateGas with params: [{'to': '0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7', 'value': '0x38d7ea4c68000', 'from': '0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b'}]
2025-09-20 22:55:01,913 - INFO - ✅ eth_estimateGas succeeded
2025-09-20 22:55:01,913 - INFO - Raw result for eth_estimateGas: 0x5208
2025-09-20 22:55:01,913 - INFO - Built transaction: nonce=16, to=0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7, value=0.001 ETH, gas=21000, gasPrice=1000000000 wei
2025-09-20 22:55:01,913 - INFO - Transaction built:
{
  "nonce": "0x10",
  "to": "0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7",
  "value": "0x38d7ea4c68000",
  "gas": "0x5208",
  "gasPrice": "0x3b9aca00",
  "chainId": "0xaa36a7",
  "data": "0x"
}
2025-09-20 22:55:01,913 - INFO - Signing transaction...
2025-09-20 22:55:01,922 - INFO - Expected address from private key: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
2025-09-20 22:55:01,935 - INFO - Signed transaction: 0xf86e10843b9aca00825208947e4dd6856aa001b78f1f2fe1...
2025-09-20 22:55:01,951 - INFO - Signed transaction hex: 0xf86e10843b9aca00825208947e4dd6856aa001b78f1f2fe1...
2025-09-20 22:55:01,951 - INFO - Sending transaction to network...
2025-09-20 22:55:01,951 - INFO - 🔄 Calling eth_sendRawTransaction with params: ['0xf86e10843b9aca00825208947e4dd6856aa001b78f1f2fe1a4a1f0e5b2cce5f787038d7ea4c68000808401546d71a06f8c906cfcf01502d635aa58b663956ac9cb3d356846887466f132ca86ee0244a04ca10e128cb7346a5c9d068d2efaf1bb0e5152988e0ef1b951e9c9e72df854b1']
2025-09-20 22:55:02,897 - INFO - ✅ eth_sendRawTransaction succeeded
2025-09-20 22:55:02,897 - INFO - Raw result for eth_sendRawTransaction: 0x9052cd8f106a52e1680e790be79b86a068085e8358acb15575c73c5b21dd0a14
2025-09-20 22:55:02,897 - INFO - 📤 Transaction sent: 0x9052cd8f106a52e1680e790be79b86a068085e8358acb15575c73c5b21dd0a14
2025-09-20 22:55:02,897 - INFO - Transaction sent: 0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b -> 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7, amount=0.001 ETH, tx_hash=0x9052cd8f106a52e1680e790be79b86a068085e8358acb15575c73c5b21dd0a14
2025-09-20 22:55:02,898 - INFO - RPC Client closed
2025-09-20 22:55:02,898 - INFO - TransactionManager closed
```

### 11. Send Transaction (Negative Amount)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli send --to "0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7" --amount -0.001 --password "Parsa1382@"
```
```output
Error: Amount must be positive
2025-09-20 22:55:03,396 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:04,416 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:04,416 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:04,416 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:55:04,416 - INFO - ✅ TransactionManager initialized
2025-09-20 22:55:04,417 - INFO - RPC Client closed
2025-09-20 22:55:04,417 - INFO - TransactionManager closed
```

### 12. Send Transaction (Invalid To Address)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli send --to "invalid" --amount 0.001 --password "Parsa1382@"
```
```output
Error: Invalid recipient address: invalid
2025-09-20 22:55:04,776 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:07,091 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:07,091 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:07,091 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:55:07,092 - INFO - ✅ TransactionManager initialized
2025-09-20 22:55:07,092 - INFO - Attempting to get wallet info for 0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b
2025-09-20 22:55:07,094 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:08,322 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:08,322 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:08,322 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:55:08,322 - INFO - 🔄 Calling eth_getBalance with params: ['0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b', 'latest']
2025-09-20 22:55:09,028 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:55:09,028 - INFO - Raw result for eth_getBalance: 0xd0dd1420654a90
2025-09-20 22:55:09,028 - INFO - 🔄 Calling eth_getBalance with params: ['0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b', 'latest']
2025-09-20 22:55:09,779 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:55:09,779 - INFO - Raw result for eth_getBalance: 0xd0dd1420654a90
2025-09-20 22:55:09,782 - INFO - RPC Client closed
2025-09-20 22:55:09,850 - INFO - Wallet info retrieved: private_key_available=True
2025-09-20 22:55:09,850 - INFO - Building transaction...
2025-09-20 22:55:09,851 - INFO - RPC Client closed
2025-09-20 22:55:09,851 - INFO - TransactionManager closed
```

### 13. Transaction Status (Valid Hash)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli tx status --hash "0xfae30a5dcf0e6776cda8a01efb26501702f733f7e4335fffe60bd035a458c647"
```
```output
Transaction Hash: 0xfae30a5dcf0e6776cda8a01efb26501702f733f7e4335fffe60bd035a458c647
Status: success
Message: Confirmed in block 9240825
Gas Used: 21,000
Block Number: 9240825
2025-09-20 22:55:10,188 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:11,857 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:11,858 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:11,858 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:55:11,858 - INFO - ✅ TransactionManager initialized
2025-09-20 22:55:11,858 - INFO - 🔄 Calling eth_getTransactionByHash with params: ['0xfae30a5dcf0e6776cda8a01efb26501702f733f7e4335fffe60bd035a458c647']
2025-09-20 22:55:12,730 - INFO - ✅ eth_getTransactionByHash succeeded
2025-09-20 22:55:12,730 - INFO - Raw result for eth_getTransactionByHash: {'blockHash': '0xc6095759fe9c91a5704123d67060a90d5f1fd4643de561db3a4eaa0a77f0d7b4', 'blockNumber': '0x8d00f9', 'from': '0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b', 'gas': '0x5208', 'gasPrice': '0x3b9aca00', 'hash': '0xfae30a5dcf0e6776cda8a01efb26501702f733f7e4335fffe60bd035a458c647', 'input': '0x', 'nonce': '0x9', 'to': '0x7e4dd6856aa001b78f1f2fe1a4a1f0e5b2cce5f7', 'transactionIndex': '0x2b', 'value': '0x2386f26fc10000', 'type': '0x0', 'chainId': '0xaa36a7', 'v': '0x1546d71', 'r': '0x3cd74fd2799dbd2229cbd239071bfc863f71666787767e0c04b7f0e7dbe7d021', 's': '0x1b1ac7ad9865b8ab8d23f6c007cb7cbd5c4409019666d300ea804f54bd37b6e5'}
2025-09-20 22:55:12,730 - INFO - 🔄 Calling eth_getTransactionReceipt with params: ['0xfae30a5dcf0e6776cda8a01efb26501702f733f7e4335fffe60bd035a458c647']
2025-09-20 22:55:13,632 - INFO - ✅ eth_getTransactionReceipt succeeded
2025-09-20 22:55:13,633 - INFO - Raw result for eth_getTransactionReceipt: {'blockHash': '0xc6095759fe9c91a5704123d67060a90d5f1fd4643de561db3a4eaa0a77f0d7b4', 'blockNumber': '0x8d00f9', 'contractAddress': None, 'cumulativeGasUsed': '0x3b4425', 'effectiveGasPrice': '0x3b9aca00', 'from': '0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b', 'gasUsed': '0x5208', 'logs': [], 'logsBloom': '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 'status': '0x1', 'to': '0x7e4dd6856aa001b78f1f2fe1a4a1f0e5b2cce5f7', 'transactionHash': '0xfae30a5dcf0e6776cda8a01efb26501702f733f7e4335fffe60bd035a458c647', 'transactionIndex': '0x2b', 'type': '0x0'}
2025-09-20 22:55:13,633 - INFO - Transaction status for 0xfae30a5dcf0e6776cda8a01efb26501702f733f7e4335fffe60bd035a458c647: success
2025-09-20 22:55:13,636 - INFO - RPC Client closed
2025-09-20 22:55:13,636 - INFO - TransactionManager closed
```

### 14. Transaction Status (Invalid Hash)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli tx status --hash "0x123"
```
```output
Error: Failed to check transaction status: Invalid transaction hash
2025-09-20 22:55:14,003 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:14,963 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:14,963 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:14,963 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:55:14,964 - INFO - ✅ TransactionManager initialized
2025-09-20 22:55:14,964 - ERROR - Failed to check transaction status: Invalid transaction hash
2025-09-20 22:55:14,966 - INFO - RPC Client closed
2025-09-20 22:55:14,966 - INFO - TransactionManager closed
```

### 15. Transaction History (Default Wallet)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli tx history
```
```output
Retrieved 27 transactions for 0xb0b51e4bb8e9ecc0a89d4bee4cbe02201acb936b:
--------------------------------------------------
Hash: 0x9052cd8f106a52e1680e790be79b86a068085e8358acb15575c73c5b21dd0a14
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.001000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9243873
--------------------------------------------------
Hash: 0xa401edea11e03b096fba3bcb3ba5477bec7d7288f44a5e45596c1749df6e86b5
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.001000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9243859
--------------------------------------------------
Hash: 0x89d86886280faf88db09c744954ddcf724218cf0d6b7a13221d240f392f523ac
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.020000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9241938
--------------------------------------------------
Hash: 0xd5b0b3a92e243d94d68435050d2512efe73422ec28946dc4f56a0a7a2b02d3dc
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9241080
--------------------------------------------------
Hash: 0xfb0f93f69d58378bdb519d30ee2803c5061b8bfb67a5404ccd77802a60541348
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9241079
--------------------------------------------------
Hash: 0xfbe1ed7c1d10b14050ab40f310be24ac94e7a0768af336892518bcb23e25cfca
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240964
--------------------------------------------------
Hash: 0x37947baea432ae36ef8f61d0656c78dd3b83889070ee747d8c57d20ec57cef28
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240895
--------------------------------------------------
Hash: 0xfae30a5dcf0e6776cda8a01efb26501702f733f7e4335fffe60bd035a458c647
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240825
--------------------------------------------------
Hash: 0xa9f75a8c0ed27d5fbab27f2b484412feed77f792797937ab283af4bed480ad5a
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240764
--------------------------------------------------
Hash: 0xe6d67ddaee88f542c842ae88f0e98d2e11f5a29391f39b2fe5e4a15fc56ec544
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240743
--------------------------------------------------
Hash: 0x988aeff0410fbf9312b49742ee7c8d1edc4e372a3da8d15bd2b47d007be6d870
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240651
--------------------------------------------------
Hash: 0x3ad147142b06baf80efccb5ed60d9310ef4af90a953e0baf3d9f48918ba3cd73
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,100 wei
Block Number: 9240569
--------------------------------------------------
Hash: 0x31cef91e837a5a159da73131e3ba5b12da3cfebda45c5adf1801d7b0d9a39d4c
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,089 wei
Block Number: 9240566
--------------------------------------------------
Hash: 0x7d9329b946dd181616f792bef1618059e5168581e7172a774a5827b55232b7b9
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,074 wei
Block Number: 9240544
--------------------------------------------------
Hash: 0x0f3db2834194f1e9b2d753ac034b3a5026a1543d4b582657137c06c720436160
From: 0xC0f3833B7e7216EEcD9f6bC2c7927A7aA36Ab58B
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.050000 ETH
Gas Used: 21,000
Gas Price: 1,100,065 wei
Block Number: 9240436
--------------------------------------------------
Hash: 0xb8fe6631beb1b191347c60d443ec2815de642b58f6acce1f44fcb5ab05f582b9
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,002,420 wei
Block Number: 9235884
--------------------------------------------------
Hash: 0xf9d050427600a5e988f73e5d9d960a4a81d3772deedc9a4c5c94b24335cb40b6
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,003,156 wei
Block Number: 9235821
--------------------------------------------------
Hash: 0xcab33ecfe31fb093a195851a341b14312c6cfcbd2fff44a3ce670fdbd9c1e92a
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,005,480 wei
Block Number: 9235759
--------------------------------------------------
Hash: 0xa1834db498ceba734f87a6f7ab211214f7b44c77ac434ee13f48e921f0fa0e44
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,005,782 wei
Block Number: 9235757
--------------------------------------------------
Hash: 0xdc954fda9b3e52d2dc83a6ed614227a11ad9ad0e295d1dd73e6a0230cb344b48
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,006,249 wei
Block Number: 9235753
--------------------------------------------------
Hash: 0x69c31e0cbed58fc5240723c806928b10b073cc69cf30aa708a48ec1f63e1aa3c
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,006,891 wei
Block Number: 9235735
--------------------------------------------------
Hash: 0xfd8921c6073c7befa6b02fed783a3b7cb04d0eaf810aa1516300cb603a36a0e4
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,006,500 wei
Block Number: 9235713
--------------------------------------------------
Hash: 0x0fc39b7baaf43b45f0d861c1a3f63be72555ce9ea466cf16eec626ec4abc3974
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,007,698 wei
Block Number: 9235638
--------------------------------------------------
Hash: 0xd42d87cea8a8e90c16d41691cb15587b02d7eaa1cee52cde7d892d8343c6239f
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,008,899 wei
Block Number: 9235467
--------------------------------------------------
Hash: 0xb54d72c08764463ee2a101ef63640855abed01cc7cb040be1e04b2c9c3e2dfd3
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,009,287 wei
Block Number: 9235236
--------------------------------------------------
Hash: 0xf6a7831d8d5824d1c12c43f6fa1539a3c7ddd75192b46543ec51259789f8e0e0
From: 0x52f1984Cd3e46e1214dB222D3Ff63712E7aCEedD
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.050000 ETH
Gas Used: 21,000
Gas Price: 1,100,017 wei
Block Number: 9230977
--------------------------------------------------
Hash: 0xfe8674a89163b5e4bdd89e632f7e0a2c37acd5fa3cc63ddfc1885226c1539163
From: 0x95A13F457C76d10A40D7e8497eD4F40c53F4d04b
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.050000 ETH
Gas Used: 21,000
Gas Price: 1,214,859 wei
Block Number: 9222066
--------------------------------------------------
2025-09-20 22:55:15,326 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:16,132 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:16,132 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:16,132 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:55:16,133 - INFO - ✅ TransactionManager initialized
2025-09-20 22:55:16,146 - INFO - Fetching transaction history for 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b from Etherscan
2025-09-20 22:55:17,446 - INFO - Retrieved 27 transactions for 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
2025-09-20 22:55:17,450 - INFO - RPC Client closed
2025-09-20 22:55:17,450 - INFO - TransactionManager closed
```

### 16. Transaction History (From Address)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli tx history --address "0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b"
```
```output
Retrieved 27 transactions for 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b:
--------------------------------------------------
Hash: 0x9052cd8f106a52e1680e790be79b86a068085e8358acb15575c73c5b21dd0a14
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.001000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9243873
--------------------------------------------------
Hash: 0xa401edea11e03b096fba3bcb3ba5477bec7d7288f44a5e45596c1749df6e86b5
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.001000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9243859
--------------------------------------------------
Hash: 0x89d86886280faf88db09c744954ddcf724218cf0d6b7a13221d240f392f523ac
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.020000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9241938
--------------------------------------------------
Hash: 0xd5b0b3a92e243d94d68435050d2512efe73422ec28946dc4f56a0a7a2b02d3dc
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9241080
--------------------------------------------------
Hash: 0xfb0f93f69d58378bdb519d30ee2803c5061b8bfb67a5404ccd77802a60541348
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9241079
--------------------------------------------------
Hash: 0xfbe1ed7c1d10b14050ab40f310be24ac94e7a0768af336892518bcb23e25cfca
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240964
--------------------------------------------------
Hash: 0x37947baea432ae36ef8f61d0656c78dd3b83889070ee747d8c57d20ec57cef28
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240895
--------------------------------------------------
Hash: 0xfae30a5dcf0e6776cda8a01efb26501702f733f7e4335fffe60bd035a458c647
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240825
--------------------------------------------------
Hash: 0xa9f75a8c0ed27d5fbab27f2b484412feed77f792797937ab283af4bed480ad5a
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240764
--------------------------------------------------
Hash: 0xe6d67ddaee88f542c842ae88f0e98d2e11f5a29391f39b2fe5e4a15fc56ec544
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240743
--------------------------------------------------
Hash: 0x988aeff0410fbf9312b49742ee7c8d1edc4e372a3da8d15bd2b47d007be6d870
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240651
--------------------------------------------------
Hash: 0x3ad147142b06baf80efccb5ed60d9310ef4af90a953e0baf3d9f48918ba3cd73
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,100 wei
Block Number: 9240569
--------------------------------------------------
Hash: 0x31cef91e837a5a159da73131e3ba5b12da3cfebda45c5adf1801d7b0d9a39d4c
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,089 wei
Block Number: 9240566
--------------------------------------------------
Hash: 0x7d9329b946dd181616f792bef1618059e5168581e7172a774a5827b55232b7b9
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,074 wei
Block Number: 9240544
--------------------------------------------------
Hash: 0x0f3db2834194f1e9b2d753ac034b3a5026a1543d4b582657137c06c720436160
From: 0xC0f3833B7e7216EEcD9f6bC2c7927A7aA36Ab58B
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.050000 ETH
Gas Used: 21,000
Gas Price: 1,100,065 wei
Block Number: 9240436
--------------------------------------------------
Hash: 0xb8fe6631beb1b191347c60d443ec2815de642b58f6acce1f44fcb5ab05f582b9
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,002,420 wei
Block Number: 9235884
--------------------------------------------------
Hash: 0xf9d050427600a5e988f73e5d9d960a4a81d3772deedc9a4c5c94b24335cb40b6
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,003,156 wei
Block Number: 9235821
--------------------------------------------------
Hash: 0xcab33ecfe31fb093a195851a341b14312c6cfcbd2fff44a3ce670fdbd9c1e92a
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,005,480 wei
Block Number: 9235759
--------------------------------------------------
Hash: 0xa1834db498ceba734f87a6f7ab211214f7b44c77ac434ee13f48e921f0fa0e44
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,005,782 wei
Block Number: 9235757
--------------------------------------------------
Hash: 0xdc954fda9b3e52d2dc83a6ed614227a11ad9ad0e295d1dd73e6a0230cb344b48
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,006,249 wei
Block Number: 9235753
--------------------------------------------------
Hash: 0x69c31e0cbed58fc5240723c806928b10b073cc69cf30aa708a48ec1f63e1aa3c
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,006,891 wei
Block Number: 9235735
--------------------------------------------------
Hash: 0xfd8921c6073c7befa6b02fed783a3b7cb04d0eaf810aa1516300cb603a36a0e4
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,006,500 wei
Block Number: 9235713
--------------------------------------------------
Hash: 0x0fc39b7baaf43b45f0d861c1a3f63be72555ce9ea466cf16eec626ec4abc3974
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,007,698 wei
Block Number: 9235638
--------------------------------------------------
Hash: 0xd42d87cea8a8e90c16d41691cb15587b02d7eaa1cee52cde7d892d8343c6239f
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,008,899 wei
Block Number: 9235467
--------------------------------------------------
Hash: 0xb54d72c08764463ee2a101ef63640855abed01cc7cb040be1e04b2c9c3e2dfd3
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,009,287 wei
Block Number: 9235236
--------------------------------------------------
Hash: 0xf6a7831d8d5824d1c12c43f6fa1539a3c7ddd75192b46543ec51259789f8e0e0
From: 0x52f1984Cd3e46e1214dB222D3Ff63712E7aCEedD
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.050000 ETH
Gas Used: 21,000
Gas Price: 1,100,017 wei
Block Number: 9230977
--------------------------------------------------
Hash: 0xfe8674a89163b5e4bdd89e632f7e0a2c37acd5fa3cc63ddfc1885226c1539163
From: 0x95A13F457C76d10A40D7e8497eD4F40c53F4d04b
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.050000 ETH
Gas Used: 21,000
Gas Price: 1,214,859 wei
Block Number: 9222066
--------------------------------------------------
2025-09-20 22:55:17,812 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:18,699 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:18,699 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:18,699 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:55:18,700 - INFO - ✅ TransactionManager initialized
2025-09-20 22:55:18,713 - INFO - Fetching transaction history for 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b from Etherscan
2025-09-20 22:55:19,719 - INFO - Retrieved 27 transactions for 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
2025-09-20 22:55:19,723 - INFO - RPC Client closed
2025-09-20 22:55:19,723 - INFO - TransactionManager closed
```

### 17. Transaction History (To Address)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli tx history --address "0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7"
```
```output
Retrieved 27 transactions for 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7:
--------------------------------------------------
Hash: 0x9052cd8f106a52e1680e790be79b86a068085e8358acb15575c73c5b21dd0a14
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.001000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9243873
--------------------------------------------------
Hash: 0xa401edea11e03b096fba3bcb3ba5477bec7d7288f44a5e45596c1749df6e86b5
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.001000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9243859
--------------------------------------------------
Hash: 0x89d86886280faf88db09c744954ddcf724218cf0d6b7a13221d240f392f523ac
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.020000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9241938
--------------------------------------------------
Hash: 0xd5b0b3a92e243d94d68435050d2512efe73422ec28946dc4f56a0a7a2b02d3dc
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9241080
--------------------------------------------------
Hash: 0xfb0f93f69d58378bdb519d30ee2803c5061b8bfb67a5404ccd77802a60541348
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9241079
--------------------------------------------------
Hash: 0xfbe1ed7c1d10b14050ab40f310be24ac94e7a0768af336892518bcb23e25cfca
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240964
--------------------------------------------------
Hash: 0x37947baea432ae36ef8f61d0656c78dd3b83889070ee747d8c57d20ec57cef28
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240895
--------------------------------------------------
Hash: 0xfae30a5dcf0e6776cda8a01efb26501702f733f7e4335fffe60bd035a458c647
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240825
--------------------------------------------------
Hash: 0xa9f75a8c0ed27d5fbab27f2b484412feed77f792797937ab283af4bed480ad5a
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240764
--------------------------------------------------
Hash: 0xe6d67ddaee88f542c842ae88f0e98d2e11f5a29391f39b2fe5e4a15fc56ec544
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240743
--------------------------------------------------
Hash: 0x988aeff0410fbf9312b49742ee7c8d1edc4e372a3da8d15bd2b47d007be6d870
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,000,000 wei
Block Number: 9240651
--------------------------------------------------
Hash: 0x3ad147142b06baf80efccb5ed60d9310ef4af90a953e0baf3d9f48918ba3cd73
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,100 wei
Block Number: 9240569
--------------------------------------------------
Hash: 0x31cef91e837a5a159da73131e3ba5b12da3cfebda45c5adf1801d7b0d9a39d4c
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,089 wei
Block Number: 9240566
--------------------------------------------------
Hash: 0x7d9329b946dd181616f792bef1618059e5168581e7172a774a5827b55232b7b9
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,000,074 wei
Block Number: 9240544
--------------------------------------------------
Hash: 0x22fb9be6620efe24baef6a8ef45b25a1cd79bbf5def6c78db8043fd54e24b736
From: 0x993a0f3653887078215914BAdCF039263293adD9
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.050000 ETH
Gas Used: 21,000
Gas Price: 1,100,063 wei
Block Number: 9240440
--------------------------------------------------
Hash: 0xb8fe6631beb1b191347c60d443ec2815de642b58f6acce1f44fcb5ab05f582b9
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,002,420 wei
Block Number: 9235884
--------------------------------------------------
Hash: 0xf9d050427600a5e988f73e5d9d960a4a81d3772deedc9a4c5c94b24335cb40b6
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,003,156 wei
Block Number: 9235821
--------------------------------------------------
Hash: 0xcab33ecfe31fb093a195851a341b14312c6cfcbd2fff44a3ce670fdbd9c1e92a
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,005,480 wei
Block Number: 9235759
--------------------------------------------------
Hash: 0xa1834db498ceba734f87a6f7ab211214f7b44c77ac434ee13f48e921f0fa0e44
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,005,782 wei
Block Number: 9235757
--------------------------------------------------
Hash: 0xdc954fda9b3e52d2dc83a6ed614227a11ad9ad0e295d1dd73e6a0230cb344b48
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,006,249 wei
Block Number: 9235753
--------------------------------------------------
Hash: 0x69c31e0cbed58fc5240723c806928b10b073cc69cf30aa708a48ec1f63e1aa3c
From: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,006,891 wei
Block Number: 9235735
--------------------------------------------------
Hash: 0xfd8921c6073c7befa6b02fed783a3b7cb04d0eaf810aa1516300cb603a36a0e4
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,006,500 wei
Block Number: 9235713
--------------------------------------------------
Hash: 0x0fc39b7baaf43b45f0d861c1a3f63be72555ce9ea466cf16eec626ec4abc3974
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,007,698 wei
Block Number: 9235638
--------------------------------------------------
Hash: 0xd42d87cea8a8e90c16d41691cb15587b02d7eaa1cee52cde7d892d8343c6239f
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,008,899 wei
Block Number: 9235467
--------------------------------------------------
Hash: 0xb54d72c08764463ee2a101ef63640855abed01cc7cb040be1e04b2c9c3e2dfd3
From: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
To: 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
Value: 0.010000 ETH
Gas Used: 21,000
Gas Price: 1,009,287 wei
Block Number: 9235236
--------------------------------------------------
Hash: 0x82f3b96f2ad512302370b414dc36d782cc563d1caae15d2964b51f8b1cf9ef97
From: 0x42645cE4Dd0B766dE53ee483cbf54bcEa670f9b2
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.050000 ETH
Gas Used: 21,000
Gas Price: 1,100,014 wei
Block Number: 9230981
--------------------------------------------------
Hash: 0x9759c170cecacfda492d34a64b100cb1e03bc0225be9c9e378e2f69478e8e530
From: 0x15095Ec8FB1Fc9C664b3223459dFF43158ACe7aD
To: 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
Value: 0.050000 ETH
Gas Used: 21,000
Gas Price: 1,217,938 wei
Block Number: 9221975
--------------------------------------------------
2025-09-20 22:55:20,079 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:20,970 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:20,970 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:20,970 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:55:20,970 - INFO - ✅ TransactionManager initialized
2025-09-20 22:55:20,979 - INFO - Fetching transaction history for 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7 from Etherscan
2025-09-20 22:55:21,822 - INFO - Retrieved 27 transactions for 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
2025-09-20 22:55:21,826 - INFO - RPC Client closed
2025-09-20 22:55:21,826 - INFO - TransactionManager closed
```

### 18. Transaction History (Invalid Address)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli tx history --address "invalid"
```
```output
Error: Invalid address: invalid
2025-09-20 22:55:22,177 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:23,069 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:23,069 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:23,069 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:55:23,069 - INFO - ✅ TransactionManager initialized
2025-09-20 22:55:23,071 - INFO - RPC Client closed
2025-09-20 22:55:23,071 - INFO - TransactionManager closed
```

### 19. Transaction Export (Default Wallet)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli tx export --output "tx_history.json"
```
```output
Transaction history exported to: /Users/parsaoryani/PycharmProjects/ethereum-cli/exports/tx_history.json
2025-09-20 22:55:23,435 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:24,550 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:24,550 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:24,550 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:55:24,551 - INFO - ✅ TransactionManager initialized
2025-09-20 22:55:24,565 - INFO - Fetching transaction history for 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b from Etherscan
2025-09-20 22:55:25,971 - INFO - Retrieved 27 transactions for 0xB0b51E4bb8E9EcC0a89D4BEe4Cbe02201acb936b
2025-09-20 22:55:25,975 - INFO - Transaction history exported to /Users/parsaoryani/PycharmProjects/ethereum-cli/exports/tx_history.json
2025-09-20 22:55:25,977 - INFO - RPC Client closed
2025-09-20 22:55:25,977 - INFO - TransactionManager closed
```

### 20. Transaction Export (Specific Address)
```bash
python /Users/parsaoryani/PycharmProjects/ethereum-cli/cli tx export --address "0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7" --output "tx_history_to.json"
```
```output
Transaction history exported to: /Users/parsaoryani/PycharmProjects/ethereum-cli/exports/tx_history_to.json
2025-09-20 22:55:26,337 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:27,171 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:27,171 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:27,171 - INFO - ✅ Connected to https://go.getblock.io/7018d72bb3df4d5f82120f1d92ca9a80 (Chain ID: 11155111)
2025-09-20 22:55:27,171 - INFO - ✅ TransactionManager initialized
2025-09-20 22:55:27,180 - INFO - Fetching transaction history for 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7 from Etherscan
2025-09-20 22:55:28,062 - INFO - Retrieved 27 transactions for 0x7E4Dd6856Aa001b78f1f2fE1A4A1f0e5b2CcE5f7
2025-09-20 22:55:28,065 - INFO - Transaction history exported to /Users/parsaoryani/PycharmProjects/ethereum-cli/exports/tx_history_to.json
2025-09-20 22:55:28,066 - INFO - RPC Client closed
2025-09-20 22:55:28,066 - INFO - TransactionManager closed
```

## Test Results

### Unit Tests
```bash
python -m unittest discover -s tests -v
```
```output
Adding project root to sys.path: /Users/parsaoryani/PycharmProjects/ethereum-cli
sys.path before: ['/Users/parsaoryani/PycharmProjects/ethereum-cli/src', '/Users/parsaoryani/PycharmProjects/ethereum-cli', '/Applications/PyCharm.app/Contents/plugins/python-ce/helpers/pycharm_display', '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python39.zip', '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9', '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/lib-dynload', '/Users/parsaoryani/PycharmProjects/ethereum-cli/.venv/lib/python3.9/site-packages', '/Applications/PyCharm.app/Contents/plugins/python-ce/helpers/pycharm_matplotlib_backend', '/Applications/PyCharm.app/Contents/plugins/python-ce/helpers/pycharm_plotly_backend']
sys.path after: ['/Users/parsaoryani/PycharmProjects/ethereum-cli/src', '/Users/parsaoryani/PycharmProjects/ethereum-cli', '/Applications/PyCharm.app/Contents/plugins/python-ce/helpers/pycharm_display', '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python39.zip', '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9', '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/lib-dynload', '/Users/parsaoryani/PycharmProjects/ethereum-cli/.venv/lib/python3.9/site-packages', '/Applications/PyCharm.app/Contents/plugins/python-ce/helpers/pycharm_matplotlib_backend', '/Applications/PyCharm.app/Contents/plugins/python-ce/helpers/pycharm_plotly_backend', '/Users/parsaoryani/PycharmProjects/ethereum-cli']
test_estimate_gas_invalid_transaction (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:28,378 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:28,378 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:28,378 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:28,378 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
ok
test_estimate_gas_success (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:28,379 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:28,380 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:28,380 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:28,380 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:55:28,380 - INFO - 🔄 Calling eth_estimateGas with params: [{'to': '0x1234567890123456789012345678901234567890', 'value': '0x1'}]
2025-09-20 22:55:28,885 - INFO - ✅ eth_estimateGas succeeded
2025-09-20 22:55:28,885 - INFO - Raw result for eth_estimateGas: 0x5208
ok
test_get_balance_invalid_address (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:28,888 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:28,889 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:28,889 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:28,889 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
ok
test_get_balance_invalid_unit (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:28,891 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:28,892 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:28,892 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:28,892 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
ok
test_get_balance_success (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:28,894 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:28,894 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:28,894 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:28,894 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:55:28,895 - INFO - 🔄 Calling eth_getBalance with params: ['0x1234567890123456789012345678901234567890', 'latest']
2025-09-20 22:55:29,396 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:55:29,396 - INFO - Raw result for eth_getBalance: 0x1bc16d674ec80000
2025-09-20 22:55:29,396 - INFO - 🔄 Calling eth_getBalance with params: ['0x1234567890123456789012345678901234567890', 'latest']
2025-09-20 22:55:29,902 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:55:29,902 - INFO - Raw result for eth_getBalance: 0x1bc16d674ec80000
2025-09-20 22:55:29,902 - INFO - 🔄 Calling eth_getBalance with params: ['0x1234567890123456789012345678901234567890', 'latest']
2025-09-20 22:55:30,407 - INFO - ✅ eth_getBalance succeeded
2025-09-20 22:55:30,408 - INFO - Raw result for eth_getBalance: 0x1bc16d674ec80000
ok
test_get_block_info_invalid_block (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:30,414 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:30,415 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:30,415 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:30,415 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:55:30,416 - INFO - 🔄 Calling eth_getBlockByNumber with params: ['0x64', False]
2025-09-20 22:55:30,917 - INFO - ✅ eth_getBlockByNumber succeeded
2025-09-20 22:55:30,917 - INFO - Raw result for eth_getBlockByNumber: None
ok
test_get_block_info_negative_block (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:30,920 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:30,921 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:30,921 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:30,921 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
ok
test_get_block_info_success (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:30,923 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:30,924 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:30,924 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:30,924 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:55:30,925 - INFO - 🔄 Calling eth_getBlockByNumber with params: ['0x64', False]
2025-09-20 22:55:31,428 - INFO - ✅ eth_getBlockByNumber succeeded
2025-09-20 22:55:31,429 - INFO - Raw result for eth_getBlockByNumber: {'timestamp': '0x5f5e100', 'miner': '0x1234567890123456789012345678901234567890', 'gasUsed': '0x5208', 'transactions': ['0x1111111111111111111111111111111111111111111111111111111111111111']}
ok
test_get_block_number_success (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:31,433 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:31,433 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:31,433 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:31,433 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:55:31,434 - INFO - 🔄 Calling eth_blockNumber with params: []
2025-09-20 22:55:31,938 - INFO - ✅ eth_blockNumber succeeded
2025-09-20 22:55:31,938 - INFO - Raw result for eth_blockNumber: 0x123
ok
test_get_chain_id_success (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:31,941 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:31,942 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:31,942 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:31,942 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:55:31,943 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:32,449 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:32,449 - INFO - Raw result for eth_chainId: 0xaa36a7
ok
test_get_chain_id_wrong_network (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:32,453 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:32,453 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:32,454 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:32,454 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:55:32,454 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:32,956 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:32,956 - INFO - Raw result for eth_chainId: 0x1
ok
test_get_gas_price_success (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:32,958 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:32,958 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:32,958 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:32,958 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:55:32,959 - INFO - 🔄 Calling eth_gasPrice with params: []
2025-09-20 22:55:33,459 - INFO - ✅ eth_gasPrice succeeded
2025-09-20 22:55:33,459 - INFO - Raw result for eth_gasPrice: 0x3b9aca00
2025-09-20 22:55:33,459 - INFO - Raw eth_gasPrice hex: 0x3b9aca00
2025-09-20 22:55:33,460 - INFO - 🔄 Calling eth_gasPrice with params: []
2025-09-20 22:55:33,965 - INFO - ✅ eth_gasPrice succeeded
2025-09-20 22:55:33,965 - INFO - Raw result for eth_gasPrice: 0x3b9aca00
2025-09-20 22:55:33,965 - INFO - Raw eth_gasPrice hex: 0x3b9aca00
2025-09-20 22:55:33,966 - INFO - 🔄 Calling eth_gasPrice with params: []
2025-09-20 22:55:34,467 - INFO - ✅ eth_gasPrice succeeded
2025-09-20 22:55:34,468 - INFO - Raw result for eth_gasPrice: 0x3b9aca00
2025-09-20 22:55:34,468 - INFO - Raw eth_gasPrice hex: 0x3b9aca00
ok
test_get_gas_price_zero_fallback (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:34,475 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:34,477 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:34,477 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:34,477 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:55:34,478 - INFO - 🔄 Calling eth_gasPrice with params: []
2025-09-20 22:55:34,983 - INFO - ✅ eth_gasPrice succeeded
2025-09-20 22:55:34,983 - INFO - Raw result for eth_gasPrice: 0x0
2025-09-20 22:55:34,983 - INFO - Raw eth_gasPrice hex: 0x0
2025-09-20 22:55:34,983 - WARNING - Zero gas price received, using default 1.0 Gwei
ok
test_get_network_info_failure (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:34,988 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:34,989 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:34,989 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:34,989 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:55:34,990 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:35,495 - WARNING - 🌐 Network error on attempt 1: Network error
2025-09-20 22:55:40,503 - WARNING - 🌐 Network error on attempt 2: Network error
2025-09-20 22:55:45,510 - WARNING - 🌐 Network error on attempt 3: Network error
2025-09-20 22:55:50,515 - WARNING - 🌐 Network error on attempt 4: Network error
2025-09-20 22:55:55,522 - WARNING - 🌐 Network error on attempt 5: Network error
2025-09-20 22:55:55,522 - ERROR - Failed to get network info: Network error: Network error
ok
test_get_network_info_success (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:55,532 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:55,533 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:55,533 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:55,533 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:55:55,535 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:56,041 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:56,041 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:56,041 - INFO - 🔄 Calling eth_blockNumber with params: []
2025-09-20 22:55:56,549 - INFO - ✅ eth_blockNumber succeeded
2025-09-20 22:55:56,549 - INFO - Raw result for eth_blockNumber: 0x123
2025-09-20 22:55:56,550 - INFO - 🔄 Calling eth_gasPrice with params: []
2025-09-20 22:55:57,052 - INFO - ✅ eth_gasPrice succeeded
2025-09-20 22:55:57,053 - INFO - Raw result for eth_gasPrice: 0x3b9aca00
2025-09-20 22:55:57,053 - INFO - Raw eth_gasPrice hex: 0x3b9aca00
ok
test_get_nonce_invalid_address (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:57,058 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:57,060 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:57,060 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:57,060 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
ok
test_get_nonce_success (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:57,063 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:57,064 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:57,064 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:57,064 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:55:57,065 - INFO - 🔄 Calling eth_getTransactionCount with params: ['0x1234567890123456789012345678901234567890', 'pending']
2025-09-20 22:55:57,571 - INFO - ✅ eth_getTransactionCount succeeded
2025-09-20 22:55:57,571 - INFO - Raw result for eth_getTransactionCount: 0x5
ok
test_get_stats (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:57,576 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:57,577 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:57,577 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:57,577 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:55:57,578 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:58,085 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:58,085 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:58,085 - INFO - 🔄 Calling eth_blockNumber with params: []
2025-09-20 22:55:58,590 - INFO - ✅ eth_blockNumber succeeded
2025-09-20 22:55:58,590 - INFO - Raw result for eth_blockNumber: 0xaa36a7
ok
test_get_transaction_status_invalid_hash (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:58,597 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:58,598 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:58,598 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:58,598 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
ok
test_get_transaction_status_not_found (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:58,601 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:58,602 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:58,602 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:58,602 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:55:58,603 - INFO - 🔄 Calling eth_getTransactionByHash with params: ['0x1111111111111111111111111111111111111111111111111111111111111111']
2025-09-20 22:55:59,110 - INFO - ✅ eth_getTransactionByHash succeeded
2025-09-20 22:55:59,110 - INFO - Raw result for eth_getTransactionByHash: None
ok
test_get_transaction_status_pending (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:55:59,116 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:55:59,117 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:55:59,117 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:55:59,117 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:55:59,118 - INFO - 🔄 Calling eth_getTransactionByHash with params: ['0x1111111111111111111111111111111111111111111111111111111111111111']
2025-09-20 22:55:59,623 - INFO - ✅ eth_getTransactionByHash succeeded
2025-09-20 22:55:59,624 - INFO - Raw result for eth_getTransactionByHash: {'hash': '0x1111111111111111111111111111111111111111111111111111111111111111'}
2025-09-20 22:55:59,624 - INFO - 🔄 Calling eth_getTransactionReceipt with params: ['0x1111111111111111111111111111111111111111111111111111111111111111']
2025-09-20 22:56:00,126 - INFO - ✅ eth_getTransactionReceipt succeeded
2025-09-20 22:56:00,127 - INFO - Raw result for eth_getTransactionReceipt: None
ok
test_get_transaction_status_success (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:56:00,130 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:56:00,131 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:56:00,131 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:56:00,131 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:56:00,132 - INFO - 🔄 Calling eth_getTransactionByHash with params: ['0x1111111111111111111111111111111111111111111111111111111111111111']
2025-09-20 22:56:00,639 - INFO - ✅ eth_getTransactionByHash succeeded
2025-09-20 22:56:00,639 - INFO - Raw result for eth_getTransactionByHash: {'hash': '0x1111111111111111111111111111111111111111111111111111111111111111'}
2025-09-20 22:56:00,639 - INFO - 🔄 Calling eth_getTransactionReceipt with params: ['0x1111111111111111111111111111111111111111111111111111111111111111']
2025-09-20 22:56:01,143 - INFO - ✅ eth_getTransactionReceipt succeeded
2025-09-20 22:56:01,143 - INFO - Raw result for eth_getTransactionReceipt: {'status': '0x1', 'blockNumber': '0x123', 'gasUsed': '0x5208'}
ok
test_init_success (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:56:01,148 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:56:01,149 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:56:01,149 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:56:01,149 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:56:01,151 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:56:01,151 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:56:01,151 - INFO - Raw result for eth_chainId: 0x1
2025-09-20 22:56:01,151 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 1)
ok
test_send_raw_transaction_invalid (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:56:01,154 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:56:01,155 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:56:01,155 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:56:01,155 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
ok
test_send_raw_transaction_success (tests.test_rpc_client.TestRPCClient) ... 2025-09-20 22:56:01,157 - INFO - 🔄 Calling eth_chainId with params: []
2025-09-20 22:56:01,158 - INFO - ✅ eth_chainId succeeded
2025-09-20 22:56:01,158 - INFO - Raw result for eth_chainId: 0xaa36a7
2025-09-20 22:56:01,158 - INFO - ✅ Connected to https://mock-rpc-url (Chain ID: 11155111)
2025-09-20 22:56:01,158 - INFO - 🔄 Calling eth_sendRawTransaction with params: ['0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff']
2025-09-20 22:56:01,665 - INFO - ✅ eth_sendRawTransaction succeeded
2025-09-20 22:56:01,665 - INFO - Raw result for eth_sendRawTransaction: 0x1111111111111111111111111111111111111111111111111111111111111111
2025-09-20 22:56:01,665 - INFO - 📤 Transaction sent: 0x1111111111111111111111111111111111111111111111111111111111111111
ok
test_build_transaction_gas_estimation_failure (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:01,674 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:01,688 - WARNING - Gas estimation failed: Gas estimation error, using default gas limit 21000
2025-09-20 22:56:01,688 - INFO - Built transaction: nonce=5, to=0x0987654321098765432109876543210987654321, value=1.0 ETH, gas=21000, gasPrice=1000000000 wei
ok
test_build_transaction_insufficient_balance (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:01,694 - INFO - ✅ TransactionManager initialized
ok
test_build_transaction_invalid_addresses (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:01,698 - INFO - ✅ TransactionManager initialized
ok
test_build_transaction_negative_amount (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:01,702 - INFO - ✅ TransactionManager initialized
ok
test_build_transaction_nonce_failure (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:01,706 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:01,706 - WARNING - Nonce fetch attempt 1 failed: Nonce error
2025-09-20 22:56:02,711 - WARNING - Nonce fetch attempt 2 failed: Nonce error
2025-09-20 22:56:03,713 - WARNING - Nonce fetch attempt 3 failed: Nonce error
ok
test_build_transaction_success (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:03,724 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:03,724 - INFO - Built transaction: nonce=5, to=0x0987654321098765432109876543210987654321, value=1.0 ETH, gas=21000, gasPrice=1000000000 wei
ok
test_check_transaction_status_failure (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:03,730 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:03,730 - ERROR - Failed to check transaction status: Invalid hash
ok
test_check_transaction_status_success (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:03,735 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:03,735 - INFO - Transaction status for 0x1111111111111111111111111111111111111111111111111111111111111111: success
ok
test_close (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:03,741 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:03,741 - INFO - TransactionManager closed
ok
test_export_transaction_history_failure (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:03,745 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:03,745 - INFO - Fetching transaction history for 0x1234567890123456789012345678901234567890 from Etherscan
ok
test_export_transaction_history_success (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:03,749 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:03,749 - INFO - Fetching transaction history for 0x1234567890123456789012345678901234567890 from Etherscan
2025-09-20 22:56:03,751 - INFO - Retrieved 1 transactions for 0x1234567890123456789012345678901234567890
2025-09-20 22:56:03,753 - INFO - Transaction history exported to /Users/parsaoryani/PycharmProjects/ethereum-cli/tests/test_exports/test_export.json
ok
test_get_transaction_history_api_failure (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:03,777 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:03,778 - INFO - Fetching transaction history for 0x1234567890123456789012345678901234567890 from Etherscan
2025-09-20 22:56:03,778 - ERROR - Etherscan API error: API error, details: Error
ok
test_get_transaction_history_invalid_address (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:03,781 - INFO - ✅ TransactionManager initialized
ok
test_get_transaction_history_network_failure (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:03,783 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:03,784 - INFO - Fetching transaction history for 0x1234567890123456789012345678901234567890 from Etherscan
2025-09-20 22:56:03,784 - WARNING - Etherscan fetch attempt 1 failed: Network error
2025-09-20 22:56:04,789 - WARNING - Etherscan fetch attempt 2 failed: Network error
2025-09-20 22:56:05,795 - WARNING - Etherscan fetch attempt 3 failed: Network error
ok
test_get_transaction_history_no_api_key (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:05,806 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:05,807 - WARNING - Etherscan API key not configured in settings.json
2025-09-20 22:56:05,807 - INFO - ✅ TransactionManager initialized
ok
test_get_transaction_history_success (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:05,813 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:05,813 - INFO - Fetching transaction history for 0x1234567890123456789012345678901234567890 from Etherscan
2025-09-20 22:56:05,814 - INFO - Retrieved 1 transactions for 0x1234567890123456789012345678901234567890
ok
test_init_invalid_json (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:05,820 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:05,820 - ERROR - Invalid JSON format in configuration file: /Users/parsaoryani/PycharmProjects/ethereum-cli/tests/test_config/test_settings.json
ok
test_init_missing_config_file (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:05,825 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:05,825 - ERROR - Configuration file not found at: /Users/parsaoryani/PycharmProjects/ethereum-cli/tests/nonexistent.json
ok
test_init_missing_config_keys (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:05,829 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:05,829 - ERROR - Missing required configuration key: network
ok
test_init_success (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:05,833 - INFO - ✅ TransactionManager initialized
ok
test_send_transaction_invalid_wallet (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:05,838 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:05,838 - INFO - Attempting to get wallet info for 0x1234567890123456789012345678901234567890
2025-09-20 22:56:05,838 - INFO - Wallet info retrieved: private_key_available=False
ok
test_send_transaction_network_failure (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:05,841 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:05,841 - INFO - Attempting to get wallet info for 0x1234567890123456789012345678901234567890
2025-09-20 22:56:05,841 - INFO - Wallet info retrieved: private_key_available=True
2025-09-20 22:56:05,841 - INFO - Building transaction...
2025-09-20 22:56:05,841 - INFO - Built transaction: nonce=5, to=0x0987654321098765432109876543210987654321, value=1.0 ETH, gas=21000, gasPrice=1000000000 wei
2025-09-20 22:56:05,841 - INFO - Transaction built:
{
  "nonce": "0x5",
  "to": "0x0987654321098765432109876543210987654321",
  "value": "0xde0b6b3a7640000",
  "gas": "0x5208",
  "gasPrice": "0x3b9aca00",
  "chainId": "0xaa36a7",
  "data": "0x"
}
2025-09-20 22:56:05,841 - INFO - Signing transaction...
2025-09-20 22:56:05,846 - INFO - Expected address from private key: 0x1Be31A94361a391bBaFB2a4CCd704F57dc04d4bb
2025-09-20 22:56:05,854 - INFO - Signed transaction: 0xf86f05843b9aca0082520894098765432109876543210987...
2025-09-20 22:56:05,865 - INFO - Signed transaction hex: 0xf86f05843b9aca0082520894098765432109876543210987...
2025-09-20 22:56:05,865 - INFO - Sending transaction to network...
2025-09-20 22:56:05,865 - WARNING - Attempt 1 failed: Network error
2025-09-20 22:56:10,871 - WARNING - Attempt 2 failed: Network error
2025-09-20 22:56:15,876 - WARNING - Attempt 3 failed: Network error
ok
test_send_transaction_success (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:15,886 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:15,886 - INFO - Attempting to get wallet info for 0x1234567890123456789012345678901234567890
2025-09-20 22:56:15,887 - INFO - Wallet info retrieved: private_key_available=True
2025-09-20 22:56:15,887 - INFO - Building transaction...
2025-09-20 22:56:15,887 - INFO - Built transaction: nonce=5, to=0x0987654321098765432109876543210987654321, value=1.0 ETH, gas=21000, gasPrice=1000000000 wei
2025-09-20 22:56:15,887 - INFO - Transaction built:
{
  "nonce": "0x5",
  "to": "0x0987654321098765432109876543210987654321",
  "value": "0xde0b6b3a7640000",
  "gas": "0x5208",
  "gasPrice": "0x3b9aca00",
  "chainId": "0xaa36a7",
  "data": "0x"
}
2025-09-20 22:56:15,887 - INFO - Signing transaction...
2025-09-20 22:56:15,895 - INFO - Expected address from private key: 0x1Be31A94361a391bBaFB2a4CCd704F57dc04d4bb
2025-09-20 22:56:15,907 - INFO - Signed transaction: 0xf86f05843b9aca0082520894098765432109876543210987...
2025-09-20 22:56:15,922 - INFO - Signed transaction hex: 0xf86f05843b9aca0082520894098765432109876543210987...
2025-09-20 22:56:15,922 - INFO - Sending transaction to network...
2025-09-20 22:56:15,922 - INFO - Transaction sent: 0x1234567890123456789012345678901234567890 -> 0x0987654321098765432109876543210987654321, amount=1.0 ETH, tx_hash=0x1111111111111111111111111111111111111111111111111111111111111111
ok
test_sign_transaction_invalid_private_key (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:15,926 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:15,927 - ERROR - Invalid private key format: Non-hexadecimal digit found
ok
test_sign_transaction_missing_field (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:15,930 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:15,933 - INFO - Expected address from private key: 0x1Be31A94361a391bBaFB2a4CCd704F57dc04d4bb
ok
test_sign_transaction_signature_verification_failure (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:15,936 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:15,938 - INFO - Expected address from private key: 0x1234567890123456789012345678901234567890
2025-09-20 22:56:15,938 - INFO - Signed transaction: 0xed05843b9aca008252089409876543210987654321098765...
2025-09-20 22:56:15,938 - ERROR - Signature verification failed: recovered=0x0987654321098765432109876543210987654321, expected=0x1234567890123456789012345678901234567890
ok
test_sign_transaction_success (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:15,940 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:15,941 - INFO - Expected address from private key: 0x1234567890123456789012345678901234567890
2025-09-20 22:56:15,941 - INFO - Signed transaction: 0xed05843b9aca008252089409876543210987654321098765...
ok
test_transaction_export_no_default_wallet (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:15,944 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:15,944 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:15,944 - INFO - TransactionManager closed
ok
test_transaction_export_success (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:15,947 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:15,947 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:15,947 - INFO - Fetching transaction history for 0x1234567890123456789012345678901234567890 from Etherscan
2025-09-20 22:56:15,948 - INFO - Retrieved 1 transactions for 0x1234567890123456789012345678901234567890
2025-09-20 22:56:15,948 - INFO - Transaction history exported to /Users/parsaoryani/PycharmProjects/ethereum-cli/tests/test_exports/test_export.json
2025-09-20 22:56:15,948 - INFO - TransactionManager closed
ok
test_transaction_history_no_default_wallet (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:15,950 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:15,950 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:15,951 - INFO - TransactionManager closed
ok
test_transaction_history_success (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:15,953 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:15,953 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:15,953 - INFO - Fetching transaction history for 0x1234567890123456789012345678901234567890 from Etherscan
2025-09-20 22:56:15,954 - INFO - Retrieved 1 transactions for 0x1234567890123456789012345678901234567890
2025-09-20 22:56:15,954 - INFO - TransactionManager closed
ok
test_transaction_send_failure (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:15,956 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:15,956 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:15,956 - INFO - Attempting to get wallet info for 0x1234567890123456789012345678901234567890
2025-09-20 22:56:15,956 - INFO - Wallet info retrieved: private_key_available=True
2025-09-20 22:56:15,956 - INFO - Building transaction...
2025-09-20 22:56:15,957 - INFO - Built transaction: nonce=5, to=0x0987654321098765432109876543210987654321, value=1.0 ETH, gas=21000, gasPrice=1000000000 wei
2025-09-20 22:56:15,957 - INFO - Transaction built:
{
  "nonce": "0x5",
  "to": "0x0987654321098765432109876543210987654321",
  "value": "0xde0b6b3a7640000",
  "gas": "0x5208",
  "gasPrice": "0x3b9aca00",
  "chainId": "0xaa36a7",
  "data": "0x"
}
2025-09-20 22:56:15,957 - INFO - Signing transaction...
2025-09-20 22:56:15,960 - INFO - Expected address from private key: 0x1Be31A94361a391bBaFB2a4CCd704F57dc04d4bb
2025-09-20 22:56:15,965 - INFO - Signed transaction: 0xf86f05843b9aca0082520894098765432109876543210987...
2025-09-20 22:56:15,973 - INFO - Signed transaction hex: 0xf86f05843b9aca0082520894098765432109876543210987...
2025-09-20 22:56:15,973 - INFO - Sending transaction to network...
2025-09-20 22:56:15,973 - WARNING - Attempt 1 failed: Network error
2025-09-20 22:56:20,979 - WARNING - Attempt 2 failed: Network error
2025-09-20 22:56:25,984 - WARNING - Attempt 3 failed: Network error
2025-09-20 22:56:25,986 - INFO - TransactionManager closed
ok
test_transaction_send_negative_amount (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:25,995 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:25,995 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:25,996 - INFO - TransactionManager closed
ok
test_transaction_send_no_default_wallet (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:26,002 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:26,003 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:26,003 - INFO - TransactionManager closed
ok
test_transaction_send_success (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:26,007 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:26,008 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:26,008 - INFO - Attempting to get wallet info for 0x1234567890123456789012345678901234567890
2025-09-20 22:56:26,008 - INFO - Wallet info retrieved: private_key_available=True
2025-09-20 22:56:26,008 - INFO - Building transaction...
2025-09-20 22:56:26,008 - INFO - Built transaction: nonce=5, to=0x0987654321098765432109876543210987654321, value=1.0 ETH, gas=21000, gasPrice=1000000000 wei
2025-09-20 22:56:26,008 - INFO - Transaction built:
{
  "nonce": "0x5",
  "to": "0x0987654321098765432109876543210987654321",
  "value": "0xde0b6b3a7640000",
  "gas": "0x5208",
  "gasPrice": "0x3b9aca00",
  "chainId": "0xaa36a7",
  "data": "0x"
}
2025-09-20 22:56:26,008 - INFO - Signing transaction...
2025-09-20 22:56:26,014 - INFO - Expected address from private key: 0x1Be31A94361a391bBaFB2a4CCd704F57dc04d4bb
2025-09-20 22:56:26,024 - INFO - Signed transaction: 0xf86f05843b9aca0082520894098765432109876543210987...
2025-09-20 22:56:26,037 - INFO - Signed transaction hex: 0xf86f05843b9aca0082520894098765432109876543210987...
2025-09-20 22:56:26,037 - INFO - Sending transaction to network...
2025-09-20 22:56:26,037 - INFO - Transaction sent: 0x1234567890123456789012345678901234567890 -> 0x0987654321098765432109876543210987654321, amount=1.0 ETH, tx_hash=0x1111111111111111111111111111111111111111111111111111111111111111
2025-09-20 22:56:26,037 - INFO - TransactionManager closed
ok
test_transaction_status_failure (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:26,040 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:26,040 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:26,040 - ERROR - Failed to check transaction status: Invalid hash
2025-09-20 22:56:26,041 - INFO - TransactionManager closed
ok
test_transaction_status_success (tests.test_transaction.TestTransactionManager) ... Current working directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
Looking for src directory: /Users/parsaoryani/PycharmProjects/ethereum-cli/src
2025-09-20 22:56:26,044 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:26,044 - INFO - ✅ TransactionManager initialized
2025-09-20 22:56:26,044 - INFO - Transaction status for 0x1111111111111111111111111111111111111111111111111111111111111111: success
2025-09-20 22:56:26,044 - INFO - TransactionManager closed
ok
test_generate_wallet_short_password (tests.test_wallet.TestWalletManager) ... ok
test_generate_wallet_success (tests.test_wallet.TestWalletManager) ... ok
test_get_default_wallet (tests.test_wallet.TestWalletManager) ... ok
test_get_wallet_info_nonexistent (tests.test_wallet.TestWalletManager) ... ok
test_get_wallet_info_success (tests.test_wallet.TestWalletManager) ... ok
test_get_wallet_info_wrong_password (tests.test_wallet.TestWalletManager) ... ok
test_import_wallet_invalid_key (tests.test_wallet.TestWalletManager) ... ok
test_import_wallet_short_password (tests.test_wallet.TestWalletManager) ... ok
test_import_wallet_success (tests.test_wallet.TestWalletManager) ... ok
test_is_valid_address (tests.test_wallet.TestWalletManager) ... ok
test_list_wallets (tests.test_wallet.TestWalletManager) ... ok
test_list_wallets_empty (tests.test_wallet.TestWalletManager) ... ok
test_set_default_wallet_invalid_address (tests.test_wallet.TestWalletManager) ... ok
test_set_default_wallet_nonexistent (tests.test_wallet.TestWalletManager) ... ok
test_set_default_wallet_success (tests.test_wallet.TestWalletManager) ... ok

----------------------------------------------------------------------
Ran 77 tests in 58.003s

OK
```

## Design Choices

1. **Network: Sepolia Testnet**
   - **Why**: Safe environment for testing without risking real funds. Chain ID 11155111 ensures compatibility.
   - **How**: Configured via config/settings.json with a public RPC URL.

2. **Wallet Management**
   - **Why**: Secure storage of private keys is critical.
   - **How**: Keys are encrypted in JSON files with a password.

3. **Transaction Building**
   - **Why**: Manual RLP encoding ensures Ethereum protocol compliance.
   - **How**: Uses eth_account for signing and rlp for encoding.

4. **Etherscan API**
   - **Why**: Reliable source for transaction history.
   - **How**: Implements retry logic for API calls.

5. **CLI Design**
   - **Why**: User-friendly interface for developers.
   - **How**: Built with argparse for subcommands.

6. **Error Handling**
   - **Why**: Robustness against network or user errors.
   - **How**: Validates inputs early and retries failed calls.
