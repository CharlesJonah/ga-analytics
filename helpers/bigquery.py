from google.cloud import bigquery
from google.oauth2 import service_account

from constants import config

credentials = service_account.Credentials.from_service_account_file(
    config.GOOGLE_APPLICATION_CREDENTIALS
)

client = bigquery.Client(credentials=credentials, project=config.PROJECT_ID)
