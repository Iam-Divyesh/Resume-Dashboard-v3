import streamlit as st
import pandas as pd
import math
import webbrowser
import urllib.parse
import pyperclip

st.set_page_config(page_title="Candidate Search Dashboard", layout="wide")

# === Load CSV Data ===
@st.cache_data
def load_data():
    return pd.read_csv("version3.csv")

df = load_data()

# === Sidebar Filters ===
st.sidebar.header("🔍 Search Filters")

# Required Role field
role = st.sidebar.text_input("Role (required)", placeholder="e.g., Data Entry")

# Optional filters
name = st.sidebar.text_input("Name (optional)", placeholder="e.g., Tushar")
location = st.sidebar.text_input("Location (optional)", placeholder="e.g., Surat")
area = st.sidebar.text_input("Area (optional)", placeholder="e.g., Katargam")
contact = st.sidebar.text_input("Number (optional)", placeholder="e.g., 1112223334")
gender_options = {
    "All": None,  # No filter for 'All'
    "Male": 5,
    "Female": 1
}

religion = st.sidebar.selectbox(
    "Gender",
    ["Hindu","Muslim"]
)

# The new dropdown select box
gender_selection = st.sidebar.selectbox(
    "Gender",
    list(gender_options.keys())
)


# if not role.strip():
#     st.sidebar.warning("⚠️ Please enter a role to search.")
#     st.stop()

# === Filter Logic ===
filtered_df = df[df["Job Type"].str.contains(role, case=False, na=False)]

if name:
    filtered_df = filtered_df[filtered_df["Name"].str.contains(name, case=False, na=False)]

if location:
    filtered_df = filtered_df[filtered_df["City"].str.contains(location, case=False, na=False)]

filtered_df["Contact"] = filtered_df["Contact"].astype(str)

if contact:
    
    filtered_df = filtered_df[filtered_df["Contact"].str.fullmatch(contact, case=False, na=False)]
    
if area:
    filtered_df = filtered_df[filtered_df["Area"].str.contains(area, case=False, na=False)]

if religion:
    filtered_df = filtered_df[filtered_df["Religion"].str.contains(religion, case=False, na=False)]

selected_gender_value = gender_options[gender_selection]
if selected_gender_value is not None:
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender_value]

# === Pagination ===
results_per_page = 10
total_results = len(filtered_df)
total_pages = math.ceil(total_results / results_per_page)

st.markdown(f"### Showing {total_results} result(s) for role: **{role}**")

# Page selector
page = st.number_input("Page", min_value=1, max_value=max(total_pages, 1), step=1)

# Slice results
start = (page - 1) * results_per_page
end = start + results_per_page

# === Display Each Candidate ===
for idx, row in filtered_df.iloc[start:end].iterrows():
    with st.container():
        col1, col2 , col3 = st.columns([2,2,1])
        with col1:
            gender_value = row.get('Gender', 'N/A')
            gender_display = "Male" if gender_value == 5 else "Female" if gender_value != 'N/A' else 'N/A'
            st.markdown(f"""
                ### {row.get('Name', 'N/A')}                  
                **Role:** {row.get('Job Type', 'N/A')}  
                **Location:** {row.get('City', 'N/A')}  
            """)
            Copy,sample = st.columns([1,1])
            with Copy:
                st.code(row.get('Name', 'N/A'))
                st.code(row.get('Contact', 'N/A'))
            with sample:
                pass
        
        with col2:
            st.markdown(f"""
                **Area:** {row.get('Area', 'N/A')}  
                **Mobile.No:** {row.get('Contact', 'N/A')}  
                **Experience:** {row.get('Experience', 'N/A')}  
                **Gender:** {gender_display}    
                **Religion:** {row.get('Religion', 'N/A')}  
            """)

        with col3:
            resume_link = row.get("Resume") or row.get("resume_url") or ""
            if pd.notna(resume_link) and resume_link.strip() != "":
                resume_button_key = f"resume_btn_{idx}"
                if st.button("📄 Open Resume", key=resume_button_key):
                    js = f"window.open('{resume_link}')"
                    st.components.v1.html(f"<script>{js}</script>", height=0)
            else:
                st.write("❌ No Resume")

            # WhatsApp button logic
            mobile = str(row.get("Contact", "")).strip().replace(" ", "").replace("+91", "").replace("-", "")

            if pd.notna(mobile) and mobile.isdigit() and len(mobile) == 10:
                message = f"Hi {row.get('Name','N/A')}" 
                encoded_message = urllib.parse.quote(message)
                whatsapp_url = f"https://web.whatsapp.com/send?phone=91{mobile}&text={encoded_message}"
                whatsapp_button_key = f"whatsapp_btn_{idx}"
                if st.button("💬 WhatsApp", key=whatsapp_button_key):
                    js = f"window.open('{whatsapp_url}')"
                    st.components.v1.html(f"<script>{js}</script>", height=0)
            else:
                st.write("❌ No WhatsApp Number")

        st.markdown("---")


# === Footer ===
st.markdown("Made with ❤️ using Streamlit")
