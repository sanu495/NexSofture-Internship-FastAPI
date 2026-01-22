from fastapi import APIRouter, Depends, Request, Form
from Models.ClassModels import ClassRequest, ClassResponse
from DataDependencyConfig.ClassDataDependencyConfig import get_class_dal
from Dal.ClassDal import ClassDal
from CommonModel import ResponseTo
from schema import Class
import uuid
from typing import List, Optional
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

classter = APIRouter(tags=["Class-Jinja"])

templates = Jinja2Templates(directory="ClassTemplates")

# Class HomePage (Response)

@classter.get("/Class", name = "class_home", response_class=HTMLResponse)
def get_class_home(request:Request):
    return templates.TemplateResponse("ClassHome.html",{"request":request})

@classter.get("/Classcreate", name="class_form", response_class=HTMLResponse)
def get_class_form(request:Request):
    return templates.TemplateResponse("ClassForm.html",{"request":request})

@classter.get("/Classdelete", name="class_delete", response_class=HTMLResponse)
def get_class_delete(request:Request):
    return templates.TemplateResponse("/ClassDelete.html",{"request":request})

@classter.get("/deleted", name="deleted_class", response_class=HTMLResponse)   
def get_delete_submit(request:Request, delete_msg:  str = "Class ID Deleted Successfully"):
    return templates.TemplateResponse("deletesubmit.html",{"request":request, "delete":delete_msg})

@classter.get("/Classgetid", name="class_find", response_class=HTMLResponse)
def get_class_id(request:Request):
    return templates.TemplateResponse("Classgetid.html",{"request":request})

@classter.get("/ClassUpdate", name="class_update", response_class=HTMLResponse)
def get_class_update(request:Request):
    return templates.TemplateResponse("ClassUpdate.html",{"request":request})

@classter.get("/Classerror", name="class_error", response_class=HTMLResponse)
def get_class_error(request:Request, error_msg: str = "Class ID not Find"):
    return templates.TemplateResponse("ClassError.html",{"request":request, "error":error_msg})

@classter.get("/ClassDetails", name="class_details", response_model=ResponseTo[list[ClassResponse]])
def get_class_details(request:Request, dal:ClassDal = Depends(get_class_dal)):
    result = dal.get_all()
    class_list = [ClassResponse(**cls.model_dump()) for cls in result]
    return templates.TemplateResponse("Classdetails.html",{"request":request, "data":class_list})

# Class (Request)

@classter.post("/createclass", response_model=ResponseTo[ClassResponse])
def create_class(request:Request, class_data: ClassRequest = Form(), dal: ClassDal = Depends(get_class_dal)) -> ResponseTo[ClassResponse]:
    data = Class(**class_data.model_dump())
    result = dal.create(data)
    value = ClassResponse(**result.model_dump())
    return templates.TemplateResponse("Classformsubmit.html",{"request":request, "submit":value})

@classter.post("/classfind", response_model=ResponseTo[Optional[ClassResponse]])
def class_one_data(request:Request, class_id: uuid.UUID = Form(...), dal: ClassDal = Depends(get_class_dal)) -> ResponseTo[Optional[ClassResponse]]:
    result = dal.get(class_id)

    if not result:
        return templates.TemplateResponse("ClassError.html", {"request": request, "error": f"Class ID {class_id} not found"})

    value = ClassResponse(**result.model_dump())
    return templates.TemplateResponse("Classgetidsubmit.html", {"request":request, "submit":value})

@classter.post("/classupdate", response_model=ResponseTo[ClassResponse])
def class_new(request:Request, class_id: uuid.UUID = Form(...), 
              class_name: Optional [int] = Form(None),
              class_teacher: Optional [str] = Form(None), 
              dal: ClassDal = Depends(get_class_dal)) -> ResponseTo[ClassResponse]:
    result = dal.get(class_id)

    if not result:
         return templates.TemplateResponse("ClassError.html", {"request": request, "error": f"Class ID {class_id} not found"})
    
    updated_data = {}

    if class_name is not None:
        updated_data["class_name"] = class_name
    if class_teacher is not None:
        updated_data["class_teacher"] = class_teacher

    value = dal.update(class_id, updated_data)
    updated_list = value.model_dump()
    return templates.TemplateResponse("ClassUpdatesubmit.html", {"request":request, "submit":updated_list})

@classter.post("/classdelete", response_class=HTMLResponse)
def class_delete(request:Request, class_id: uuid.UUID = Form(...), dal: ClassDal = Depends(get_class_dal)):
    result = dal.get(class_id)

    if not result:
        return templates.TemplateResponse("ClassError.html", {"request": request, "error": f"Class ID {class_id} not found"})
    
    value = dal.delete(class_id)
    return templates.TemplateResponse("deletesubmit.html", {"request": request, "delete": f"Class ID {class_id} Deleted Successfully"})
