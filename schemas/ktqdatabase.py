from pydantic import BaseModel, Field

# ==================================================
# スキーマ定義
# ==================================================
class emergency_transport_Schema(BaseModel):
    # 年次。このフィールドは必須です。
    year: int = Field(...,
            description="年次を西暦で入力してください。必須項目です。",
            example=2025)
    # 出動と搬送の区分。このフィールドは必須です。
    Dispatch_Transport: str = Field(...,
            description="出動と搬送の区分を選択してください。必須項目です。",
            example="Dispatch",
            max_length=45)
    # 類型。このフィールドは必須です。
    Type: str = Field(...,
            description="類型を選択してください。必須項目です。",
            example="Traffic_accident",
            max_length=45)
    # 件数。このフィールドは任意で入力可能です。
    Number: int = Field(...,
            description="件数。任意で記入できます。",
            example=0)

# レスポンスで使用する結果用スキーマ
class ResponseSchema(BaseModel):
    # 処理結果のメッセージ。このフィールドは必須です。
    message: str = Field(...,
        description="API操作の結果を説明するメッセージ。",
        example="救急搬送状況の更新に成功しました。")