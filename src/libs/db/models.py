# Python imports
from typing import Optional

# Lib imports
from sqlmodel import SQLModel, Field

# Application imports



class User(SQLModel, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    name: str
    password: str
    email: Optional[str] = None
