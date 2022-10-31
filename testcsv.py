# streamlit_app.py
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
# Create API client.
gcp_service_account={
  "type": "service_account",
  "project_id": "wise-reporter-319902",
  "private_key_id": "af56e388d7365a7ec88d1158c1090f15c5202ab8",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQD0XY+nK88AM6WM\nWPD4mAzJDxkKKoY+Btpj5gGV4gflOmhIQVqz7ww/pknWKDhq18Qu1GByc08zU2Du\n65hsoS+ccnP2y+CaScLr5EwZJYmqb7S++2Q/Uz91BQMVDwl96MHfO9EAfXaJ7PcH\na4W4CjdmQAomCTMmhbUUHptu6iE0yIR5XRNvKbjSH39r+ggPm6DnYO3s2Q70XP9z\npv6xoERTSKlzm4E5CEuNnq/K2YDXS6stFWpzTUe8+FglbxO04CNNk9xuDGoH50PH\nAj6YtMqh2nNTTjoOBGtlwubjUIudd5Fh6gmP+7PB0FR8OlQgTAjVI/87DzmbDq9u\nwf/s4NB5AgMBAAECggEABLy2zwKTQ3l81iztVPW4E0mgHJ0I7QOCuAjjhOyRLchn\nG6CXKAU0Z8brAQRIiF7Q7lMkCyvy6r6pkrOxHixuiP2grmBrz6ZU6X5Ed/JwmDzT\nvwmAEIiJsOnpp4XT6JVsdPFuVFPoikpX9w1Gh8JKuHoHuhze0lbiRswn4IDfmRaQ\n5KRTjkluJC5DXeoqB6uPx7U8AKGRImHnbI6MSCFh/PVJA1Cv3WEd/ow0wKaPw0Zf\nuHftHKf+o++Hi5I7faXCAJFJ2funYx02XzE9nzCetjPySDfklVX4nEUFc+D3F788\n4NmG6fmFHDmFMk4cu5MxnghLQpckkolzjjvpVRkapQKBgQD+cV2G8RBjG/2ALpTu\n3bakxJen94oZpKRX0DjqwmZSAFEJVqTBVErgLUrrk+cV+XYt0OG3Olz+bHcLLuaI\nbNfMRHQR300/FBjHDI2b1bQoNzJNHm6Btd7XofbKpXoKuEfLFjHvI1QSvQGCCGJ+\nYM9uBpittbAevCAlhFGvOr7r9QKBgQD13GhbJxTxu+URO42CopZTdbHlZOW7p0ml\nHzfW+ni6paOchZpPEAbf8y4knc4oyP713GHcZr3XKAw4zGAKkc3f9kaXNzA5Y7sc\ny16/uXpIJZPifeS/RyjRUE+zb92YZmYjNAL5dkosASBpbYo9GiMmgFuVF22XYkhT\n1OhC7Lyj9QKBgCmUsSoaPwlTS6wk8KXQicaHchk69NCX/Vt0ZbjHqB0CfDvAcxA9\nDDdyb2nsM7l9mPiHyDs/SG8znoivU3E8CFATZ7x79421ZQ8yV/n9hIGF86xyqrB7\n3jzy9PfM7xLNZr4jlGl2JokhZhuv7xikDYH3hf/tTyjWqZI3+3ldalH5AoGBAKNy\nyQm4XKssX+fp8HTlhAyuFPtM7ZGocERPEb9gurxS/AdFpsVjAT8HGykKpBDnNuDa\nh1CQGSsdm6py7HJ6ZiS7REipTu0ISU+mQDIzq4ClQsBzM4yaUR9+Rc4j02zKvqIu\npL+VjU/d299bDGj8pFunP7tJXPkkRLM+ur4rRmm1AoGAcv5Tu/6JFkL/DS8V2Tam\ngxwmSOLq1bkk2vWqz3tC3OUuuWkIhR1RV7dlN5RD127w1lifsKgijFWaKgxICfk8\nv+azHGsXGG3ueaW03FnJmsotqgtm1oac+aQg2WLSVJAjd+o2MePJTGPGQBRLE+kf\n2qNzhDT9cwUt/J+UFAXtxF8=\n-----END PRIVATE KEY-----\n",
  "client_email": "kann-547@wise-reporter-319902.iam.gserviceaccount.com",
  "client_id": "107447072525822971618",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/kann-547%40wise-reporter-319902.iam.gserviceaccount.com"
}

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.experimental_memo to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

rows = run_query("SELECT keyword FROM `wise-reporter-319902.testdate.testxlsx` LIMIT 10")

# Print results.
st.write("Some wise words from Shakespeare:")
for row in rows:
    st.write("✍️ " + row['keyword'])