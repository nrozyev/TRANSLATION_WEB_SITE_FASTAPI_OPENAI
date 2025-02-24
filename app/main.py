import logging
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud

from schemas import TranslationRequestSchema, TaskResponseSchema, TranslationStatusSchema
from typing import List
from utility import perform_translation

# db related #  #
from database import engine, SessionLocal, get_db
import models 
from models import TranslationTask, TranslationResult, IndividualTranslations
models.Base.metadata.create_all(engine)
#       #       #


#####################################################################################################
#####################################################################################################
app = FastAPI()

# Configure logging
logging.basicConfig(filename="program.log", level=logging.INFO)
logging.log(logging.INFO, "beginning program")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return RedirectResponse(url="/index")

@app.get("/index", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

############################################################################
############################################################################
############################################################################
############################################################################





# @app.post("/translate")
# async def translate(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
#     try:
#         body = await request.json()
#         logging.info(f"Received raw request body: {body}")
#     except Exception as e:
#         logging.error(f"Error parsing request body: {e}")
#         raise HTTPException(status_code=400, detail="Invalid request body")
    
#     try:
#         translation_request = TranslationRequestSchema(**body)
#         logging.info(f"Validated request data: {translation_request.json()}")
#     except Exception as e:
#         logging.error(f"Error validating request data: {e}")
#         raise HTTPException(status_code=422, detail="Unprocessable Entity")
    
#     # Convert the languages string to a list
#     languages_list = [lang.strip() for lang in translation_request.languages.split(',')]
    
#     request_data = TranslationRequest(
#         text=translation_request.text,
#         languages=languages_list
#     )
#     db.add(request_data)
#     db.commit()
#     db.refresh(request_data)
#     background_tasks.add_task(process_translations, request_data.id, translation_request.text, languages_list)
#     return {"id": request_data.id, "status": request_data.status}


@app.post("/translate", response_model = TaskResponseSchema)
def translate(request: TranslationRequestSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    logging.log(logging.INFO, "I am in translate route")
    task = crud.create_translation_task(db, request.text, request.languages)
    background_tasks.add_task(perform_translation, task.id, request.text, request.languages, db)

    return {"task_id": task.id}


@app.get("/translate/{task_id}", response_model = TranslationStatusSchema)
def get_translate(task_id: int,  db: Session = Depends(get_db)):
    

    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"task_id": task.id, "status": task.status, "translation": task.translations}

@app.get("/translate/content/{task_id}", response_model = TranslationStatusSchema)
def get_translate_content(task_id: int,  db: Session = Depends(get_db)):
    

    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {task}
