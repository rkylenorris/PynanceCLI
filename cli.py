import click
from tracker_sql import TransactionType, Pynance, PynanceVis, PynanceReport

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

    trans_type = TransactionType(1) if income else TransactionType(0)
    tracker.process_transaction(amt=amount, trans_type=trans_type,
                                cat=category.title(), desc=d.lower())

    click.echo(f"Transaction ({trans_type.name} {category.title()}) "
               f" ${amount}) added")


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
    smmry = tracker.get_summary_data()
    print("----------SUMMARY----------")
    print(f"Total Income: ${smmry['total_income']} - Count: {smmry['count_income']}")
    print(f"Total Expense: ${smmry['total_expense']} - Count: {smmry['count_expense']}")
    print(f'Current Balance: ${smmry['total']}')
    print("----------END SUMMARY----------")


@cli.command()
def vis_exp():
    vis = PynanceVis(tracker)
    vis.expense_by_category()


@cli.command()
def vis_income_exp():
    vis = PynanceVis(tracker)
    vis.income_vs_expense_by_month()


@cli.command()
def create_report():
    report = PynanceReport(tracker)
    report.create_report()


if __name__ == '__main__':
    cli()
