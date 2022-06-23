from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from services import MainServices as _services
from connection import shemas as _sh
from connection import services_create as _sCreate
from connection import services_show as _sShow
from connection import services_change as _sChange
from connection import services_delete as _sDelete

app = APIRouter(prefix="/connections")

#######################################################
#####   All_data
#######################################################

@app.get("/all", response_model=list[_sh.AllData], tags=["Get Data"])
def show_all_data(db: Session = Depends(_services.get_db)):
    return _sShow.get_all_con(db=db)

#######################################################
#####   Connections
#######################################################

@app.get("/", response_model=list[_sh.Connection], tags=["Get Data"])
def show_all_connections(db: Session = Depends(_services.get_db)):
    return _sShow.get_all_con(db=db)

@app.get("/{id}", response_model=_sh.Connection, tags=["Get Data"])
def show_connection(id: int, db: Session = Depends(_services.get_db)):
    return _sShow.get_con(id=id, db=db)

@app.post("/", response_model=_sh.Connection, tags=["Add Data"])
def add_connection(conn: _sh.ConnectionCreate, db: Session = Depends(_services.get_db)):
    print(conn)
    return _sCreate.create_connection(db=db, conn=conn)

@app.put("/{id}", response_model=_sh.Connection, tags=["Change Data"])
def change_connection(id: int, conn: _sh.ConnectionCreate, db: Session = Depends(_services.get_db)):
    return _sChange.change_connection(db=db, id=id, conn=conn)

@app.delete("/{id}", response_model=_sh.StatusCommand, tags=["Delete Data"])
def delete_connection(id: int, db: Session =Depends(_services.get_db)):
    return _sDelete.delete_connection(id=id, db=db)

#######################################################
#####   Area
#######################################################

@app.get('/{id_connection}/area', response_model=list[_sh.Area], tags=["Get Data"])
def show_all_area_connection(id_connection: int, db: Session = Depends(_services.get_db)):
    return _sShow.get_all_area(id_connection=id_connection, db=db)

@app.get('/area/{id_area}', response_model=_sh.Area, tags=["Get Data"])
def show_area(id_area: int, db: Session = Depends(_services.get_db)):
    return _sShow.get_area(id_area=id_area, db=db)

@app.post('/area', response_model=_sh.Area, tags=["Add Data"])
def add_area(area: _sh.AreaCreate, db: Session = Depends(_services.get_db)):
    return _sCreate.create_area(area=area, db=db)

@app.put('/area/{id_area}', response_model=_sh.Area, tags=["Change Data"])
def change_area(id_area: int, area: _sh.AreaChange, db: Session = Depends(_services.get_db)):
    return _sChange.change_area(id_area=id_area, area=area, db=db)

@app.delete('/area/{id_area}', response_model=_sh.StatusCommand, tags=["Delete Data"])
def delete_area(id_area: int, db: Session = Depends(_services.get_db)):
    return _sDelete.delete_area(id_area=id_area, db=db)

#######################################################
#####   Value
#######################################################

@app.get('/area/{id_area}/value', response_model=list[_sh.Value], tags=["Get Data"])
def show_all_value_area(id_area: int, db: Session = Depends(_services.get_db)):
    return _sShow.get_all_value(id_area=id_area, db=db)

@app.get('/value/{id_value}', response_model=_sh.Value, tags=["Get Data"])
def show_value(id_value: int, db: Session = Depends(_services.get_db)):
    return _sShow.get_value(id_value=id_value, db=db)

@app.post('/value', response_model=_sh.Value, tags=["Add Data"])
def add_value(value:_sh.ValueCreate, db: Session = Depends(_services.get_db)):
    return _sCreate.create_value(value=value, db=db)

@app.put('/value/{id_value}', response_model=_sh.Value, tags=["Change Data"])
def change_value(id_value: int, value: _sh.ValueChange, db: Session = Depends(_services.get_db)):
    return _sChange.change_value(id_value=id_value, value=value, db=db)

@app.delete('/value/{id_value}', response_model=_sh.StatusCommand, tags=["Delete Data"])
def delete_value(id_value: int, db: Session = Depends(_services.get_db)):
    return _sDelete.delete_value(id_value=id_value, db=db)