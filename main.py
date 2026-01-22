from fastapi import FastAPI
from DatabaseConfig import create_tables
from Controller.StudentController import router
from Controller.SubjectController import subrouter
from Controller.ClassController import classrouter
from JinjaController.StudentJinja import apirouter
from JinjaController.ClassJinja import classter
from JinjaController.SubjectJinja import suberout
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables()

app.mount("/static", StaticFiles(directory="ClassTemplates"), name="static") 
app.mount("/static", StaticFiles(directory="StudentTemplates"), name="static")
app.mount("/static", StaticFiles(directory="SubjectTemplates"), name="static") 

app.mount("/ClassPhotos", StaticFiles(directory="ClassTemplates/ClassPhotos"), name="class_photos")
app.mount("/Photos", StaticFiles(directory="StudentTemplates/Photos"), name="student_photos")
app.mount("/SubPhotos", StaticFiles(directory="SubjectTemplates/SubPhotos"), name="subject_photos")

app.include_router(apirouter)
app.include_router(classter)
app.include_router(suberout)
app.include_router(router)
app.include_router(classrouter)
app.include_router(subrouter)



if __name__=="__main__":
    create_tables()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)