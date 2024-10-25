import click
from tracker import Transaction, TransactionType, Pynance

tracker = Pynance()
# TODO create way of setting the data file to custom location


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
    """
    adds a transaction to finance tracker object
    :param amount: float
    :param category: str
    :param d: str
    :param income: bool
    :param expense: bool
    :return:
    """
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
                              cat=category.title(), desc=d.lower())
    tracker.perform_transaction(transaction)
    click.echo(f"Transaction ({trans_type.name} {transaction.category} "
               f" ${transaction.amount}) added")


@cli.command()
def view() -> None:
    """
    prints the list of transactions in a readable format
    :return:
    """
    tracker.view_transactions()


@cli.command()
def summary() -> None:
    """
    shows a summary of the transactions and savings in readable format
    :return:
    """
    sum = tracker.get_summary()
    print("----------SUMMARY----------")
    print(f"Total Income: ${sum['total_income']} - Count: {sum['count_income']}")
    print(f"Total Expense: ${sum['total_expense']} - Count: {sum['count_expense']}")
    print(f'Current Balance: ${sum['total']}')
    print("----------END SUMMARY----------")


@cli.command()
def vis_exp():
    tracker.visualize_expenses()


if __name__ == '__main__':
    cli()
