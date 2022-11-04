import streamlit as st
from google.oauth2 import service_account
import gspread
import pandas as pd

scopes = [ 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'
]
credentials = service_account.Credentials.from_service_account_info( st.secrets["gcp_service_account"], scopes=scopes
)
gc = gspread.authorize(credentials)

SP_SHEET_KEY = st.secrets.SP_SHEET_KEY.key 
sh = gc.open_by_key(SP_SHEET_KEY)
SP_SHEET = 'Sheet1' 
worksheet = sh.worksheet(SP_SHEET)
data = worksheet.get_all_values() 
df = pd.DataFrame(data[1:], columns=data[0])

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "パスワードを入れてください", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "パスワードを入れてください", type="password", on_change=password_entered, key="password"
        )
        st.error("パスワードが違う")
        return False
    else:
        # Password correct.
        return True

if check_password():
    st.markdown("# keywordsraech")
    keyword= df['keyword'].unique().tolist()
    mondai = df['問題'].unique().tolist()
    k_select = st.sidebar.selectbox("keywordを選択してください", keyword)
    m_select = st.sidebar.selectbox("問題を選択してください", mondai)
    result_df = df[(df['keyword'] == k_select) & (df['問題'] == m_select)]

    if len(result_df) == 0:
        st.write("答えはありません")
    else:
        st.write("答えの例： ")
        for i in range(len(result_df)):
            st.write(result_df["答え1"].values[i])
            st.write(result_df["答え2"].values[i])
            st.write(result_df["答え3"].values[i]) 