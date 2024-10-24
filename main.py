# simple python finance tracker
# author: R. Kyle Norris
from tracker import Transaction, TransactionType, Pynance
from datetime import datetime
from random import randint

if __name__ == '__main__':
    tracker = Pynance()

    for expense in ['groceries', 'rent', 'utilities']:
        amount = randint(75, 600)
        transaction = Transaction(amount=amount, cat=expense)
        tracker.perform_transaction(transaction)

    tracker.perform_transaction(Transaction(amount=2000,
                                            transaction_type=TransactionType.income,
                                            cat="salary",
                                            desc="biweekly salary"))

    print("\n-----view transactions-----")
    tracker.view_transactions()

    print("\n-----view summary-----")
    tracker.view_summary()

    print("\n-----end------")

    tracker.visualize_expenses()

    input("\nPress Enter to continue...")
