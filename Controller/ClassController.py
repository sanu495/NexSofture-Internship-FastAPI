from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
import uuid
from Models.ClassModels import ClassRequest, ClassResponse
from DataDependencyConfig.ClassDataDependencyConfig import get_class_dal
from Dal.ClassDal import ClassDal
from CommonModel import ResponseTo
from starlette import status as star
from schema import Class

classrouter = APIRouter()

@classrouter.post("/Class", tags=["Class"], response_model=ResponseTo[ClassResponse], status_code=star.HTTP_201_CREATED)
def create_class(class_data: ClassRequest, dal: ClassDal = Depends(get_class_dal)) -> ResponseTo[ClassResponse]:
    data = Class(**class_data.model_dump())
    result = dal.create(data)
    return ResponseTo(
        message="Success",
        status=star.HTTP_201_CREATED,
        response=ClassResponse(**result.model_dump())
    )

@classrouter.get("/classes/{class_id}", tags=["Class"], response_model=ResponseTo[Optional[ClassResponse]], status_code=star.HTTP_200_OK)
def class_one_data(class_id: uuid.UUID, dal: ClassDal = Depends(get_class_dal)) -> ResponseTo[Optional[ClassResponse]]:
    result = dal.get(class_id)
    if not result:
        return ResponseTo(
            message="Not Found",
            status=star.HTTP_404_NOT_FOUND,
            response=None
        )
    return ResponseTo(
        message="Success",
        status=star.HTTP_200_OK,
        response=ClassResponse(**result.model_dump())
    )

@classrouter.get("/class_details", tags=["Class"], response_model=ResponseTo[Optional[List[ClassResponse]]], status_code=star.HTTP_200_OK)
def class_teacher_all(dal: ClassDal = Depends(get_class_dal)) -> ResponseTo[Optional[List[ClassResponse]]]:
    result = dal.get_all()
    class_list = [ClassResponse(**clss.model_dump()) for clss in result]
    return ResponseTo(
        message="Success",
        status=star.HTTP_200_OK,
        response=class_list
    )

@classrouter.put("/Class_update/{class_id}", tags=["Class"], response_model=ResponseTo[ClassResponse], status_code=star.HTTP_200_OK)
def class_new(class_id: uuid.UUID, class_data: ClassRequest, dal: ClassDal = Depends(get_class_dal)) -> ResponseTo[ClassResponse]:
    result = dal.update(class_id, class_data.model_dump())
    if not result:
        return ResponseTo(
            message="Not Found",
            status=star.HTTP_404_NOT_FOUND,
            response=None
        )
    return ResponseTo(
        message="Class Details are updated Successfully",
        status=star.HTTP_200_OK,
        response=ClassResponse(**result.model_dump())
    )

@classrouter.delete("/delete/{class_id}", tags=["Class"], response_model=ResponseTo[bool], status_code=star.HTTP_200_OK)
def class_delete_details(class_id: uuid.UUID, dal: ClassDal = Depends(get_class_dal)) -> ResponseTo[bool]:
    result = dal.delete(class_id)
    if not result:
        return ResponseTo(
            message="Not Found",
            status=star.HTTP_404_NOT_FOUND,
            response=False
        )
    return ResponseTo(
        message="Deleted class Successfully",
        status=star.HTTP_200_OK,
        response=True
    )
