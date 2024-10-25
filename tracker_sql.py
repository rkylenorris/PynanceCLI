import pandas as pd
import sqlite3
from pathlib import Path


class PynanceSQL:

    def __init__(self, db_file='transactions.db'):
        self.db_file = db_file
        self.transactions = self.load_transactions()

        self.dtypes = {
            "amount": float,
            "created": str,
            "transaction_type": int,
            "category": str,
            "description": str,
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
                      dtype=self.dtypes)
