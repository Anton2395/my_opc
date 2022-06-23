from psycopg2 import connect
import sqlalchemy.orm as _orm

import DB.models as _models


def delete_connection(id: int, db: _orm.Session) -> dict:
    connects = db.query(_models.ConnectionList).filter(_models.ConnectionList.id==id)[0]
    for connect in connects:
        name = connect.name
        db.delete(connect)
    db.commit()
    return {
        "status": True,
        "text": f"{name} connection delete"
    }

def delete_area(id_area: int, db: _orm.Session):
    areas = db.query(_models.Area).filter(_models.Area.id==id_area)
    for area in areas:
        name = area.name
        db.delete(area)
    db.commit()
    return {
        "status": True,
        "text": f"{name} area delete"
    }

def delete_value(id_value: int, db: _orm.Session):
    values = db.query(_models.ValueList).filter(_models.ValueList.id==id_value)
    for value in values:
        name = value.name_val
        db.delete(value)
    db.commit()
    return {
        "status": True,
        "text": f"{name} value delete"
    }
