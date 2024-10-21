import json
from datetime import datetime
# from dataclasses import dataclass
# from dataclasses_json import dataclass_json
from enum import Enum


class TransactionType(Enum):
    expense = 0
    income = 1


class Transaction:
    def __init__(self, amount: float, timestamp: datetime = datetime.now(),
                 transaction_type: TransactionType = TransactionType.expense,
                 cat: str = "", desc: str = ""):
        self.amount: float = amount
        self.creation_datetime = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        self.transaction_type = transaction_type.value
        self.category = cat
        self.description = desc

    def __repr__(self):
        return (f"Transaction:\t${self.amount} | {TransactionType(self.transaction_type).name} " +
                f"| {self.category} | {self.description} | " +
                f"{self.creation_datetime}")


class Pynance:
    # python based finance tracker
    def __init__(self, data_file="data.json"):
        self.data_file = data_file
        data = self.load_data()
        self.transactions = data.get("transactions")
        self.total = data.get("total")

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
            json.dump(self.__dict__, f, indent=4)

    def perform_transaction(self, transaction: Transaction):

        self.transactions.append(transaction.__dict__)

        if transaction.transaction_type == TransactionType.expense.value:
            self.total -= transaction.amount
        elif transaction.transaction_type == TransactionType.income.value:
            self.total += transaction.amount

        self.save_data()

    def view_transactions(self):
        print("  \tAmount | Datetime | Type | Category | Description")
        for i, tran in enumerate(self.transactions):
            counter = i + 1
            print(f"{counter}:\t${tran['amount']} | "
                  f"{tran['creation_datetime']} | "
                  f"{TransactionType(tran['transaction_type']).name} | "
                  f"{tran['category']} | "
                  f"{tran['description']}")

    def view_summary(self):
        income = [trans['amount'] for trans in self.transactions if
                  trans['transaction_type'] == TransactionType.income.value]
        expense = [trans['amount'] for trans in self.transactions if
                   trans['transaction_type'] == TransactionType.expense.value]
        total_income = sum(income)
        count_income = len(income)
        total_expense = sum(expense)
        count_expense = len(expense)
        print("----------SUMMARY----------")
        print(f"Total Income: ${total_income} - Count: {count_income}")
        print(f"Total Expense: ${total_expense} - Count: {count_expense}")
        print(f'Current Balance: ${self.total}')
        print("----------END SUMMARY----------")
