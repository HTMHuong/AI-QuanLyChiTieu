import google.generativeai as genai
import os
import json
import re

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model=genai.GenerativeModel(
    "gemini-2.5-flash"
)

def classify_expense(text):

    prompt=f"""
    Phân tích nội dung sau:

    "{text}"

    Trả về JSON đúng định dạng:

    {{
        "category":"",
        "amount":0,
        "description":""
    }}

    Quy tắc:
    - category bằng tiếng Việt
    - amount là số nguyên
    - description ngắn gọn
    - Chỉ trả JSON thuần
    - Không markdown
    - Không giải thích
    """

    try:

        response=model.generate_content(
            prompt
        )

        result=response.text.strip()

        # Xóa markdown nếu Gemini tự thêm
        result=re.sub(
            r"```json|```",
            "",
            result
        ).strip()

        # Kiểm tra JSON hợp lệ
        data=json.loads(
            result
        )

        return data

    except json.JSONDecodeError:

        return {
            "category":"Không xác định",
            "amount":0,
            "description":"Lỗi định dạng AI"
        }

    except Exception as e:

        return {
            "category":"Lỗi",
            "amount":0,
            "description":str(e)
        }