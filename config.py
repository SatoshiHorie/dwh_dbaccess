from dotenv import load_dotenv
load_dotenv()

import os

HOSTNAME = os.getenv('HOSTNAME') 
USERNAME = os.getenv('USERNAME') 
PASSWORD = os.getenv('PASSWORD') 
DBNAME = os.getenv('DBNAME') 
