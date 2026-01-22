from GenericDal import GenericDal
from sqlmodel import Session
from schema import Class

class ClassDal(GenericDal[Class]):
    def __init__(self,db: Session):
        super().__init__(Class, db)