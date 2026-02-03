from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSquema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserDB(UserPublic):
    password: str


class UserList(BaseModel):
    user: list[UserPublic]
