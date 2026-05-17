import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
from datetime import datetime

from modules.logic_agent import process_input
from modules.database import load_transactions


# ======================
# BACKEND
# ======================

transactions=load_transactions()

budget=10000000

spent=sum(
    int(item.get("amount",0))
    for item in transactions
)

remaining=max(
    budget-spent,
    0
)

percent_usage=min(
    spent/budget,
    1
) if budget>0 else 0


# Calendar: tổng chi mỗi ngày

daily_total={}

today=datetime.now().strftime(
    "%Y-%m-%d"
)

for item in transactions:

    amount=int(
        item.get(
            "amount",
            0
        )
    )

    daily_total[today]=daily_total.get(
        today,
        0
    )+amount


calendar_events=[]

for date,total in daily_total.items():

    calendar_events.append({

        "title":
        f'Tổng: {total:,}đ',

        "start":
        date,

        "color":
        "#ff6b6b"

    })


# Chat history

if "messages" not in st.session_state:

    st.session_state.messages=[

        {
            "role":"assistant",
            "content":"👋 Tôi là Quản Gia AI. Hãy nhập chi tiêu của bạn."
        }

    ]


# Dashboard

average=0
highest=0
top_category="---"

if transactions:

    average=spent//30

    highest=max(

        int(item["amount"])
        for item in transactions

    )

    categories={}

    for item in transactions:

        cat=item["category"]

        categories[cat]=categories.get(
            cat,
            0
        )+int(item["amount"])

    top_category=max(
        categories,
        key=categories.get
    )


# ======================
# GIAO DIỆN
# ======================

st.set_page_config(
    page_title="Quản Gia Tài Chính AI",
    page_icon="💰",
    layout="wide"
)

st.markdown("""

<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap'
);

html,
body,
[class*="css"]{

font-family:'Inter',sans-serif;

}


/* Sidebar */

[data-testid="stSidebar"]{

background-color:#1E1E2E;

}

[data-testid="stSidebar"] *{

color:white !important;

}


/* Chat */

[data-testid="chat-message-container"]{

background:white;
border-radius:10px;

}

/* Chat AI */

[data-testid="chat-message-container"]{

background:#ffffff !important;
border-radius:12px;
padding:8px;

}

/* Nội dung chat */

[data-testid="chat-message-container"] p,
[data-testid="chat-message-container"] span,
[data-testid="chat-message-container"] div{

color:#000000 !important;
opacity:1 !important;

}


/* Metric */

[data-testid="stMetric"] *{

color:#222222 !important;

}


/* AI Card */

.ai-card{

background:
linear-gradient(
135deg,
#fdfbfb 0%,
#ebedee 100%
);

padding:20px;

border-radius:15px;

border-left:
6px solid #2E86C1;

margin-bottom:25px;

box-shadow:
0 4px 12px rgba(
0,
0,
0,
0.05
);

color:#222222;

}


.header-style{

background:
-webkit-linear-gradient(
45deg,
#1E1E1E,
#2E86C1
);

-webkit-background-clip:text;

-webkit-text-fill-color:
transparent;

font-size:32px!important;

font-weight:800;

margin-bottom:5px;

}


div[data-testid="stVerticalBlock"] > div > div > div > div.stVerticalBlock{

background:white;

padding:25px;

border-radius:15px;

box-shadow:
0 4px 15px rgba(
0,
0,
0,
0.05
);

border:
1px solid #f0f2f6;

}

</style>

""",unsafe_allow_html=True)


# ======================
# LỊCH
# ======================

@st.dialog(
"📅 Chi tiết lịch chi tiêu",
width="large"
)

def show_calendar_popup():

    calendar(

        events=calendar_events,

        options={

            "initialView":"dayGridMonth",
            "locale":"vi"

        }

    )

    if st.button(
        "Đóng"
    ):
        st.rerun()


col_chat,col_dashboard=st.columns(
    [1,1.5]
)


# ======================
# SIDEBAR
# ======================

with st.sidebar:

    st.markdown(
        '<p class="header-style">🤖 Quản Gia AI</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    with st.popover(
        "⚙️ Cài đặt ngân sách",
        use_container_width=True
    ):

        st.number_input(
            "Nhập ngân sách:",
            value=budget
        )

        st.button(
            "Lưu",
            type="primary",
            use_container_width=True
        )

    st.markdown(
        "### 📊 Tóm tắt nhanh"
    )

    st.table(

        pd.DataFrame({

            "Mục":[
                "💰 Ngân sách",
                "💸 Đã chi",
                "📉 Còn lại"
            ],

            "Giá trị":[
                f"{budget:,}",
                f"{spent:,}",
                f"{remaining:,}"
            ]

        })

    )

    st.write(
        f"**Tỉ lệ sử dụng: {percent_usage*100:.1f}%**"
    )

    st.progress(
        percent_usage
    )


# ======================
# CHAT
# ======================

with col_chat:

    st.markdown(
    '<p class="header-style">💬 Ghi chép nhanh</p>',
    unsafe_allow_html=True
    )

    with st.container():

        for message in st.session_state.messages:

            with st.chat_message(
                message["role"]
            ):

                st.write(
                    message["content"]
                )

    user_input=st.chat_input(
        "Nhập chi tiêu..."
    )

    if user_input:

        st.session_state.messages.append({

            "role":"user",
            "content":user_input

        })

        ai_response=process_input(
            user_input
        )

        st.session_state.messages.append({

            "role":"assistant",
            "content":ai_response

        })

        st.rerun()


# ======================
# DASHBOARD
# ======================

with col_dashboard:

    c1,c2=st.columns([2.5,1])

    with c1:

        st.markdown(
            '<p class="header-style">📊 Báo cáo chi tiêu</p>',
            unsafe_allow_html=True
        )

        st.write(
            "Tổng quan tháng hiện tại"
        )

    with c2:

        st.write("")

        if st.button(
            "📅 Xem lịch chi",
            type="primary",
            use_container_width=True
        ):

            show_calendar_popup()

    st.markdown(

f"""

<div class="ai-card">

<h4>💡 Trợ lý AI Phân Tích</h4>

🔮 <b>Dự báo chi cuối tháng:</b>
{spent*1.2:,.0f}đ

<br><br>

✨ Tổng giao dịch:
{len(transactions)}

<br><br>

🏷️ Mục chi nhiều nhất:
{top_category}

<br><br>

💡 Bạn đã sử dụng
{percent_usage*100:.1f}%
ngân sách

</div>

""",

unsafe_allow_html=True

)

    m1,m2,m3=st.columns(3)

    m1.metric(
        "Trung bình/Ngày",
        f"{average:,}đ"
    )

    m2.metric(
        "Chi cao nhất",
        f"{highest:,}đ"
    )

    m3.metric(
        "Ví còn lại",
        f"{remaining:,}đ"
    )

    st.divider()

    t1,t2=st.tabs(
        ["📉 Xu hướng","📝 Nhật ký"]
    )

    with t1:

        if transactions:

            chart_data=pd.DataFrame(
                transactions
            )

            chart_data["amount"]=chart_data[
                "amount"
            ].astype(int)

            st.line_chart(
                chart_data["amount"]
            )

        else:

            st.info(
                "Chưa có dữ liệu"
            )

    with t2:

        if transactions:

            st.dataframe(
                pd.DataFrame(
                    transactions
                ),
                use_container_width=True
            )

        else:

            st.info(
                "Chưa có dữ liệu"
            )