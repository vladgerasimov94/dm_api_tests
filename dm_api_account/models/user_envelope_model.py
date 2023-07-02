from enum import Enum

from pydantic import BaseModel, StrictStr, Field
from typing import Optional


class Metadata(BaseModel):
    email: Optional[StrictStr] = Field(default=None)


class Roles(Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class User(BaseModel):
    login: StrictStr
    roles: Optional[list[Roles]] = Field(default=None)
    medium_picture_url: Optional[StrictStr] = Field(alias="mediumPictureUrl", default=None)
    small_picture_url: Optional[StrictStr] = Field(alias="smallPictureUrl", default=None)
    status: Optional[StrictStr] = Field(default=None)
    rating: Optional[Rating] = Field(default=None)
    online: Optional[str] = Field(default=None)
    name: Optional[StrictStr] = Field(default=None)
    location: Optional[StrictStr] = Field(default=None)
    registration: Optional[str] = Field(default=None)


class UserEnvelopeModel(BaseModel):
    resource: User
    metadata: Optional[Metadata] = Field(default=None)
