import sqlalchemy.orm as _orm

import DB.models as _models
from connection import shemas as _sh


def change_connection(
    id: int,
    db: _orm.Session,
    conn: _sh.ConnectionCreate
):
    connect = db.query(_models.ConnectionList).filter(_models.ConnectionList.id==id)[0]
    connect.name = conn.name
    connect.driver = conn.driver
    connect.ip_addres = conn.ip_addres
    connect.port = conn.port
    connect.slot = conn.slot
    connect.rack = conn.rack
    db.commit()
    db.refresh(connect)
    return connect

def change_area(
    id_area: int,
    area: _sh.AreaChange,
    db: _orm.Session
):
    db_area = db.query(_models.Area).filter(_models.Area.id==id_area)[0]
    db_area.name = area.name
    db_area.area_memory = area.area_memory
    db_area.group = area.group
    db_area.db = area.db
    db_area.start = area.start
    db_area.size = area.size
    db.commit()
    db.refresh(db_area)
    return db_area

def change_value(
    id_value: int,
    value: _sh.ValueChange,
    db: _orm.Session
):
    db_value = db.query(_models.ValueList).filter(_models.ValueList.id==id_value)[0]
    db_value.start = value.start
    db_value.name_val = value.name_val
    db_value.type_value_get_data = value.type_value_get_data
    db_value.type_value_write_data = value.type_value_write_data
    db_value.if_change = value.if_change
    db_value.divide = value.divide
    db_value.divide_number = value.divide_number
    db_value.time_write_if_change = value.time_write_if_change
    db_value.time_rewrite = value.time_rewrite
    db_value.bit = value.bit
    db.commit()
    db.refresh(db_value)
    return db_value