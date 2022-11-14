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
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():
    SP_SHEET_KEY = st.secrets.SP_SHEET_KEY.key 
    sh = gc.open_by_key(SP_SHEET_KEY)      
    SP_SHEET = 'Sheet3' 
    worksheet = sh.worksheet(SP_SHEET)
    list = worksheet.get_all_values()
    x1=len(list)
    x2=x1+1
    st.title("keyword:1"
            "問題:2"
            "答え1:3"
            "答え2:4"
            "答え3:5")
    title1 = st.text_input("内容","内容")
    title2 = st.text_input("内容","内容")
    title3 = st.text_input("内容","内容")
    title4 = st.text_input("内容","内容")
    title5 = st.text_input("内容","内容")
    if st.button("update"):
        update1 = worksheet.update_cell(x2,5,title1)
        update2 = worksheet.update_cell(x2,1,title2)
        update3 = worksheet.update_cell(x2,2,title3)
        update4 = worksheet.update_cell(x2,3,title4)
        update5 = worksheet.update_cell(x2,4,title5)
       
    
    