from sqlalchemy import Column, Integer, String
from .database import Base

class Password(Base):
    __tablename__ = "passwords"
    
    id = Column(Integer, primary_key=True, index=True)
    website = Column(String, index=True)
    username = Column(String)
    encrypted_password = Column(String)
