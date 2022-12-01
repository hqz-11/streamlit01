import streamlit as st
from google.oauth2 import service_account
import gspread
import pandas as pd

#必要なアクセス権を取る、キー(gcp_service_account)はstreamlit cloudに保存されている
scopes = [ 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'
]
credentials = service_account.Credentials.from_service_account_info( st.secrets["gcp_service_account"], scopes=scopes
)
gc = gspread.authorize(credentials)


#パスワード確認
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
    SP_SHEET_KEY = st.secrets.SP_SHEET_KEY.key #キー(SP_SHEET_KEY)はstreamlit cloudに保存されている
    sh = gc.open_by_key(SP_SHEET_KEY)#スプレッドシートキーを指定してワークブックを選択
    SP_SHEET = 'Sheet4' #スプレッドシートキーを指定してワークブックを選択
    worksheet = sh.worksheet(SP_SHEET)
    data = worksheet.get_all_values() #ワークシートの値の全てを多次元配列に格納する
    df = pd.DataFrame(data[1:], columns=data[0])
    st.markdown("# keywordsraech")
    kw= df['キーワード'].unique().tolist()#この列の各カテゴリの名前を返し、リストに変換します
    stm = df['質問'].unique().tolist()#この列の各カテゴリの名前を返し、リストに変換します
    k_select = st.sidebar.selectbox("キーワードを選択してください", kw)#選択ボックスとラジオボタンを追加する
    s_select = st.sidebar.selectbox("質問を選択してください", stm)#選択ボックスとラジオボタンを追加する
    result_df = df[(df['キーワード'] == k_select) & (df['質問'] == s_select)]

    if len(result_df) == 0:
        st.write("答えはありません")
    else:
        st.write("答えの例： ")
        for i in range(len(result_df)):
            st.write(result_df["回答"].values[i])
            st.write("性別：",result_df["性別"].values[i])
            st.write("ファイル名：",result_df["ファイル名"].values[i])

    st.markdown("# SHEET UPDATE URL :")
    st.header('https://hqz-11-streamlit01-update-hztko3.streamlit.app/')
