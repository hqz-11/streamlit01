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
    st.markdown("# sheet update")
    
    SP_SHEET_KEY = st.secrets.SP_SHEET_KEY.key 
    sh = gc.open_by_key(SP_SHEET_KEY)      
    SP_SHEET = 'Sheet3' 
    worksheet = sh.worksheet(SP_SHEET)
    
    if st.button("sheet check"):
        st.dataframe(worksheet.get_all_values())
        
    st.markdown("# cell追加")
    x1=len(worksheet.get_all_values())
    x2=x1+1
    title1 = st.text_input("keyword")
    title2 = st.text_input("問題")
    title3 = st.text_input("答え1")
    title4 = st.text_input("答え2")
    title5 = st.text_input("答え3")
    
    if st.button("追加"):
        update1 = worksheet.update_cell(x2,1,title1)
        update2 = worksheet.update_cell(x2,2,title2)
        update3 = worksheet.update_cell(x2,3,title3)
        update4 = worksheet.update_cell(x2,4,title4)
        update5 = worksheet.update_cell(x2,5,title5)
        st.write("successful","LAST DATA IS")
        ik = worksheet.row_values(x2)
        st.title(ik)
        
    if st.button("追加消し"):
        cancel = worksheet.delete_rows(x1)
        st.write("successful")
        
    st.markdown("# データ更新")
    title6 = st.text_input("行")
    title7 = st.text_input("列")
    title8 = st.text_input("新し内容")
    
    if st.button("データ更新"):
        update6 = worksheet.update_cell(title6,title7,title8)
        st.write("successful")
     
    st.markdown("# データ消し")
    title9 = st.text_input("消したい行")
    title10 = st.text_input("消したい列")
    
    if st.button("行 消し"):
        update7 = worksheet.delete_rows(title9)
        st.write("successful")
    if st.button("列 消し"):
        update7 = worksheet.delete_cols(title9)
        st.write("successful")
        
       
    
    
