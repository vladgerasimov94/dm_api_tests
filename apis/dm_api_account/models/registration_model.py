from typing import Optional

from pydantic import BaseModel, Extra, Field, StrictStr


class Registration(BaseModel):
    class Config:
        extra = Extra.forbid

    login: Optional[StrictStr] = Field(None, description='Login')
    email: Optional[StrictStr] = Field(None, description='Email')
    password: Optional[StrictStr] = Field(None, description='Password')
