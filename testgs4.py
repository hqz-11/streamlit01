import streamlit as st
from google.oauth2 import service_account
import gspread
import pandas as pd

scopes = [ 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'
]
credentials = service_account.Credentials.from_service_account_info( st.secrets["gcp_service_account"], scopes=scopes
)
gc = gspread.authorize(credentials)



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
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("π Password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():
    st.title("# keywordsearch")
    SP_SHEET_KEY = st.secrets.SP_SHEET_KEY.key 
    sh = gc.open_by_key(SP_SHEET_KEY) 
    SP_SHEET = 'Sheet3'
    worksheet = sh.worksheet(SP_SHEET)
    data = worksheet.get_all_values() 
    df = pd.DataFrame(data[1:], columns=data[0])
    keyword= df['keyword'].unique().tolist()
    mondai = df['ει‘'].unique().tolist()
    k_select = st.sidebar.selectbox("keywordγιΈζγγ¦γγ γγ", keyword)
    m_select = st.sidebar.selectbox("ει‘γιΈζγγ¦γγ γγ", mondai)
    result_df = df[(df['keyword'] == k_select) & (df['ει‘'] == m_select)]

    if len(result_df) == 0:
        st.write("η­γγ―γγγΎγγ")
    else:
        st.write("η­γγ?δΎοΌ ")
        for i in range(len(result_df)):
            st.write(result_df["η­γ1"].values[i])
            st.write(result_df["η­γ2"].values[i])
            st.write(result_df["η­γ3"].values[i])
            
            
            
    st.title("# SHEET UPDATE URL")
    st.header('https://hqz-11-streamlit01-update-hztko3.streamlit.app/')
    
        
            
    
    
