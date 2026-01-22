from pydantic import BaseModel
from schema import Subject, Class
import uuid
from datetime import datetime
from sqlmodel import SQLModel
from Models.ClassModels import ClassResponse
from typing import Optional

class SubjectResponse(BaseModel):
    id:uuid.UUID
    subject_name:str
    created_at:datetime
    class_id: Optional[uuid.UUID] = None

class SubjectRequest(BaseModel):
    subject_name:str
    class_id: Optional[uuid.UUID] = None
 
class SubjectClass(BaseModel):
    id: uuid.UUID                
    subject_name: str
    class_id: Optional[uuid.UUID] = None
    class_name: int
    class_teacher: Optional[str] = None





    