import sqlalchemy.orm as _orm


import DB.models as _models
from connection import shemas as _sh



def create_connection(db: _orm.Session, conn: _sh.ConnectionCreate):
    db_connection = _models.ConnectionList(
        name=conn.name,
        driver=conn.driver,
        ip_addres=conn.ip_addres,
        port=conn.port,
        slot=conn.slot,
        rack=conn.rack
        )
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection

def create_area(db: _orm.Session, area: _sh.AreaCreate):
    db_area = _models.Area(
        connection_id=area.connection_id,
        name=area.name,
        area_memory=area.area_memory,
        group=area.group,
        db=area.db,
        start=area.start,
        size=area.size
    )
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area

def create_value(db: _orm.Session, value: _sh.ValueCreate):
    db_value = _models.ValueList(
        area_id=value.area_id,
        start=value.start,
        name_val=value.name_val,
        type_value_get_data=value.type_value_get_data,
        type_value_write_data=value.type_value_write_data,
        if_change=value.if_change,
        divide=value.divide,
        divide_number=value.divide_number,
        time_write_if_change=value.time_write_if_change,
        time_rewrite=value.time_rewrite,
        bit=value.bit
    )
    db.add(db_value)
    db.commit()
    db.refresh(db_value)
    return db_value