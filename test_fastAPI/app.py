
import time as _tm
import multiprocessing as _mp

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from sqlalchemy.orm import Session
import uvicorn

from services import CoreService as _start_services
from services import MainServices as _services 
from DB import models as _models
from connection import shemas as _sh
from connection import app_connection




app = FastAPI()

app.include_router(app_connection.app)


origins = ["*"
    # "http://127.0.0.1:8080",
    # "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

process_connect = {}



@app.on_event("startup")
def startup_event():
    status = _start_services.start_proc_switcher_on(process_connect=process_connect)
    if not status:
        print('bed start')
    else:
        print('good start')






@app.get('/status/proc', tags=["Connect"])
def status_process():
    response = {}
    for key in process_connect:
        response[key] = process_connect[key]["process"].is_alive()
    return response

@app.get('/status/conn', tags=["Connect"])
def status_connect():
    response = {}
    for key in process_connect:
        response[key] = process_connect[key]["status"].value
    return response

@app.post('/start', response_model=_sh.StatusCommand, tags=["Connect"])
def start_process(data:_sh.Command, db: Session = Depends(_services.get_db)):
    status = _start_services.start_process(db=db, id_proc=data.id, process_connect=process_connect)
    if status:
        connect = db.query(_models.ConnectionList).filter(_models.ConnectionList.id==data.id)[0]
        connect.switchr = True
        db.commit()
    response = {
        "status": status,
        "text": f"start {data.name}"
    }
    return response

@app.post('/stop', response_model=_sh.StatusCommand, tags=["Connect"])
def stop_process(data: _sh.Command, db: Session = Depends(_services.get_db)):
    print(2)
    # connect = db.query(_models.ConnectionList).filter(_models.ConnectionList.id==data.id)[0]
    status = _start_services.stop_process(all_work_process=process_connect, db=db, id=data.id)
    if status:
        connect = db.query(_models.ConnectionList).filter(_models.ConnectionList.id==data.id)[0]
        connect.switchr = False
        db.commit()
    response = {
        "status": status,
        "text": f"start {data.name}"
    }
    return response

    





# if __name__ == "__main__":
    # _mp.set_start_method("fork")
    # uvicorn.run(app=app, host='0.0.0.0', port=8000)