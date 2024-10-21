import click
from tracker import Transaction, TransactionType, Pynance

tracker = Pynance()


@click.group()
def cli():
    pass


@cli.command()
@click.argument('amount', type=float)
@click.argument('category', type=str)
@click.option('-d', default="", help='Description of the transaction')
@click.option('--income', is_flag=True, help='Mark this transaction as income')
@click.option('--expense', is_flag=True, help='Mark this transaction as an expense')
def add(amount: float, category: str, d: str,
        income: bool, expense: bool) -> None:

    if income and expense:
        click.echo("Error: can only have one transaction type, "
                   "either income or expense")
        return
    elif not income and not expense:
        click.echo("Error: must have a transaction type, "
                   "either income or expense")
        return

    trans_type = TransactionType.income if income else TransactionType.expense
    transaction = Transaction(amount=amount, transaction_type=trans_type,
                              cat=category, desc=d)
    tracker.perform_transaction(transaction)
    click.echo(f"Transaction ({transaction.category} {trans_type.name} "
               f"of ${transaction.amount}) added")


@cli.command()
def view() -> None:
    tracker.view_transactions()


@cli.command()
def summary() -> None:
    tracker.view_summary()


if __name__ == '__main__':
    cli()