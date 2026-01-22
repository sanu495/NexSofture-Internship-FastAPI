from GenericDal import GenericDal
from sqlmodel import Session, select
from schema import Subject, Class
from Models.SubjectsModels import SubjectClass

class SubjectDal(GenericDal[Subject]):
    def __init__(self, db: Session):
        super().__init__(Subject, db)

    def Jointable(self)->list[SubjectClass]:
        query = select (Subject, Class).join(Class, Class.id == Subject.class_id)
        statement = self.db_session.exec(query).all()
        return [SubjectClass(
            id=subject.id,
            subject_name=subject.subject_name,
            class_id=cls.id,
            class_name=cls.class_name,
            class_teacher=cls.class_teacher,)for subject, cls in statement]
        
