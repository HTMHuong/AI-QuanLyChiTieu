import json
import os

FILE_NAME="finance_data.json"

def load_transactions():

    if not os.path.exists(
        FILE_NAME
    ):
        return []

    try:

        with open(
            FILE_NAME,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return []


def save_transaction(data):

    transactions=load_transactions()

    transactions.append(data)

    with open(
        FILE_NAME,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            transactions,
            f,
            ensure_ascii=False,
            indent=4
        )