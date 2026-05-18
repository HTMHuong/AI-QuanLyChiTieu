from modules.ai_agent import classify_expense
from modules.database import save_transaction


def process_input(user_text):

    data = classify_expense(user_text)

    # Nếu AI trả list
    if isinstance(data, list):

        data = data[0]

    # Chuẩn hóa amount
    amount = str(
        data.get(
            "amount",
            0
        )
    )

    amount = amount.lower()

    amount = amount.replace(
        "k",
        "000"
    )

    amount = amount.replace(
        ".",
        ""
    )

    try:

        amount = int(amount)

    except:

        amount = 0

    data["amount"] = amount

    if amount > 0:

        save_transaction(
            data
        )

    return f"""
📌 Danh mục: {data["category"]}

💰 Số tiền: {amount:,}đ

📝 Mô tả: {data["description"]}
"""