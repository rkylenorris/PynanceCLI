from tracker_sql import TransactionType, PynanceSQL, datetime, DATE_FORMAT
import json

file_path = "generated_transactions.json"
with open(file_path, "r") as f:
    transactions = json.load(f)['transactions']

tracker = PynanceSQL()

for transaction in transactions:
    tracker.process_transaction(
        amt=transaction["amount"],
        cat=transaction["category"],
        trans_type=TransactionType(transaction["transaction_type"]),
        desc=transaction["description"],
        created=datetime.strptime(transaction["creation_datetime"], DATE_FORMAT)
                                )
tracker.view_summary()