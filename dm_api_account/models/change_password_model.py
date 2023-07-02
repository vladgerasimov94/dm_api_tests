from pydantic import BaseModel, StrictStr, Field


class ChangePasswordModel(BaseModel):
    login: StrictStr
    token: str
    old_password: StrictStr = Field(serialization_alias="oldPassword")
    new_password: StrictStr = Field(serialization_alias="newPassword")
