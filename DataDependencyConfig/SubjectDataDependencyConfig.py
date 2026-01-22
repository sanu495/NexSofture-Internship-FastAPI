from sqlmodel import SQLModel, Session
from Dal.SubjectDal import SubjectDal
from fastapi import Depends
from DatabaseConfig import get_db

def get_subject_dal(db: Session = Depends(get_db)):
    return SubjectDal(db)