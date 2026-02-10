from pydantic import BaseModel, ConfigDict, EmailStr


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
    model_config = ConfigDict(from_attributes=True)


class UserDB(UserPublic):
    password: str


class UserList(BaseModel):
    user: list[UserPublic]


class Jwt_Token(BaseModel):
    access_token: str
    token_type: str
