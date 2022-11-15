import streamlit as st
from google.oauth2 import service_account
import gspread
import pandas as pd
import time

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
    st.markdown("# sheet update")
    st.title("enterを押してください")
    ik = worksheet.row_values(x1)
    st.text(ik)
    title1 = st.text_input("keyword")
    title2 = st.text_input("問題")
    title3 = st.text_input("答え1")
    title4 = st.text_input("答え2")
    title5 = st.text_input("答え3")
    if st.button("update"):
        update1 = worksheet.update_cell(x2,1,title1)
        update2 = worksheet.update_cell(x2,2,title2)
        update3 = worksheet.update_cell(x2,3,title3)
        update4 = worksheet.update_cell(x2,4,title4)
        update5 = worksheet.update_cell(x2,5,title5)
        st.write("successful update")
        ik = worksheet.row_values(x1)
        st.write("date",ik)
    if st.button("cancel"):
        cancel = worksheet.delete_rows(x1)
        st.write("successful cancel")
        
       
    
    
