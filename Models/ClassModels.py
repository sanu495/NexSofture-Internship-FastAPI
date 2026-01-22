from pydantic import BaseModel
from schema import Class
import uuid
from sqlmodel import SQLModel
from datetime import datetime


class ClassResponse(BaseModel):
    id:uuid.UUID
    class_name:int
    class_teacher:str
    created_at:datetime

class ClassRequest(BaseModel):
    class_name:int
    class_teacher:str
