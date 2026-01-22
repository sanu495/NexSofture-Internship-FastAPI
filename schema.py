from sqlmodel import SQLModel, Field, Relationship
from fastapi import FastAPI, Query
import uuid
from enum import Enum 
from datetime import datetime, date
from typing import Optional


class UUID(SQLModel):
    id:uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)

class BloodGroup(str, Enum):   #Enum class for Student table
    B_Positive ="B+"
    B_Negative ="B-"
    A_Positive ="A+"
    AB_Positive ="AB+"
    O_Positive ="O+"
    O_Negative ="O-"

class Student(UUID, SQLModel, table=True):   #Student table
    __tablename__="Student"
    name:str
    email:str =Field(unique=True)
    primary_contact_number:str
    blood_group: BloodGroup
    class_Std:int = Field(gt=0, le=12)
    date_of_birth: date
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now,sa_column_kwargs={"onupdate": datetime.now})



class Class(UUID, SQLModel, table=True):      #Class table
    __tablename__="Class"
    class_name:int = Field(gt=0, le=12)
    class_teacher: Optional[str]
    created_at:datetime = Field(default_factory=datetime.now)
    subjects: list["Subject"] = Relationship(back_populates="classes")



class Subject(UUID, SQLModel, table=True):     #Subject table  
    __tablename__="Subject"
    subject_name:str
    class_id: Optional [uuid.UUID] = Field(default_factory= None, foreign_key="Class.id")
    created_at:datetime = Field(default_factory=datetime.now)
    classes: Optional["Class"] = Relationship(back_populates="subjects")



# class User(SQLModel, table=True):       # User Table
#     __table_name__="User"
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     email: str = Field(unique=True)
#     phone_num:str






    
