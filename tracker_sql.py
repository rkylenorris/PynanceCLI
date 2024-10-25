import pandas as pd
import sqlite3
from pathlib import Path
from enum import Enum
from datetime import datetime
from sqlalchemy.types import Integer, Float, String, NVARCHAR

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class TransactionType(Enum):
    """
    enum representing the two possible transaction types
    """
    EXPENSE = 0
    INCOME = 1


class PynanceSQL:

    def __init__(self, db_file='transactions.db'):
        self.db_file = db_file
        self.transactions = self.load_transactions()

        self.dtypes = {
            "amount": Float(precision=2),
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

        with sqlite3.connect(self.db_file) as conn:
            df.to_sql('transactions',
                      conn,
                      if_exists='replace',
                      index=False,
                      # dtype=self.dtypes
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

    def view_transactions(self):
        print("  \tAmount | Processed | Type | Category | Description")
        for i, tran in enumerate(self.transactions):
            counter = i + 1
            print(f"{counter}:\t${tran['amount']} | "
                  f"{tran['created']} | "
                  f"{TransactionType(tran['transaction_type']).name} | "
                  f"{tran['category']} | "
                  f"{tran['description']}")