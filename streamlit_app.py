import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(page_title="Janata Voice", layout="wide")
st.title("🇮🇳 Janata Voice - People's Priorities")
st.write("AI-powered feedback for MP Office")

# File load
CSV_FILE = "complaints.csv"

if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["Category", "Description", "Priority", "Status", "Comment"])

# Sidebar Login
menu = st.sidebar.selectbox("Login as", ["Citizen", "MP Office"])

# --- CITIZEN INTERFACE ---
if menu == "Citizen":
    st.header("📝 Submit Your Issue")
    category = st.selectbox("Category", ["Road", "Water", "Electricity", "Garbage", "Other"])
    desc = st.text_area("Describe the problem")
    
    if st.button("Submit Complaint"):
        if desc.strip() == "":
            st.error("Please describe the problem before submitting.")
        else:
            priority = random.randint(70, 99)
            new_row = {
                "Category": category, 
                "Description": desc, 
                "Priority": priority, 
                "Status": "Pending", 
                "Comment": ""
            }
            # Append and save
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(CSV_FILE, index=False)
            st.success(u"✅ Complaint submitted successfully! Priority Score: " + str(priority))

# --- MP OFFICE INTERFACE ---
elif menu == "MP Office":
    st.header("🏢 MP Office Dashboard")
    st.subheader("Submitted Complaints")
    
    if df.empty:
        st.info("No complaints registered yet.")
    else:
        st.dataframe(df, use_container_width=True)