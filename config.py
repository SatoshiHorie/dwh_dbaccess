from dotenv import load_dotenv
load_dotenv()

import os

HOSTNAME = os.getenv('HN') 
USERNAME = os.getenv('UN') 
PASSWORD = os.getenv('PW') 
DBNAME = os.getenv('DN') 
