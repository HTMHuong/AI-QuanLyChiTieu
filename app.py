import streamlit as st
import pandas as pd
from streamlit_calendar import calendar

# PHẦN 1: DÀNH CHO BACKEND (Giữ nguyên các biến kết nối)
budget = 0 
spent = 0
remaining = 0
percent_usage = 0.0
calendar_events = [] # Backend đổ dữ liệu sự kiện vào đây

# PHẦN 2: GIAO DIỆN 
st.set_page_config(page_title="Quản Gia Tài Chính AI", page_icon="💰", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .header-style {
        background: -webkit-linear-gradient(45deg, #1E1E1E, #2E86C1);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 32px !important; font-weight: 800; margin-bottom: 5px;
    }
    
    .ai-card {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        padding: 20px; border-radius: 15px; border-left: 6px solid #2E86C1;
        margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    div[data-testid="stVerticalBlock"] > div > div > div > div.stVerticalBlock {
        background-color: #ffffff; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# HÀM HIỂN THỊ LỊCH GIỮA MÀN HÌNH (Dialog)
@st.dialog("📅 Chi tiết lịch chi tiêu", width="large")
def show_calendar_popup():
    
    calendar(events=calendar_events, options={"initialView": "dayGridMonth", "locale": "vi"})
    if st.button("Đóng"):
        st.rerun()

col_chat, col_dashboard = st.columns([1, 1.5])

# SIDEBAR
with st.sidebar:
    st.markdown('<p class="header-style">🤖 Quản Gia AI</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    with st.popover("⚙️ Cài đặt ngân sách", use_container_width=True):
        st.number_input("Nhập ngân sách:", key="input_budget")
        st.button("Lưu", type="primary", use_container_width=True)

    st.markdown("### 📊 Tóm tắt nhanh")
    st.table(pd.DataFrame({
        "Mục": ["💰 Ngân sách", "💸 Đã chi", "📉 Còn lại"], 
        "Giá trị": [f"{budget:,}", f"{spent:,}", f"{remaining:,}"]
    }))
    
    st.write(f"**Tỉ lệ sử dụng: {percent_usage * 100:.1f}%**") 
    st.progress(percent_usage)

#  CỘT CHAT
with col_chat:
    st.markdown('<p class="header-style">💬 Ghi chép nhanh</p>', unsafe_allow_html=True)
    with st.container(height=500):
        # Backend hiển thị chat tại đây
        st.chat_message("assistant").write("Chào bạn!")
    st.chat_input("Nhập chi tiêu...")

# CỘT DASHBOARD
with col_dashboard:
    c_head1, c_head2 = st.columns([2.5, 1])
    with c_head1:
        st.markdown('<p class="header-style">📊 Báo cáo chi tiêu</p>', unsafe_allow_html=True)
        st.write("Tổng quan tháng hiện tại")
    with c_head2:
        st.write("") # Tạo khoảng cách
        # Sửa tên nút thành "Xem lịch chi"
        if st.button("📅 Xem lịch chi", type="primary", use_container_width=True):
            show_calendar_popup() # Khi nhấn sẽ gọi hàm hiện giữa màn hình

    # AI Insight Card
    st.markdown(f"""
        <div class="ai-card">
            #### 💡 Trợ lý AI Phân Tích
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <p>🔮 <b>Dự báo chi cuối tháng:</b> 0đ</p>
                    <p>✨ <i>Đang chờ dữ liệu...</i></p>
                </div>
                <div>
                    <p>🏷️ <b>Mục chi nhiều nhất:</b> ---</p>
                    <p><i>💡 Lời khuyên: Hãy bắt đầu ghi chép để AI tư vấn nhé!</i></p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Thẻ Metric
    m1, m2, m3 = st.columns(3)
    m1.metric("Trung bình/Ngày", "0đ")
    m2.metric("Chi cao nhất", "0đ")
    m3.metric("Ví còn lại", f"{remaining:,}đ")

    st.divider()
    
    t1, t2 = st.tabs(["📉 Xu hướng", "📝 Nhật ký"])
    with t1:
        st.info("Khu vực hiển thị biểu đồ phân tích.")
    with t2:
        st.write("Bảng nhật ký giao dịch chi tiết.")