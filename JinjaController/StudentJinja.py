from fastapi import APIRouter, Depends, HTTPException, Request, Form
from Models.StudentModels import StudentRequest, StudentResponse, StudentUpdate, StudentContact, StudentClass, StudentForm
from DataDependencyConfig.StudentDataDependencyConfig import get_student_dal
from Dal.StudentDal import StudentDal
from CommonModel import ResponseTo
from starlette import status
from schema import Student, BloodGroup
import uuid
from typing import List, Optional
from datetime import date
from sqlmodel import Session, select
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

apirouter = APIRouter(tags=["Student-Jinja"])

templates = Jinja2Templates(directory="StudentTemplates")

# HOME PAGE 

@apirouter.get("/", name="home", response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse("home.html",{"request":request})

@apirouter.get("/Student", name="student_home", response_class=HTMLResponse)
def get_student_home(request:Request):
    return templates.TemplateResponse("studenthome.html",{"request":request})

@apirouter.get("/About", name="about_us", response_class=HTMLResponse)
def get_about_page(request:Request):
    return templates.TemplateResponse("AboutUs.html",{"request":request})

# STUDENT HOME PAGE (RESPONSE)

@apirouter.get("/Studentform", name="student_form", response_class=HTMLResponse)
def get_student_form(request:Request):
    return templates.TemplateResponse("studentform.html",{"request":request})

@apirouter.get("/Studentupdate", name="student_update", response_class=HTMLResponse)
def get_student_update(request:Request):
    return templates.TemplateResponse("Studentupdate.html",{"request":request})

@apirouter.get("/Studentclass", name="student_class", response_class=HTMLResponse)
def get_student_class(request:Request):
    return templates.TemplateResponse("StudentClass.html",{"request":request})

@apirouter.get("/Studentcontact", name="student_contact", response_class=HTMLResponse)
def get_student_contact(request:Request):
    return templates.TemplateResponse("StudentContact.html",{"request":request})

@apirouter.get("/error", name="student_error", response_class=HTMLResponse)
def error_message(request:Request, error_msg: str = "Student ID Couldn't Found"):
    return templates.TemplateResponse("error.html",{"request":request, "error": error_msg})

@apirouter.get("/Studentdetails", name="student_details", response_model=ResponseTo[list[StudentResponse]])
def get_student_details(request:Request, dal: StudentDal = Depends(get_student_dal)):
    result = dal.get_all()
    student_list =[StudentResponse(**student.model_dump()) for student in result]
    return templates.TemplateResponse("studentsDetails.html",{"request":request,"data":student_list})

# STUDENT PAGE (REQUEST)

@apirouter.post("/submit", response_model=ResponseTo[StudentResponse])
def create_Student_form(request:Request, form_data:StudentForm = Form(), dal: StudentDal = Depends(get_student_dal)):
    data= Student(**form_data.model_dump())
    result= dal.create(data)
    value = StudentResponse(**result.model_dump())
    return templates.TemplateResponse("submitform.html",{"request":request, "submit": value})

@apirouter.post("/updatesubmit", response_class=HTMLResponse)
def update_student(request: Request, Student_id: uuid.UUID = Form(...),       
                   name: Optional[str] = Form(None), 
                   date_of_birth: Optional[date] = Form(None),
                   blood_group: Optional[BloodGroup] = Form(None), dal: StudentDal = Depends(get_student_dal)):
 
    result = dal.get(Student_id)
    if not result:
        return templates.TemplateResponse("error.html", {"request": request, "error": f"Student ID {Student_id} not found for update"})
    
    update_data = {}
    
    if name is not None:
        update_data["name"] = name
    if date_of_birth is not None:
        update_data["date_of_birth"] = date_of_birth
    if blood_group is not None:
        update_data["blood_group"] = blood_group
   
    updated = dal.update(Student_id, update_data)
    value = updated.model_dump()
    return templates.TemplateResponse("submitUpdate.html", {"request": request, "submit": value})

@apirouter.post("/updateclass", response_class = HTMLResponse)
def update_student_class(request:Request, Student_id: uuid.UUID = Form(...), class_Std: Optional[int] = Form(None), 
                         dal: StudentDal = Depends(get_student_dal)):
    result = dal.get(Student_id)
    if not result:
        return templates.TemplateResponse("error.html", {"request":request, "error": f"Student ID {Student_id} not found for Update"})
    
    update_data = {}

    if class_Std is not None:
        update_data["class_Std"] = class_Std
    
    updated = dal.update(Student_id, update_data)
    value = updated.model_dump()
    return templates.TemplateResponse("classUpdate.html", {"request":request, "submit": value})

@apirouter.post("/updatecontact", response_class = HTMLResponse)
def update_student_contact(request:Request, Student_id: uuid.UUID = Form(...), primary_contact_number: Optional[int] = Form(None), 
                         dal: StudentDal = Depends(get_student_dal)):
    result = dal.get(Student_id)
    if not result:
        return templates.TemplateResponse("error.html", {"request":request, "error": f"Student ID {Student_id} not found for Update"})
    
    update_data = {}

    if primary_contact_number is not None:
        update_data["primary_contact_number"] = primary_contact_number
    
    updated = dal.update(Student_id, update_data)
    value = updated.model_dump()
    return templates.TemplateResponse("contactUpdate.html", {"request":request, "submit": value})


          

 



