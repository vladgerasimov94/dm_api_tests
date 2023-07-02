from enum import Enum

from pydantic import BaseModel, StrictStr, Field
from typing import Optional


class PagingSettings(BaseModel):
    posts_per_page: int = Field(alias="postsPerPage")
    comments_per_page: int = Field(alias="commentsPerPage")
    topics_per_page: int = Field(alias="topicsPerPage")
    messages_per_page: int = Field(alias="messagesPerPage")
    entities_per_page: int = Field(alias="entitiesPerPage")


class ColorSchema(Enum):
    MODERN = "Modern"
    PALE = "Pale"
    CLASSIC = "Classic"
    CLASSIC_PALE = "ClassicPale"
    NIGHT = "Night"


class UserSettings(BaseModel):
    color_schema: ColorSchema = Field(alias="colorSchema")
    nannyGreetingsMessage: Optional[StrictStr]
    paging: Optional[PagingSettings] = Field(default=None)


class ParseMode(Enum):
    COMMON = "Common"
    INFO = "Info"
    POST = "Post"
    CHAT = "Chat"


class InfoBbText(BaseModel):
    value: StrictStr
    parse_mode: ParseMode = Field(alias="parseMode")


class UserRole(Enum):
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


class UserDetails(BaseModel):
    login: StrictStr
    roles: list[UserRole]
    medium_picture_url: Optional[StrictStr] = Field(alias="mediumPictureUrl", default=None)
    small_picture_url: Optional[StrictStr] = Field(alias="smallPictureUrl", default=None)
    status: Optional[StrictStr] = Field(default=None)
    rating: Rating
    online: Optional[str] = Field(default=None)
    name: Optional[StrictStr] = Field(default=None)
    location: Optional[StrictStr] = Field(default=None)
    registration: Optional[str] = Field(default=None)
    icq: Optional[StrictStr] = Field(default=None)
    skype: Optional[StrictStr] = Field(default=None)
    originalPictureUrl: StrictStr
    info: InfoBbText
    settings: UserSettings


class UserDetailsEnvelopeModel(BaseModel):
    resource: UserDetails
    metadata: Optional[StrictStr] = Field(default=None)
