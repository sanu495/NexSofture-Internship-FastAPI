from fastapi import APIRouter, Depends, Request, Form
from Models.SubjectsModels import SubjectRequest, SubjectResponse
from DataDependencyConfig.SubjectDataDependencyConfig import get_subject_dal
from Dal.SubjectDal import SubjectDal
from CommonModel import ResponseTo
from schema import Subject
import uuid
from typing import List, Optional
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

suberout = APIRouter(tags=["Subject-Jinja"])

templates = Jinja2Templates(directory="SubjectTemplates")

# Subject HomePage (Response)

@suberout.get("/Subject", name = "subject_home", response_class=HTMLResponse)
def get_subject_home(request:Request):
    return templates.TemplateResponse("SubjectHome.html",{"request":request})

@suberout.get("/Subjectcreate", name="subject_form", response_class=HTMLResponse)
def get_subject_form(request:Request):
    return templates.TemplateResponse("SubjectForm.html",{"request":request})

@suberout.get("/Subjectdeleted", name="delete_submit", response_class=HTMLResponse)
def get_subjectdelete_submit(request:Request, delete_msg:  str = "Subject ID Deleted Successfully"):
    return templates.TemplateResponse("Deletesubmit.html",{"request":request, "delete":delete_msg})

@suberout.get("/Subjectdeleteform", name="subject_delete", response_class=HTMLResponse)
def get_subject_delete(request:Request):
    return templates.TemplateResponse("Deleteform.html",{"request":request})

@suberout.get("/Subjectfind", name="subject_find", response_class=HTMLResponse)
def get_subject_id(request:Request):
    return templates.TemplateResponse("Subjectgetid.html",{"request":request})

@suberout.get("/SubjectUpdate", name="subject_update", response_class=HTMLResponse)
def get_subject_update(request:Request):
    return templates.TemplateResponse("SubjectUpdate.html",{"request":request})

@suberout.get("/Subjecterror", name="subject_error", response_class=HTMLResponse)
def get_subject_error(request:Request, error_msg: str = "Subject ID Couldn't Find"):
    return templates.TemplateResponse("SubjectError.html",{"request":request, "error":error_msg})

@suberout.get("/SubjectDetails", name="subject_details", response_model=ResponseTo[list[SubjectResponse]])
def get_subject_details(request:Request, dal:SubjectDal = Depends(get_subject_dal)):
    result = dal.get_all()
    subject_list = [SubjectResponse(**sub.model_dump()) for sub in result]
    return templates.TemplateResponse("Subjectdetails.html",{"request":request, "data":subject_list})

# Subjects (Request)

@suberout.post("/createform", response_model=ResponseTo[SubjectResponse])
def create_subject(request:Request, subject_data: SubjectRequest = Form(), dal: SubjectDal = Depends(get_subject_dal))-> ResponseTo[SubjectResponse]:
    data = Subject(**subject_data.model_dump())
    result = dal.create(data)
    value = SubjectResponse(**result.model_dump())
    return templates.TemplateResponse("Subjectsubmit.html",{"request":request, "submit":value})

@suberout.post("/subjectfind", response_model=ResponseTo[Optional[SubjectResponse]])
def subject_individual(request:Request, subject_id: uuid.UUID = Form(...), dal: SubjectDal = Depends(get_subject_dal))-> ResponseTo[Optional[SubjectResponse]]:
    result= dal.get(subject_id)

    if not result:
        return templates.TemplateResponse("SubjectError.html", {"request":request, "error": f"Subject ID {subject_id} Couldn't Found"})
    
    value = SubjectResponse(**result.model_dump())
    return templates.TemplateResponse("Subjectgetidsubmit.html", {"request":request, "submit":value})

@suberout.post("/updatesubject", response_class=HTMLResponse)
def subject_new(request:Request, subject_id: uuid.UUID = Form(...),
                   subject_name: Optional[str] = Form(None), dal:SubjectDal = Depends(get_subject_dal)):
    result = dal.get(subject_id)

    if not result:
        return templates.TemplateResponse("SubjectError.html", {"request":request, "error": f"Subject ID {subject_id} not Found"})

    updated_data = {}

    if subject_name is not None:
        updated_data["subject_name"] = subject_name

    updated_subject = dal.update(subject_id, updated_data)
    updated_list = SubjectResponse(**updated_subject.model_dump())
    return templates.TemplateResponse("Updatesubmit.html", {"request":request, "submit":updated_list})

@suberout.post("/subjectdelete", response_class=HTMLResponse)
def delete_sub(request:Request, subject_id: uuid.UUID = Form(...), dal:SubjectDal = Depends(get_subject_dal)):
    result = dal.get(subject_id)

    if not result:
       return templates.TemplateResponse("SubjectError.html", {"request":request, "error": f"Subject ID {subject_id} Couldn't Found"})

    value = dal.delete(subject_id)
    return templates.TemplateResponse("Deletesubmit.html", {"request":request, "delete": f"Subject ID {subject_id} Deleted Successfully"})