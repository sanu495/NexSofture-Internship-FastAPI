from sqlmodel import SQLModel, Session
from Dal.ClassDal import ClassDal
from fastapi import Depends
from DatabaseConfig import get_db

def get_class_dal(db: Session = Depends(get_db)):
    return ClassDal(db)