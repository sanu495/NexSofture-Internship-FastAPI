from GenericDal import GenericDal
from sqlmodel import Session, select, func
from schema import Student

class StudentDal(GenericDal[Student]):
    def __init__(self, db: Session):
        super().__init__(model=Student, db=db)
   

    def count_class(self) -> dict:
        query = select(Student.class_Std, func.count()).group_by(Student.class_Std)
        return self.db_session.exec(query).all()
