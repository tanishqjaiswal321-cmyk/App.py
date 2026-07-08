import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Janata Voice - People's Priorities", layout="wide")
st.title("🇮🇳 Janata Voice - People's Priorities")
st.subheader("AI-powered feedback platform for MP Office")

try:
    df = pd.read_csv("complaints.csv")
except:
    df = pd.DataFrame(columns=["Category", "Description", "Priority", "Status", "Comment"])

menu = st.sidebar.selectbox("Login as", ["Citizen", "MP Office"])

if menu == "Citizen":
    st.header("📝 Submit Your Issue")
    category = st.selectbox("Category", ["Road", "Water", "Electricity", "Garbage", "Other"])
    desc = st.text_area("Describe the problem")
    photo = st.file_uploader("Upload Photo", type=['jpg','png'])
    
    if st.button("Submit Complaint"):
        priority = random.randint(70, 99)
        new_row = {"Category": category, "Description": desc, "Priority": priority, "Status": "Pending", "Comment": ""}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("complaints.csv", index=False)
        st.success(f"Complaint submitted! AI Priority Score: {priority}/100")
        st.balloons()

else:
    st.header("🔐 MP Office Dashboard")
    user = st.text_input("Username")
    passw = st.text_input("Password", type="password")
    
    if user == "mpadmin" and passw == "1234":
        st.success("Logged in")
        st.subheader("All Complaints")
        
        for i, row in df.iterrows():
            with st.expander(f"{row['Category']} | Priority: {row['Priority']} | Status: {row['Status']}"):
                st.write(f"**Issue:** {row['Description']}")
                new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Resolved"], index=["Pending", "In Progress", "Resolved"].index(row['Status']), key=i)
                comment = st.text_input("Reply to Citizen", row['Comment'], key=f"c{i}")
                
                if st.button("Update", key=f"b{i}"):
                    df.loc[i, 'Status'] = new_status
                    df.loc[i, 'Comment'] = comment
                    df.to_csv("complaints.csv", index=False)
                    st.success("Updated!")
                    st.rerun()
    elif user:
        st.error("Wrong credentials")