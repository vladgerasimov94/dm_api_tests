from datetime import datetime
from enum import Enum
from typing import Any, List, Optional
from pydantic import BaseModel, Extra, Field, StrictStr


class UserRole(Enum):
    guest = 'Guest'
    player = 'Player'
    administrator = 'Administrator'
    nanny_moderator = 'NannyModerator'
    regular_moderator = 'RegularModerator'
    senior_moderator = 'SeniorModerator'


class Rating(BaseModel):
    class Config:
        extra = Extra.forbid

    enabled: Optional[bool] = Field(None, description='Rating participation flag')
    quality: Optional[int] = Field(None, description='Quality rating')
    quantity: Optional[int] = Field(None, description='Quantity rating')


class User(BaseModel):
    class Config:
        extra = Extra.forbid

    login: Optional[StrictStr] = Field(None, description='Login')
    roles: Optional[List[UserRole]] = Field(None, description='Roles')
    medium_picture_url: Optional[StrictStr] = Field(
        None, alias='mediumPictureUrl', description='Profile picture URL M-size'
    )
    small_picture_url: Optional[StrictStr] = Field(
        None, alias='smallPictureUrl', description='Profile picture URL S-size'
    )
    status: Optional[StrictStr] = Field(None, description='User defined status')
    rating: Optional[Rating] = None
    online: Optional[datetime] = Field(None, description='Last seen online moment')
    name: Optional[StrictStr] = Field(None, description='User real name')
    location: Optional[StrictStr] = Field(None, description='User real location')
    registration: Optional[datetime] = Field(
        None, description='User registration moment'
    )


class Forum(BaseModel):
    class Config:
        extra = Extra.forbid

    id: Optional[StrictStr] = Field(None, description='Forum identifier')
    unread_topics_count: Optional[int] = Field(
        None,
        alias='unreadTopicsCount',
        description='Total count of topics with unread commentaries within',
    )


class BbParseMode(Enum):
    common = 'Common'
    info = 'Info'
    post = 'Post'
    chat = 'Chat'


class CommonBbText(BaseModel):
    class Config:
        extra = Extra.forbid

    value: Optional[StrictStr] = Field(None, description='Text')
    parse_mode: Optional[BbParseMode] = Field(None, alias='parseMode')


class LastTopicComment(BaseModel):
    class Config:
        extra = Extra.forbid

    created: Optional[datetime] = Field(None, description='Creation moment')
    author: Optional[User] = None


class Topic(BaseModel):
    class Config:
        extra = Extra.forbid

    id: Optional[str] = Field(None, description='Topic identifier')
    author: Optional[User] = None
    created: Optional[datetime] = Field(None, description='Creation moment')
    title: Optional[StrictStr] = Field(None, description='Title')
    description: Optional[StrictStr] = None
    attached: Optional[bool] = Field(None, description='Attached')
    closed: Optional[bool] = Field(None, description='Closed')
    last_comment: Optional[LastTopicComment] = Field(None, alias='lastComment')
    comments_count: Optional[int] = Field(
        None, alias='commentsCount', description='Total commentaries count'
    )
    unread_comments_count: Optional[int] = Field(
        None, alias='unreadCommentsCount', description='Number of unread commentaries'
    )
    forum: Optional[Forum] = None
    likes: Optional[List[User]] = Field(None, description='Users who like this')


class TopicEnvelope(BaseModel):
    class Config:
        extra = Extra.forbid

    resource: Optional[Topic] = None
    metadata: Optional[Any] = Field(None, description='Additional metadata')
