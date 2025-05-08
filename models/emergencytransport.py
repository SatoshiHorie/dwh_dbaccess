from sqlalchemy import Column, Integer, String
from db import Base

# ==================================================
# モデル
# ==================================================
# emergency_transportテーブル用：モデル
class Emergency_transport(Base):
    # テーブル名
    __tablename__ = "emergency_transport"
    # 年次：PK
    year = Column(Integer, primary_key=True)
    # 出動と搬送の区分：PK
    Dispatch_Transport = Column(String(45), primary_key=True)
    # 類型：PK
    Type = Column(String(45), primary_key=True)
    # 件数
    Number = Column(Integer)