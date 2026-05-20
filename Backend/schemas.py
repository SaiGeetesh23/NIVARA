# from pydantic import BaseModel

# # --- User Schemas ---
# class UserCreate(BaseModel):
#     email: str
#     password: str

# class User(BaseModel):
#     id: int
#     email: str
#     thread_id: str

#     class Config:
#         orm_mode = True

# # --- Token Schema ---
# class Token(BaseModel):
#     access_token: str
#     token_type: str

# # --- Chat Schema ---
# class ChatRequest(BaseModel):
#     message: str


from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    thread_id: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class ChatRequest(BaseModel):
    message: str