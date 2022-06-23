import sqlalchemy.orm as _orm
import DB.models as _models


def get_all_data(db: _orm.Session) -> list[_models.ConnectionList]:
    data = db.query(_models.ConnectionList).all()
    for connect in data:
        for area in connect.area:
            area.valuelist
        for matharea in connect.matharea:
            for area in matharea.area:
                area.valuelist
    return data


def get_all_con(db: _orm.Session) -> list:
    return db.query(_models.ConnectionList).order_by(_models.ConnectionList.id.asc()).all()

def get_con(id: int, db: _orm.Session):
    connect = db.query(_models.ConnectionList).filter(_models.ConnectionList.id==id)[0]
    return connect

def get_all_area(id_connection: int, db: _orm.Session) -> list:
    return db.query(_models.ConnectionList).filter(_models.ConnectionList.id==id_connection)[0].area

def get_area(id_area: int, db: _orm.Session):
    return db.query(_models.Area).filter(_models.Area.id==id_area)[0]

def get_all_value(id_area: int, db: _orm.Session) -> list[_models.ValueList]:
    return db.query(_models.Area).filter(_models.Area.id==id_area)[0].valuelist

def get_value(id_value: int, db: _orm.Session) -> _models.ValueList:
    return db.query(_models.ValueList).filter(_models.ValueList.id==id_value)[0]