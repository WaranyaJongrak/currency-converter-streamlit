import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="💱 อัตราแลกเปลี่ยนเงินตรา", page_icon="💵")

st.title("💱 อัตราแลกเปลี่ยนเงินตราระหว่างสกุลเงิน")
st.write("ข้อมูลจากเว็บไซต์ [exchangerate-api.com](https://www.exchangerate-api.com/)")

# ดึงข้อมูลอัตราแลกเปลี่ยนจาก API (USD เป็นฐาน)
url = "https://open.er-api.com/v6/latest/USD"

try:
    response = requests.get(url)
    data = response.json()

    if data["result"] == "success":
        rates = data["rates"]

        # แปลงข้อมูลเป็น DataFrame เพื่อแสดงในตาราง
        df = pd.DataFrame(list(rates.items()), columns=["Currency", "Rate (per 1 USD)"])
        df = df.sort_values("Currency").reset_index(drop=True)

        # -------------------------------------------------------
        # 💰 ส่วนเครื่องคำนวณแปลงค่าเงิน (ตั้งต้นเป็น 1 USD -> THB)
        # -------------------------------------------------------
        st.subheader("💰 เครื่องคำนวณแปลงค่าเงิน")

        # ค่าเริ่มต้น: 1 USD
        amount = st.number_input("กรอกจำนวนเงิน (USD):", min_value=0.0, step=0.01, value=1.0)

        # ค่าเริ่มต้น: THB
        default_index = list(df["Currency"]).index("THB") if "THB" in df["Currency"].values else 0
        target_currency = st.selectbox("เลือกสกุลเงินที่ต้องการแปลง:", df["Currency"].unique(), index=default_index)

        if amount > 0:
            converted = amount * rates[target_currency]
            st.success(f"{amount:.2f} USD = {converted:.2f} {target_currency}")

        st.markdown("---")

        # -------------------------------------------------------
        # 📊 ตารางอัตราแลกเปลี่ยน
        # -------------------------------------------------------
        st.subheader("📊 ตารางอัตราแลกเปลี่ยน (เทียบกับ USD)")
        st.dataframe(df, use_container_width=True)

    else:
        st.warning("⚠️ ไม่สามารถดึงข้อมูลจาก API ได้ในขณะนี้")

except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาด: {e}")
