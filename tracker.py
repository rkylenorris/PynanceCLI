import json
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class TransactionTypes(Enum):
    expense = 0
    income = 1


@dataclass
class Transaction:
    amount: float = 0.00
    type: TransactionTypes = TransactionTypes.expense
    category: str = ""
    description: str = ""
    transaction_datetime: datetime = datetime.now()


class Pynance:
    # python based finance tracker
    def __init__(self, data_file="data.json"):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                        "total": 0,
                        "transactions": []
                     }

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=4)

    def perform_transaction(self, transaction: Transaction):

        self.data['transactions'].append(transaction)

        if transaction.type == TransactionTypes.expense:
            self.data['total'] -= transaction.amount
        elif transaction.type == TransactionTypes.income:
            self.data['total'] += transaction.amount

        self.save_data()




