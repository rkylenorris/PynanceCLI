import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    """
    enum representing the two possible transaction types
    """
    expense = 0
    income = 1


class Transaction:
    """
    class representing a financial transaction
    """
    def __init__(self, amount: float, timestamp: datetime = datetime.now(),
                 transaction_type: TransactionType = TransactionType.expense,
                 cat: str = "", desc: str = ""):
        """
        initialises a new transaction object
        :param amount: float: money amount
        :param timestamp: datetime: datetime transaction occurred
        :param transaction_type: TransactionType: income or expense
        :param cat: str: category of transaction
        :param desc: str: description of transaction
        """
        self.amount: float = amount
        self.creation_datetime = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        self.transaction_type = transaction_type.value
        self.category = cat.title() if cat else ""
        self.description = desc.lower() if desc else ""


class Pynance:
    """
    class representing a financial tracker
    """
    def __init__(self, data_file="data.json"):
        """
        initialises a new financial tracker object
        :param data_file: str: path to data file (file for storing transactions)
        """
        self.data_file = data_file
        data = self.load_data()
        self.transactions = data.get("transactions")
        self.total = data.get("total")

    def load_data(self):
        """
        loads data from data file if it exists
        otherwise returns dict in a 0 state
        :return:
        """
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

    def perform_transaction(self, transaction: Transaction) -> None:
        """
        adds a new transaction to the tracker and
        adds/subtracts the total balance
        :param transaction: transaction object
        :return:
        """

        # append transaction object to transactions list
        self.transactions.append(transaction.__dict__)

        # add or subtract amount based on transaction_type property
        if transaction.transaction_type == TransactionType.expense.value:
            self.total -= transaction.amount
        elif transaction.transaction_type == TransactionType.income.value:
            self.total += transaction.amount

        self.save_data()

    def view_transactions(self):
        """
        prints all transactions in readable format
        :return:
        """
        print("  \tAmount | Datetime | Type | Category | Description")
        for i, tran in enumerate(self.transactions):
            counter = i + 1
            print(f"{counter}:\t${tran['amount']} | "
                  f"{tran['creation_datetime']} | "
                  f"{TransactionType(tran['transaction_type']).name} | "
                  f"{tran['category']} | "
                  f"{tran['description']}")

    def get_summary(self) -> dict:
        """
        returns summary of the tracker, including transaction total amount
        and count and the running balance
        :return:
        """
        income = [trans['amount'] for trans in self.transactions if
                  trans['transaction_type'] == TransactionType.income.value]
        expense = [trans['amount'] for trans in self.transactions if
                   trans['transaction_type'] == TransactionType.expense.value]
        total_income = sum(income)
        count_income = len(income)
        total_expense = sum(expense)
        count_expense = len(expense)

        return {
            "total_income": total_income,
            "count_income": count_income,
            "total_expense": total_expense,
            "count_expense": count_expense,
            "total": self.total
        }

    def visualize_expenses(self):
        """
        method for creating pie chart of expenses by category

        :return:
        """
        # get expense transactions only
        expense = [trans for trans in self.transactions if
                   trans['transaction_type'] == TransactionType.expense.value]

        # group by category using dictionary
        cats = {}
        for trans in expense:
            cats[trans['category']] = (cats.get(trans['category'], 0) +
                                       trans['amount'])

        # draw plot
        plt.figure(figsize=(10, 10))
        plt.pie(list(cats.values()), labels=list(cats.keys()), autopct='%1.1f%%',
                colors=sns.color_palette('pastel'))
        plt.axis('equal')
        plt.title(f"Expense Transactions by Category")
        plt.show()

    def visualize_income_v_expenses(self):
        summary = self.get_summary()

        labels = ['Income', 'Expense']
        values = [summary['total_income'], summary['total_expense']]

        plt.figure(figsize=(10, 10))
        plt.bar(labels, values, color=['green', 'red'])
        plt.title("Income vs Expenses")
        plt.ylabel("Amount $")
        plt.show()
