from typing import Type, TypeVar, Generic, List, Optional
from sqlmodel import Session, select, SQLModel
from fastapi import HTTPException
import uuid

T= TypeVar("T", bound=SQLModel)

class GenericDal(Generic[T]):
    def __init__(self,model:Type[T], db: Session):
        self.model = model
        self.db_session = db

    def create(self, obj: T)-> T:
        self.db_session.add(obj)
        self.db_session.commit()
        self.db_session.refresh(obj)
        return obj

    def get(self, id: uuid.UUID )-> Optional[T]:
        return self.db_session.get(self.model,id)

    def get_all(self) -> Optional[List[T]]:
        statement = select(self.model)
        return self.db_session.exec(statement).all()

    def update(self, id: uuid.UUID, obj_data: dict)-> Optional[T]:
        db_obj = self.get (id)
        if not db_obj:
            raise HTTPException (status_code=404,detail="Object not found")    
        for key, value in obj_data.items():
            if value is not None:
                setattr(db_obj, key, value)
        self.db_session.add(db_obj)
        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return db_obj
    
    def delete(self, id: uuid.UUID)->bool:
        obj = self.get(id)
        if not obj:
            raise HTTPException (status_code=404, detail="Object not found")
        self.db_session.delete(obj)
        self.db_session.commit()
        return True




