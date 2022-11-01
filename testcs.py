# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account
from google.cloud import storage

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)

# Retrieve file contents.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def read_file(bucket_name, file_path):
    bucket = client.bucket(bucket_name)
    content = bucket.blob(file_path).download_as_string().decode("utf-8")
    return content

bucket_name = "streamlit-kann"
file_path = "test.xlsx"

content = read_file(bucket_name, file_path)

# Print results.
for line in content.strip().split("\n"):
    keyword, 問題 = line.split(",")
    st.write(f"{keyword} has a :{問題}:")