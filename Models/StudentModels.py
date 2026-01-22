from pydantic import BaseModel
from sqlmodel import SQLModel
from schema import Student, BloodGroup
import uuid
from datetime import date, datetime
from fastapi import Form

class StudentResponse(BaseModel):
    id:uuid.UUID
    name:str
    email:str
    date_of_birth: date
    blood_group: BloodGroup
    class_Std:int
    primary_contact_number:str
    created_at: datetime
    updated_at: datetime 

class StudentRequest(BaseModel):
    name:str
    email:str
    date_of_birth:date
    blood_group: BloodGroup
    class_Std:int
    primary_contact_number:str

class StudentUpdate(BaseModel):
    name:str
    date_of_birth:date
    blood_group: BloodGroup

class StudentContact(BaseModel):
    primary_contact_number:str


class StudentClass(BaseModel):
    class_Std:int

class StudentForm (BaseModel):
    name:str 
    email:str 
    date_of_birth:date 
    blood_group: BloodGroup 
    class_Std:int
    primary_contact_number:str

    



