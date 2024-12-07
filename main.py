# simple python finance tracker
# author: R. Kyle Norris
from tracker_sql import TransactionType, Pynance, pd, PynanceVis, PynanceReport


if __name__ == '__main__':
    tracker = Pynance(db_file='sqlite:///test/example_transactions.db')

    vis = PynanceVis(tracker=tracker)

    vis.income_vs_expense_by_month()
