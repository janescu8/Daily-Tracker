import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ===== 連接 Google Sheets =====
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# 打開指定的 Google Sheets 文件（第一個工作表）
sheet = client.open("學習追蹤表").sheet1

# ===== 預設值 =====
user_list = ["Sanny"]
topic_list = ["英語", "日語", "法語", "程式", "AI應用", "繪畫", "音樂", "社群"]

# ===== Streamlit UI =====
st.title("📘 習慣／學習追蹤表單")

with st.form("track_form"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    user = st.selectbox("👤 使用者", user_list, index=user_list.index("Sanny"))
    topic = st.selectbox("🗂️ 主題", topic_list)
    done = st.checkbox("✅ 是否完成", value=False)
    note = st.text_area("📝 備註（可選）")
    
    submitted = st.form_submit_button("📤 提交紀錄")
    
    if submitted:
        # 寫入 Google Sheets
        sheet.append_row([now, user, topic, "✅" if done else "❌", note])
        st.success("✅ 已成功提交紀錄！")

# ===== 顯示最新資料（可選）=====
st.markdown("---")
if st.checkbox("📄 顯示目前追蹤資料"):
    records = sheet.get_all_records()
    st.table(records[::-1])  # 倒著顯示（最新在上）
