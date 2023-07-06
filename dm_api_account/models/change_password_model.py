from typing import Optional

from pydantic import BaseModel, Extra, Field, StrictStr


class ChangePassword(BaseModel):
    class Config:
        extra = Extra.forbid

    login: Optional[StrictStr] = Field(None, description='User login')
    token: Optional[str] = Field(None, description='Password reset token')
    old_password: Optional[StrictStr] = Field(
        None, serialization_alias='oldPassword', description='Old password'
    )
    new_password: Optional[StrictStr] = Field(
        None, serialization_alias='newPassword', description='New password'
    )
