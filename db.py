import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config

# ==================================================
# DBアクセス
# ==================================================
# ベースクラスの定義
Base = declarative_base()

# DBファイル作成
base_dir = os.path.dirname(__file__)
# データベースのURL

hostname = config.HOSTNAME 
username = config.USERNAME 
password = config.PASSWORD
dbname = config.DBNAME 

SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://" + username + ":" + password + "@" + hostname + "/" + dbname

# 非同期エンジンの作成
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

# 非同期セッションの設定
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# DBとのセッションを非同期的に扱うことができる関数
async def get_dbsession():
    db = async_session()
    try:
        yield db
    finally:
        db.close()