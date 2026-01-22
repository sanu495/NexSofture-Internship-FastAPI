from sqlmodel import SQLModel, Session
from Dal.StudentDal import StudentDal
from fastapi import Depends
from DatabaseConfig import get_db

def get_student_dal(db: Session = Depends(get_db)):
    return StudentDal(db)


    