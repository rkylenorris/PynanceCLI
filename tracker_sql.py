import pandas as pd
from pathlib import Path
from enum import Enum
from datetime import datetime

from matplotlib import pyplot as plt
from sqlalchemy.types import Integer, NVARCHAR, REAL
from sqlalchemy import create_engine

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class TransactionType(Enum):
    """
    enum representing the two possible transaction types
    """
    EXPENSE = 0
    INCOME = 1


class Pynance:

    def __init__(self, db_file='sqlite:///transactions.db'):
        self.db_file = db_file
        self.transactions = self.load_transactions()

        self.dtypes = {
            "amount": REAL(),
            "created": NVARCHAR(length=255),
            "transaction_type": Integer(),
            "category": NVARCHAR(length=255),
            "description": NVARCHAR(length=255),
        }

    def load_transactions(self):
        if not Path(self.db_file).exists():
            return []
        else:
            return pd.read_sql_query(
                'SELECT * FROM transactions', self.db_file
            ).values.tolist()

    def save_transactions(self):
        df = pd.DataFrame(self.transactions)
        eng = create_engine(self.db_file)
        df.to_sql('transactions',
                  eng,
                  if_exists='replace',
                  index=False,
                  dtype=self.dtypes
                  )

    def process_transaction(self,
                            amt: float,
                            cat: str,
                            trans_type: TransactionType = TransactionType.EXPENSE,
                            desc: str = ""
                            ) -> None:
        """
        method to add transaction to database
        :param amt: amt of transaction
        :param cat: category of transaction
        :param trans_type: income or expense
        :param desc: description of transaction
        :return:
        """
        self.transactions.append({
            "amount": amt,
            "created": datetime.now().strftime(DATE_FORMAT),
            "transaction_type": trans_type.value,
            "category": cat.title(),
            "description": desc.lower(),
        })
        self.save_transactions()

    def get_summary_data(self):

        income = [trans['amount'] for trans in self.transactions if
                  trans['transaction_type'] == TransactionType.INCOME.value]
        expense = [trans['amount'] for trans in self.transactions if
                   trans['transaction_type'] == TransactionType.EXPENSE.value]

        return {
            "IncomeTotal": sum(income),
            "IncomeCount": len(income),
            "ExpenseTotal": sum(expense),
            "ExpenseCount": len(expense),
            "CurrentBalance": sum(income) - sum(expense),
        }

    def view_summary(self):
        data = self.get_summary_data()
        print("----------SUMMARY----------")
        print(f"Income Total: ${data['IncomeTotal']} - Income Count: {data['IncomeCount']}")
        print(f"Expense Total: ${data['ExpenseTotal']} - Expense Count: {data['ExpenseCount']}")
        print(f'Current Balance: ${data["CurrentBalance"]}')
        print("----------END SUMMARY----------")

    def view_transactions(self):
        print("  \tAmount | Processed | Type | Category | Description")
        for i, tran in enumerate(self.transactions):
            counter = i + 1
            print(f"{counter}:\t${tran['amount']} | "
                  f"{tran['created']} | "
                  f"{TransactionType(tran['transaction_type']).name} | "
                  f"{tran['category']} | "
                  f"{tran['description']}")


class PynanceVis:

    def __init__(self, tracker: Pynance):
        self.tracker = tracker

    def expense_by_category(self):
        # create engine and query
        eng = create_engine(self.tracker.db_file)
        query = f"SELECT * FROM transactions WHERE transaction_type = {TransactionType.EXPENSE.value}"
        # use pandas to query db for expense transactions
        df = pd.read_sql_query(query, eng)
        # group by category, sum amount
        grouped = df[['category', 'amount']].groupby('category').sum().reset_index()
        # break the amounts and the categories out
        amounts = grouped['amount']
        categories = grouped['category']
        # create visualization
        _, ax = plt.subplots()
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', wedgeprops=dict(width=0.5))
        plt.title("Expense Transactions by Category")
        plt.show()
