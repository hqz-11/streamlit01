import streamlit as st
import pandas as pd
#pip install openpyxl


# Create API client.

st.markdown("# keywordsraech")

#input your xlsx path
df = pd.read_excel("test.xlsx", engine='openpyxl')

#アイテムの選択を作る
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
