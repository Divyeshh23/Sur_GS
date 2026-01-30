import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Setup Connection
# Use the URL of your Google Sheet here
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Qq_EWY8lM-QtcydurVaqMhYQMKpAHd-CXfHNdP15Gao/edit?gid=0#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

# UI Layout
st.set_page_config(page_title="Surgery Register", layout="centered")
st.title("🏥 Surgery Register to Google Sheets")

with st.form("entry_form", clear_on_submit=True):
    date = st.date_input("Date")
    branch = st.selectbox("Branch Name", ["Saidapet","Chrompet","Madipakkam","Perambur","Ambattur","Vadapalani","Neelankarai","Tondiarpet","Tambaram","Pondicherry"])
    
    cataract = st.text_input("Cataract")
    refractive = st.text_input("Refractive")
    vr = st.text_input("VR Sur")
    inj = st.text_input("VR Inj")
    others = st.text_input("Others")
    value = st.text_input("Total Surgery Value")
    remarks = st.text_area("Remarks")
    
    submitted = st.form_submit_button("Submit Record")

    if submitted:
        def to_int(val):
            val = val.strip()
            return int(val) if val.isdigit() else 0

        # Create a new row of data
        new_data = pd.DataFrame([{
            "Date": str(date),
            "Branch": branch,
            "Cataract": to_int(cataract),
            "Refractive": to_int(refractive),
            "VR Sur": to_int(vr),
            "VR Inj": to_int(inj),
            "Other Sur": to_int(others),
            "Total Value": to_int(value),
            "Remarks": remarks
        }])

        # Fetch existing data and append
        try:
            existing_data = conn.read(spreadsheet=SHEET_URL)
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            conn.update(spreadsheet=SHEET_URL, data=updated_df)
            st.success("🔥 Data saved directly to Google Sheets!")
        except Exception as e:
            st.error(f"Error: {e}")

# View Section
if st.checkbox("Show Google Sheet Records"):
    data = conn.read(spreadsheet=SHEET_URL)
    st.dataframe(data)