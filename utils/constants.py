import configparser
import os
parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '../config/config.conf'))


SECRET = parser.get('api_keys', 'Client_Secret')
CLIENT_ID = parser.get('api_keys', 'Client_ID')

DATABASE_HOST =  parser.get('database', 'database_host')
DATABASE_NAME =  parser.get('database', 'database_name')
DATABASE_PORT =  parser.get('database', 'database_port')
DATABASE_USER =  parser.get('database', 'database_username')
DATABASE_PASSWORD =  parser.get('database', 'database_password')

AZURE_STORAGE = parser.get('azure', 'AZURE_STORAGE_ACCOUNT')
AZURE_KEY= parser.get('azure', 'AZURE_ACCOUNT_KEY')
