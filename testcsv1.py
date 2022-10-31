import pyarrow as pa
from google.oauth2 import service_account
from google.cloud.bigquery_storage import types
from google.cloud.bigquery_storage import BigQueryReadClient

'''
ローカルで実行する場合
gcs_service_account = {
      "type": "service_account",
      "project_id": "project-291031",
      "private_key_id": "464564c7f86786afsa453345dsf234vr32",
      "private_key": "-----BEGIN PRIVATE KEY-----\ndD\n-----END PRIVATE KEY-----\n",
      "client_email": "my-email-address@project-291031.iam.gserviceaccount.com",
      "client_id": "543423423542344334",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/d453/my-email-address@project-291031.iam.gserviceaccount.com"
    }
'''

@st.experimental_memo
def fetch_bq_data():
    '''
    ローカルで実行する場合
    credentials = service_account.Credentials.from_service_account_info(gcs_service_account)
    '''
    
    #クラウド上で実行する場合
    credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
    bqstorage_client = BigQueryReadClient(credentials=credentials)
    
    gcp_project_id = 'gcp-project-id'
    project_id = "bigquery-public-data"
    dataset_id = "new_york_trees"
    table_id = "tree_species"
    table = f"projects/{project_id}/datasets/{dataset_id}/tables/{table_id}"

    read_options = types.ReadSession.TableReadOptions(
        selected_fields=["species_common_name", "fall_color"]
    )

    parent = "projects/{}".format(gcp_project_id)

    requested_session = types.ReadSession(
        table=table,
        data_format=types.DataFormat.ARROW,
        read_options=read_options,
    )

    read_session = bqstorage_client.create_read_session(parent=parent, read_session=requested_session, max_stream_count=1)
    stream = read_session.streams[0]
    reader = bqstorage_client.read_rows(stream.name)

    frames = []
    for message in reader.rows().pages:
        frames.append(message.to_arrow())
    pa_table = pa.Table.from_batches(frames)
    dataframe = pa_table.to_pandas()
    return dataframe
