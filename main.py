# simple python finance tracker
# author: R. Kyle Norris
from tracker_sql import TransactionType, Pynance, pd, PynanceVis, PynanceReport
from random import randint


if __name__ == '__main__':
    tracker = Pynance()

    rpt = PynanceReport(tracker)

    rpt.create_report()
