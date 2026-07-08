import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Janata Voice", layout="wide")
st.title("🇮🇳 Janata Voice - People's Priorities")
st.write("AI-powered feedback for MP Office")

# File load
try:
    df = pd.read_csv("complaints.csv")
except:
    df = pd.DataFrame(columns=["Category", "Description", "Priority", "Status", "Comment"])

# Sidebar Login
menu = st.sidebar.selectbox("Login as", ["Citizen", "MP Office"])

if menu == "Citizen":
    st.header("📝 Submit Your Issue")
    category = st.selectbox("Category", ["Road", "Water", "Electricity", "Garbage", "Other"])
    desc = st.text_area("Describe the problem")
    
    if st.button("Submit Complaint"):
        priority = random.randint(70, 99)
        new_row = {"Category": category, "Description": desc, "Priority": priority, "Status": "Pending", "Comment": ""}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("complaints.csv", index=False)
        st.success(f"Submitted! AI Priority: {priority}/100")

else:
    st.header("🔐 MP Office Dashboard")
    user = st.text_input("Username")
    passw = st.text_input("Password", type="password")
    
    if user == "mpadmin" and passw == "1234":
        st.success("Logged in successfully")
        st.dataframe(df) # Saari complaints table me
        
        st.subheader("Reply to Complaint")
        idx = st.number_input("Complaint Number", 0, len(df)-1)
        new_status = st.selectbox("Status", ["Pending", "In Progress", "Resolved"])
        comment = st.text_area("Your Reply")
        
        if st.button("Update & Answer"):
            df.loc[idx, 'Status'] = new_status
            df.loc[idx, 'Comment'] = comment
            df.to_csv("complaints.csv", index=False)
            st.success("Answer submitted!")
    elif user:
        st.error("Wrong credentials")