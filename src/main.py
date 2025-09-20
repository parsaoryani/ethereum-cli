import argparse
import logging
from typing import Optional
from wallet import WalletManager, wallet_generate, wallet_import, wallet_show, wallet_list, wallet_use
from transaction import TransactionManager, transaction_send, transaction_status, transaction_history, \
    transaction_export
from rpc_client import RPCClient

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def balance(address: Optional[str] = None) -> None:
    """
    CLI command: Check wallet balance.
    Supports: ./cli balance [--address [address]]
    """
    try:
        wallet_manager = WalletManager()
        rpc_client = RPCClient()
        # Use default wallet if no address specified
        if not address:
            address = wallet_manager.get_default_wallet()
            if not address:
                print("No default wallet set. Use './cli wallet use' to set a default wallet.")
                exit(1)

        if not wallet_manager._is_valid_address(address):
            print(f"Error: Invalid address: {address}")
            exit(1)

        balance_eth = rpc_client.get_balance(address, 'ether')
        balance_wei = rpc_client.get_balance(address, 'wei')
        print(f"Address: {address}")
        print(f"Balance: {balance_eth:.6f} ETH")
        print(f"Balance: {balance_wei:,} Wei")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    finally:
        rpc_client.close()


def run():
    """
    Main CLI entry point for Ethereum CLI on Sepolia Testnet.
    Supports: ./cli [wallet|balance|send|tx] ...
    """
    parser = argparse.ArgumentParser(description="Ethereum CLI for Sepolia Testnet")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Wallet commands
    wallet_parser = subparsers.add_parser("wallet", help="Wallet management commands")
    wallet_subparsers = wallet_parser.add_subparsers(dest="wallet_command", help="Wallet subcommands")

    # Wallet generate
    wallet_generate_parser = wallet_subparsers.add_parser("generate", help="Generate new wallet")
    wallet_generate_parser.add_argument("--password", required=True, help="Password for encryption")
    wallet_generate_parser.set_defaults(func=wallet_generate)

    # Wallet import
    wallet_import_parser = wallet_subparsers.add_parser("import", help="Import existing wallet")
    wallet_import_parser.add_argument("--private-key", required=True, help="Private key to import")
    wallet_import_parser.add_argument("--password", required=True, help="Password for encryption")
    wallet_import_parser.set_defaults(func=wallet_import)

    # Wallet show
    wallet_show_parser = wallet_subparsers.add_parser("show", help="Show wallet information")
    wallet_show_parser.add_argument("--address",
                                    help="Specific wallet address (optional, uses default wallet if not specified)")
    wallet_show_parser.add_argument("--password", help="Password for private key access (optional)")
    wallet_show_parser.set_defaults(func=wallet_show)

    # Wallet list
    wallet_list_parser = wallet_subparsers.add_parser("list", help="List all wallets")
    wallet_list_parser.set_defaults(func=wallet_list)

    # Wallet use
    wallet_use_parser = wallet_subparsers.add_parser("use", help="Set default wallet")
    wallet_use_parser.add_argument("--address", required=True, help="Wallet address to set as default")
    wallet_use_parser.set_defaults(func=wallet_use)

    # Balance command
    balance_parser = subparsers.add_parser("balance", help="Check wallet balance")
    balance_parser.add_argument("--address", help="Wallet address (optional, uses default wallet if not specified)")
    balance_parser.set_defaults(func=balance)

    # Transaction commands
    tx_parser = subparsers.add_parser("send", help="Send ETH to an address")
    tx_parser.add_argument("--to", required=True, help="Recipient address")
    tx_parser.add_argument("--amount", type=float, required=True, help="Amount in ETH")
    tx_parser.add_argument("--from", dest="from_address",
                           help="Sender address (optional, uses default wallet if not specified)")
    tx_parser.add_argument("--password", required=True, help="Wallet password")
    tx_parser.set_defaults(func=transaction_send)

    tx_status_parser = subparsers.add_parser("tx", help="Transaction commands")
    tx_status_subparsers = tx_status_parser.add_subparsers(dest="tx_command", help="Transaction subcommands")

    tx_status_subparser = tx_status_subparsers.add_parser("status", help="Check transaction status")
    tx_status_subparser.add_argument("--hash", required=True, help="Transaction hash")
    tx_status_subparser.set_defaults(func=transaction_status)

    tx_history_parser = tx_status_subparsers.add_parser("history", help="Fetch transaction history")
    tx_history_parser.add_argument("--address", help="Wallet address (optional, uses default wallet if not specified)")
    tx_history_parser.set_defaults(func=transaction_history)

    tx_export_parser = tx_status_subparsers.add_parser("export", help="Export transaction history to JSON")
    tx_export_parser.add_argument("--address", help="Wallet address (optional, uses default wallet if not specified)")
    tx_export_parser.add_argument("--output", help="Output filename (optional, defaults to tx_history_<address>.json)")
    tx_export_parser.set_defaults(func=transaction_export)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        exit(1)

    # Call the appropriate function with filtered arguments
    if args.command == "wallet":
        if not args.wallet_command:
            wallet_parser.print_help()
            exit(1)
        if args.wallet_command == "generate":
            args.func(args.password)
        elif args.wallet_command == "import":
            args.func(args.private_key, args.password)
        elif args.wallet_command == "show":
            args.func(args.address, args.password)
        elif args.wallet_command == "list":
            args.func()
        elif args.wallet_command == "use":
            args.func(args.address)
    elif args.command == "balance":
        args.func(args.address)
    elif args.command == "send":
        args.func(args.to, args.amount, args.password, args.from_address)
    elif args.command == "tx":
        if not args.tx_command:
            tx_status_parser.print_help()
            exit(1)
        if args.tx_command == "status":
            args.func(args.hash)
        elif args.tx_command == "history":
            args.func(args.address)
        elif args.tx_command == "export":
            args.func(args.address, args.output)


if __name__ == '__main__':
    run()