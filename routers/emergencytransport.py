from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.ktqdatabase import emergency_transport_Schema, ResponseSchema
import cruds.emergencytransport as emergencytransport_crud
import db

# ルーターを作成し、タグとURLパスのプレフィックスを設定
router = APIRouter(tags=["Emergencytransports"], prefix="/emergencytransports")

# ==================================================
# 救急搬送状況用のエンドポイント
# ==================================================
# 救急搬送状況新規登録のエンドポイント
@router.post("/", response_model=ResponseSchema)
async def create_emergency_transport(emergencytransport: emergency_transport_Schema,
                    db: AsyncSession = Depends(db.get_dbsession)):
    try:
        # 新しいメモをデータベースに登録
        await emergencytransport_crud.insert_emergency_transport(db, emergencytransport)
        return ResponseSchema(message="救急搬送状況が正常に登録されました")
    except Exception as e:
        # 登録に失敗した場合、HTTP 400エラーを返す
        raise HTTPException(status_code=400, detail="救急搬送状況の登録に失敗しました。")

# 救急搬送状況情報全件取得のエンドポイント
@router.get("/", response_model=list[emergency_transport_Schema])
async def get_emergency_transports_list(db: AsyncSession = Depends(db.get_dbsession)):
    # 全ての救急搬送状況をデータベースから取得
    get_emergency_transports = await emergencytransport_crud.get_emergency_transports(db)
    return get_emergency_transports

# 特定の救急搬送状況情報取得のエンドポイント（PK指定）
# year, Dispatch_Transport, TypeをPKとして指定
@router.get("/{keys}", response_model=emergency_transport_Schema)
async def get_emergency_transport_detail(keys: str,
                                         db: AsyncSession = Depends(db.get_dbsession)):
    # PKを分解して取得
    year = int(keys.split("-")[0])
    Dispatch_Transport = keys.split("-")[1]
    Type = keys.split("-")[2]
    # 指定されたPKの救急搬送状況をデータベースから取得
    emergencytransport = await emergencytransport_crud.get_emergency_transport_by_pk(db, year, Dispatch_Transport, Type)
    if not emergencytransport:
        # 救急搬送状況が見つからない場合、HTTP 404エラーを返す
        raise HTTPException(status_code=404, detail="救急搬送状況が見つかりません")
    return emergencytransport

# 特定の救急搬送状況を更新するエンドポイント
@router.put("/{keys}", response_model=ResponseSchema)
async def modify_emergency_transport(keys: str,
                                     emergencytransport: emergency_transport_Schema,
                                     db: AsyncSession = Depends(db.get_dbsession)):
    # PKを分解して取得
    year = int(keys.split("-")[0])
    Dispatch_Transport = keys.split("-")[1]
    Type = keys.split("-")[2]        
    # 指定されたPKの救急搬送状況を新しいデータで更新
    updated_emergencytransport = await emergencytransport_crud.update_emergency_transport(db, year, Dispatch_Transport, Type, emergencytransport)
    if not updated_emergencytransport:
        # 更新対象が見つからない場合、HTTP 404エラーを返す
        raise HTTPException(status_code=404, detail="更新対象が見つかりません")
    return ResponseSchema(message="救急搬送状況が正常に更新されました")

# 特定の救急搬送状況を削除するエンドポイント
@router.delete("{keys}", response_model=ResponseSchema)
async def remove_emergency_transport(keys: str,
                                     db: AsyncSession = Depends(db.get_dbsession)):
    # PKを分解して取得
    year = int(keys.split("-")[0])
    Dispatch_Transport = keys.split("-")[1]
    Type = keys.split("-")[2]
    # 指定されたPKの救急搬送状況をデータベースから削除
    result = await emergencytransport_crud.delete_emergency_transport(db, year, Dispatch_Transport, Type)
    if not result:
        # 削除対象が見つからない場合、HTTP 404エラーを返す
        raise HTTPException(status_code=404, detail="削除対象が見つかりません")
    return ResponseSchema(message="救急搬送状況が正常に削除されました")