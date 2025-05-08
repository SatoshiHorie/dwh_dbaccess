from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import schemas.ktqdatabase as emergency_transport_Schema
import models.emergencytransport as emergency_transport_model

# ==================================================
# 非同期CRUD処理
# ==================================================
# 新規登録
async def insert_emergency_transport(
        db_session: AsyncSession,
        Emergency_transport_data: emergency_transport_Schema.emergency_transport_Schema) -> emergency_transport_model.Emergency_transport:
    """
        新しい救急搬送状況をデータベースに登録する関数
        Args:
        db_session (AsyncSession): 非同期DBセッション
        Emergency_transport_data (InsertAndUpdate_emergency_transport_Schema): 作成する救急搬送状況のデータ
        Returns:
        Emergency_transport: 作成された救急搬送状況のモデル
    """
    print("=== 新規登録：開始 ===")
    new_emergency_transport = emergency_transport_model.Emergency_transport(**Emergency_transport_data.model_dump())
    db_session.add(new_emergency_transport)
    await db_session.commit()
    await db_session.refresh(new_emergency_transport)
    print(">>> データ追加完了")
    return new_emergency_transport

# 全件取得
async def get_emergency_transports(db_session: AsyncSession) -> list[emergency_transport_model.Emergency_transport]:
    """
        データベースから全ての救急搬送状況を取得する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
        Returns:
            list[emergency_transport_model.Emergency_transport]: 取得された全ての救急搬送状況のリスト
    """
    print("=== 全件取得：開始 ===")
    result = await db_session.execute(select(emergency_transport_model.Emergency_transport))
    emergency_transports = result.scalars().all()
    print(">>> データ全件取得完了")
    return emergency_transports

# 1件取得
async def get_emergency_transport_by_pk(db_session: AsyncSession,
        year: int,
        Dispatch_Transport: str,
        Type: str) -> emergency_transport_model.Emergency_transport | None:
    """
        データベースから特定の救急搬送状況を1件取得する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
            year (int): 年次（プライマリキー）
            Dispatch_Transport (str): 出動と搬送の区分（プライマリキー）
            Type (str): 類型（プライマリキー）
            Emergency_transport | None: 取得された救急搬送状況のモデル、救急搬送状況が存在しない場合はNoneを返す
    """
    print("=== １件取得：開始 ===")
    print(type(emergency_transport_model.Emergency_transport.year))
    print(type(year))
    result = await db_session.execute(
    select(emergency_transport_model.Emergency_transport).where((emergency_transport_model.Emergency_transport.year == year)
                                                                & (emergency_transport_model.Emergency_transport.Dispatch_Transport == Dispatch_Transport)
                                                                & (emergency_transport_model.Emergency_transport.Type == Type)))
    emergency_transport = result.scalars().first()
    print(">>> データ取得完了")
    return emergency_transport

# 更新処理
async def update_emergency_transport(
        db_session: AsyncSession,
        year: int,
        Dispatch_Transport: str,
        Type: str,
        target_data: emergency_transport_Schema.emergency_transport_Schema) -> emergency_transport_model.Emergency_transport | None:
    """
        データベースの救急搬送状況を更新する関数
        Args:
            year (int): 年次（プライマリキー）
            Dispatch_Transport (str): 出動と搬送の区分（プライマリキー）
            Type (str): 類型（プライマリキー）
        Returns:
            Emergency_transport | None: 更新された救急搬送状況のモデル、救急搬送状況が存在しない場合はNoneを返す
    """
    print("=== データ更新：開始 ===")
    emergency_transport = await get_emergency_transport_by_pk(db_session, year, Dispatch_Transport, Type)
    if emergency_transport:
        emergency_transport.year = target_data.year
        emergency_transport.Dispatch_Transport = target_data.Dispatch_Transport
        emergency_transport.Type = target_data.Type
        emergency_transport.Number = target_data.Number
        await db_session.commit()
        await db_session.refresh(emergency_transport)
        print(">>> データ更新完了")
        
    return emergency_transport

# 削除処理
async def delete_emergency_transport(
        db_session: AsyncSession,
        year: int,
        Dispatch_Transport: str,
        Type: str
        ) -> emergency_transport_model.Emergency_transport | None:
    """
        データベースの救急搬送状況を削除する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
            year (int): 年次（プライマリキー）
            Dispatch_Transport (str): 出動と搬送の区分（プライマリキー）
            Type (str): 類型（プライマリキー）
        Returns:
            Emergency_transport | None: 削除された救急搬送状況のモデル、救急搬送状況が存在しない場合はNoneを返す
    """
    print("=== データ削除：開始 ===")
    emergency_transport = await get_emergency_transport_by_pk(db_session, year, Dispatch_Transport, Type)
    if emergency_transport:
        await db_session.delete(emergency_transport)
        await db_session.commit()
        print(">>> データ削除完了")
    
    return emergency_transport