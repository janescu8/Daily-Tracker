import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime  # 👈 這一行是關鍵
import pytz

# 加上 scope
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Google auth
creds_dict = st.secrets["google_service_account"]
credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

# gspread
gc = gspread.authorize(credentials)
sheet = gc.open("Daily-Tracker").sheet1

# ===== 預設值 =====
user_name = "Sanny"
topic_list = ["英語", "日語", "法語", "程式", "AI應用", "繪畫", "音樂", "日記", "其他"]

# ===== Streamlit UI =====
st.title("📘 習慣／學習追蹤表單")

tz = pytz.timezone('Asia/Taipei')  # 建議這樣寫在外面

with st.form("track_form"):
    
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    user = st.text_input("👤 使用者", value=user_name)
    topic = st.selectbox("🗂️ 主題", topic_list)
    done = st.checkbox("✅ 是否完成", value=False)
    note = st.text_area("📝 備註（可選）")
    
    submitted = st.form_submit_button("📤 提交紀錄")
    
    if submitted:
        st.balloons()
        # 寫入 Google Sheets
        sheet.append_row([now, user, topic, "✅" if done else "❌", note])
        st.success("✅ 已成功提交紀錄！")

# ===== 顯示最新資料（可選）=====
st.markdown("---")
if st.checkbox("📄 顯示目前追蹤資料"):
    records = sheet.get_all_records()
    st.table(records[::-1])  # 倒著顯示（最新在上）
