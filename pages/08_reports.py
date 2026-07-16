import streamlit as st

from src.dashboard.utils.db import (
    get_documents,
    get_companies
)

st.title("📄 Annual Reports")

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

selected = companies[
    companies["company_name"] == company
].iloc[0]

docs = get_documents()

docs = docs[
    docs["company_id"] == selected["id"]
]

if docs.empty:

    st.warning("No Annual Reports Available.")

else:

    for _, row in docs.iterrows():

        col1, col2 = st.columns([1,4])

        col1.write(f"📅 {row['year']}")

        col2.link_button(
            "Open Annual Report",
            row["annual_report"]
        )