# simple python finance tracker
# author: R. Kyle Norris
from tracker_sql import TransactionType, Pynance, pd, PynanceVis
from random import randint


if __name__ == '__main__':
    tracker = Pynance()

    vis = PynanceVis(tracker)
    vis.income_vs_expense_by_month()
