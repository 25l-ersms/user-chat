from pydantic import BaseModel
from datetime import datetime


class UserModel(BaseModel):
    user_id: str
    name: str
    email: str


class MessageModel(BaseModel):
    message_id: str
    sender_id: str
    receiver_id: str
    content: str
    timestamp: datetime
