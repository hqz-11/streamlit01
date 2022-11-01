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
    content = bucket.blob(file_path).download_as_string().decode('utf-8', errors='ignore')
    return content

bucket_name = "streamlit-kann"
file_path = "test.xlsx"

df = read_file(bucket_name, file_path)

# Print results.
keyword= df['keyword'].unique().tolist()
mondai = df['問題'].unique().tolist()
k_select = st.sidebar.selectbox("keywordを選択してください", keyword)
m_select = st.sidebar.selectbox("問題を選択してください", mondai)
result_df = df[(df['keyword'] == k_select) & (df['問題'] == m_select)]

#回答を出力する
if len(result_df) == 0:
    st.write("答えはありません")
else:
    st.write("答えの例： ")
    for i in range(len(result_df)):
        st.write(result_df["答え1"].values[i])
        st.write(result_df["答え2"].values[i])
        st.write(result_df["答え3"].values[i])
