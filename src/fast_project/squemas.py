from pydantic import BaseModel, ConfigDict, EmailStr, Field

from fast_project.models import TodoState


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


class FilterPage(BaseModel):
    limit: int = Field(ge=1, le=100, default=10)
    offset: int = Field(ge=0, default=0)


class FilterTodo(FilterPage):
    title: str | None = Field(default=None, min_length=3)
    description: str | None = None
    state: TodoState | None = None


class Jwt_Token(BaseModel):
    access_token: str
    token_type: str


class TodoSquema(BaseModel):
    title: str
    description: str
    state: TodoState | None = None


class TodoPublic(TodoSquema):
    id: int


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
