from pydantic import BaseModel

class PasswordCreate(BaseModel):
    website: str
    username: str
    encrypted_password: str

class PasswordOut(PasswordCreate):
    id: int

    class Config:
        orm_mode = True
