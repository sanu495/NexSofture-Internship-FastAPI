from fastapi import APIRouter, Depends, HTTPException, Request, Form
from Models.StudentModels import StudentRequest, StudentResponse, StudentUpdate, StudentContact, StudentClass
from DataDependencyConfig.StudentDataDependencyConfig import get_student_dal
from Dal.StudentDal import StudentDal
from CommonModel import ResponseTo
from starlette import status
from schema import Student
import uuid
from typing import List, Optional
from sqlmodel import Session, select
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.post("/Student/", tags=["Student"], response_model = ResponseTo[StudentResponse], 
status_code=status.HTTP_201_CREATED)
def create_student(student_data: StudentRequest, dal: StudentDal = Depends(get_student_dal))-> ResponseTo[StudentResponse]:
    data = Student(**student_data.model_dump())
    result = dal.create(data)
    return ResponseTo(
        message="success",
        status=status.HTTP_201_CREATED,
        response=StudentResponse(**result.model_dump())
    )

@router.get("/Student details", tags=["Student"], response_model=ResponseTo[Optional[List[StudentResponse]]],
 status_code=status.HTTP_201_CREATED)
def student_show_all( request: Request, dal: StudentDal = Depends(get_student_dal)) -> ResponseTo[Optional[List[StudentResponse]]]:
    result = dal.get_all()
    student_list = [StudentResponse(**student.model_dump()) for student in result]
    return ResponseTo(
        message="success",
        status=status.HTTP_201_CREATED,
        response=student_list)

@router.put("/Student_update/{student_id}", tags=["Student"], response_model=ResponseTo[StudentResponse],
 status_code=status.HTTP_200_OK)
def student_update(student_id: uuid.UUID, student_data: StudentUpdate, dal: StudentDal = Depends(get_student_dal)) -> ResponseTo[StudentResponse]:
    result = dal.update(student_id, student_data.model_dump())
    if not result:
        return ResponseTo(
            message="Not Found",
            status=status.HTTP_404_NOT_FOUND,
            response="Please input a valid data"
        )
    return ResponseTo(
        message="Student detail updated Successfully",
        status=status.HTTP_200_OK,
        response=StudentResponse(**result.model_dump())
    )

@router.put("/{student_id}", tags=["Student"], response_model=ResponseTo[StudentResponse], status_code=status.HTTP_200_OK)
def student_contact(student_id: uuid.UUID, student_data: StudentContact, dal: StudentDal = Depends(get_student_dal)) -> ResponseTo[StudentResponse]:
    result = dal.update(student_id, student_data.model_dump())
    if not result:
        return ResponseTo(
            message="Not Found",
            status=status.HTTP_404_NOT_FOUND,
            response="Please input a valid data"
        )
    return ResponseTo(
        message="Student Contact details updated Successfully",
        status=status.HTTP_200_OK,
        response=StudentResponse(**result.model_dump())
    )

@router.put("/increment/{student_id}", tags=["Student"], response_model=ResponseTo[Optional[StudentResponse]], status_code=status.HTTP_200_OK)
def student_increment(student_id: uuid.UUID, dal: StudentDal = Depends(get_student_dal)) -> ResponseTo[Optional[StudentResponse]]:
    data = dal.get(student_id)
    if not data:
        return ResponseTo(
            message="Not Found",
            status=status.HTTP_404_NOT_FOUND,
            response=None)

    data.class_Std = data.class_Std+1
    updated_result = dal.update(student_id, data.model_dump())
    return ResponseTo(
        message="Student class details was incremented Successfully",
        status=status.HTTP_200_OK,
        response=StudentResponse(**updated_result.model_dump())
    )

@router.put("/Decrement/{student_id}", tags=["Student"], response_model=ResponseTo[Optional[StudentResponse]],
status_code=status.HTTP_200_OK)
def student_decrement(student_id:uuid.UUID, dal:StudentDal = Depends(get_student_dal))-> ResponseTo[Optional[StudentResponse]]:
    data= dal.get(student_id)
    if not data:
        return ResponseTo(
            message="Not Found",
            status=status.HTTP_404_NOT_FOUND,
            response=None)
    data.class_Std= data.class_Std-1
    student_data=dal.update(student_id, data.model_dump())
    return ResponseTo(
        message="Student class details was decremented Successfully",
        status=status.HTTP_200_OK,
        response=StudentResponse(**student_data.model_dump())
    )

@router.get("/class_student", tags=["Student"], response_model=ResponseTo[dict], status_code=status.HTTP_200_OK)
def class_count(dal: StudentDal = Depends(get_student_dal))-> ResponseTo[dict]:
    data = dal.count_class()
    result=({f"Class{class_std}": count for class_std, count in data})
    return ResponseTo(
        message="Students Class Count are showing Successfully",
        status=status.HTTP_200_OK,
        response=result
    )
    