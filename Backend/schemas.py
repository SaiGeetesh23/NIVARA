from pydantic import BaseModel

# --- User Schemas ---
class UserCreate(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: int
    email: str
    thread_id: str

    class Config:
        # This allows Pydantic to work with ORM models like SQLAlchemy
        orm_mode = True

# --- Token Schema ---
class Token(BaseModel):
    access_token: str
    token_type: str

# --- Chat Schema ---
class ChatRequest(BaseModel):
    message: str
