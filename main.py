# simple python finance tracker
# author: R. Kyle Norris
from tracker_sql import TransactionType, PynanceSQL, pd
from random import randint


if __name__ == '__main__':
    tracker = PynanceSQL()

    for expense in ['groceries', 'rent', 'utilities', 'subscriptions']:
        amount = round(float(randint(750, 6000) / 10),2)
        tracker.process_transaction(amt=amount, cat=expense)

    tracker.process_transaction(amt=2000, cat='salary',
                                trans_type=TransactionType.INCOME,
                                desc="biweekly salary")

    # tracker.process_transaction(Transaction(amount=2000,
    #                                         transaction_type=TransactionType.income,
    #                                         cat="salary",
    #                                         desc="biweekly salary"))

    print("\n-----view transactions-----")
    tracker.view_transactions()

    # df = pd.DataFrame(tracker.transactions)
    # df['creation_month'] = pd.to_datetime(df.creation_datetime).dt.month_name()
    # grouped = df.groupby("creation_month")
    # print(grouped)

    # print("\n-----view summary-----")
    # tracker.get_summary()
    #
    # print("\n-----end------")
    #
    # tracker.visualize_income_v_expenses()
    #
    # input("\nPress Enter to continue...")
