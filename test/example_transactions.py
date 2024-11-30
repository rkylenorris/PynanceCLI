import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tracker_sql import TransactionType, Pynance, datetime, DATE_FORMAT
import json


file_path = "generated_transactions.json"
with open(file_path, "r") as f:
    transactions = json.load(f)['transactions']

tracker = Pynance(db_file='sqlite:///example_transactions.db')

for transaction in transactions:
    tracker.process_transaction(
        amt=transaction["amount"],
        cat=transaction["category"],
        trans_type=TransactionType(transaction["transaction_type"]),
        desc=transaction["description"],
        created=datetime.strptime(transaction["creation_datetime"], DATE_FORMAT)
                                )

summary = tracker.get_summary_data()
