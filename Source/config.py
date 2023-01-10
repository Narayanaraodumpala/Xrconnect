# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/xrconn_xrcoreflaskdb' #mysql://username:password@server/db 




#  db connection for xrconnect(B2C)

# mysql://username:password@server/db

# dev
# SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://xrconnect_b2c_dev:Hyderabad1990@20.204.30.104/xrconnect_b2c_dev'

# qa
#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://xrconnect_b2c_qa:Hyderabad1991@20.204.30.104/xrconnect_b2c_qa' #mysql://username:password@server/db

# prod
# SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://xrconnect_prod:Reinvision2021@20.204.30.104/xrconnect_prod' #mysql://username:password@server/db

#localhoat
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/stage_server' #mysql://username:password@server/db

#Azure MySQL
#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://rimysqlsuperuser:d3AbW!n75s@ri-mysql-server-dev.mysql.database.azure.com/xrconnect-dev-db' 

SQLALCHEMY_ENGINE_OPTIONS = {
    'connect_args': {
        'connect_timeout': 10
    }
}

DATABASE_CONNECT_OPTIONS = {}
UPLOAD_FOLDER = "."
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

# account_name = "xrdemo"
# account_key = "6ENSAfOyVGzLff0sOk8bsAspMnXYdju7OjjZefgshK9y+Xv387ZR0RpYXexCG6/i0bqOIcR6RTu/+AStTUrfDg=="
# private_container_name = "xrconnect-demo"
# public_container_name = "public-container"

# app_build_quest_uri='app-build-quest'
# app_build_windows_uri='app-build-windows'

account_name = "xrconnect-kv-dev"
account_key = "GZw8Q~hyBhT3OmiOw4u8VS6dFWN7ffLdnc22~dx7"
private_container_name = "storage-container"
public_container_name = "storage-container-public"


from os import environ as env
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

TENANT_ID = env.get("AZURE_TENANT_ID", "123f33de-6961-4fb3-bf2e-e00548e0e982")
CLIENT_ID = env.get("AZURE_CLIENT_ID", "cedcc728-d32b-46ab-9327-3ab64f5fcf93")
CLIENT_SECRET = env.get("AZURE_CLIENT_SECRET", "GZw8Q~hyBhT3OmiOw4u8VS6dFWN7ffLdnc22~dx7")

KEYVAULT_NAME = env.get("AZURE_KEYVAULT_NAME", "xrconnect-kv-dev")
KEYVAULT_URI = f"https://{KEYVAULT_NAME}.vault.azure.net/"


_credential = ClientSecretCredential(
    tenant_id=TENANT_ID,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

#private_container_name = "storage-container"
#public_container_name = "storage-container-public"
_sc = SecretClient(vault_url=KEYVAULT_URI, credential=_credential)

retrieved_secret = _sc.get_secret('api-base-url')
# print('retrieved  secret=',retrieved_secret.value)

app_build_quest=_sc.get_secret('app-build-quest')
app_build_quest_value=app_build_quest.value


app_build_windows=_sc.get_secret('app-build-windows')
app_build_windows_value=app_build_windows.value


private_container_name=_sc.get_secret('storage-container')
private_container_value=private_container_name.value


public_container_name=_sc.get_secret('storage-container-public')
public_container_value=public_container_name.value


storage_account_name=_sc.get_secret('storage-account')
storage_account_value=storage_account_name.value



smtp_email=_sc.get_secret('smtp-email')
smtp_email_value=smtp_email.value


smtp_from_name=_sc.get_secret('smtp-from-name')
smtp_from_name_value=smtp_from_name.value


smtp_host=_sc.get_secret('smtp-host')
smtp_host_value=smtp_host.value


smtp_password=_sc.get_secret('smtp-password')
smtp_password_value=smtp_password.value


smtp_port=_sc.get_secret('smtp-port')
smtp_port_value=smtp_port.value


front_base_url=_sc.get_secret('front-base-url')
front_base_url_value=front_base_url.value


api_base_url=_sc.get_secret('api-base-url')
api_base_url_value=api_base_url.value

storage_account_key=_sc.get_secret('storage-account-key')
storage_account_key_value=storage_account_key.value

google_login_key=_sc.get_secret('google-login-key')
google_login_key_value=google_login_key.value


facebook_key=_sc.get_secret('facebook-key')
facebook_key_value=facebook_key.value

webgl_link=_sc.get_secret('webgl-link')
webgl_link_value=webgl_link.value