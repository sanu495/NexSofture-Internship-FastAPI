from fastapi import APIRouter, Depends, HTTPException
from Models.SubjectsModels import SubjectRequest, SubjectResponse, SubjectClass
from DataDependencyConfig.SubjectDataDependencyConfig import get_subject_dal
from Dal.SubjectDal import SubjectDal
from CommonModel import ResponseTo
from starlette import status
from schema import Subject
import uuid
from typing import List, Optional
from sqlmodel import Session

subrouter = APIRouter()

@subrouter.post("/Subject/", tags=["Subject"], response_model = ResponseTo[SubjectResponse],
status_code=status.HTTP_201_CREATED)
def create_subject(subject_data: SubjectRequest, dal: SubjectDal = Depends(get_subject_dal))-> ResponseTo[SubjectResponse]:
    data = Subject(**subject_data.model_dump())
    result = dal.create(data)
    return ResponseTo(
      message="success",
      status=status.HTTP_201_CREATED,
      response=SubjectResponse(**result.model_dump())
    )

@subrouter.get("/subject_result/{subject_id}", tags=["Subject"], response_model= ResponseTo[Optional[SubjectResponse]],
status_code=status.HTTP_200_OK)
def subject_individual(subject_id: uuid.UUID, dal: SubjectDal = Depends(get_subject_dal))-> ResponseTo[Optional[SubjectResponse]]:
    result= dal.get(subject_id)
    if not result:
        return ResponseTo(
            message="Not Found",
            status=status.HTTP_404_NOT_FOUND,
            response=None
        )
    return ResponseTo(
        message="Success",
        status=status.HTTP_201_CREATED,
        response=SubjectResponse(**result.model_dump())
    )

@subrouter.get("/Subject_details", tags=["Subject"], response_model=ResponseTo[Optional[List[SubjectResponse]]],
status_code=status.HTTP_200_OK)
def subject_all(dal: SubjectDal = Depends(get_subject_dal))-> ResponseTo[Optional[List[SubjectResponse]]]:
    result= dal.get_all()
    subject_list= [SubjectResponse(**sub.model_dump()) for sub in result]
    return ResponseTo(
        message="Success",
        status=status.HTTP_200_OK,
        response=subject_list
    )

@subrouter.put("/Subject_update/{subject_id}", tags=["Subject"], response_model=ResponseTo[SubjectResponse],
status_code=status.HTTP_200_OK)
def subject_edit(subject_id: uuid.UUID, subject_data: SubjectRequest, dal: SubjectDal = Depends(get_subject_dal))-> ResponseTo[SubjectResponse]:
    result= dal.update(subject_id, subject_data.model_dump())
    if not result:
        return ResponseTo(
            message="Not Found",
            status=status.HTTP_404_NOT_FOUND,
            response=None
        )
    return ResponseTo(
        message="Subject Details are Updated Successfully",
        status=status.HTTP_200_OK,
        response=SubjectResponse(**result.model_dump())
    )

@subrouter.delete("/Sub_delete/{subject_id}", tags=["Subject"], response_model= ResponseTo[bool],
status_code=status.HTTP_200_OK)
def subject_delete(subject_id: uuid.UUID, dal: SubjectDal = Depends(get_subject_dal))-> ResponseTo[bool]:
    result= dal.delete(subject_id)
    if not result:
        return ResponseTo(
            message="Not Found",
            status= status.HTTP_404_NOT_FOUND,
            response=False
        )
    return ResponseTo(
        message="Deleted Subject Successfully",
        status=status.HTTP_200_OK,
        response=True
    )

@subrouter.get("/Relation_table", tags=["Subject"], response_model= ResponseTo[list[SubjectClass]],
status_code=status.HTTP_200_OK)
def Subject_and_Class(dal: SubjectDal = Depends(get_subject_dal))-> ResponseTo[list[SubjectClass]]:
    result = dal.Jointable()
    return ResponseTo(
        message="Success",
        status=status.HTTP_200_OK,
        response= result
    )
