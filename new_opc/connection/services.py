from sqlalchemy import orm as _orm

from DB import models as _models

def change_record_connection(form: dict, db: _orm.Session, id:int) -> bool:
    """
    Изменяет поля конкретной записи
    """
    try:
        connect_db = db.query(_models.ConnectionList).get(id)
        connect_db.name = form['name']
        connect_db.driver = form['driver']
        connect_db.ip_addres = form['ip']
        connect_db.port = form['port']
        connect_db.slot = form['slot']
        connect_db.rack = form['rack']
        db.commit()
        return True
    except Exception as e:
        print(e)
        db.close()
        return False


def get_all_connections(db: _orm.Session) -> list[_models.ConnectionList]:
    """
    Метод возвращает все записи соединений
    """
    connections_db = db.query(_models.ConnectionList).order_by(_models.ConnectionList.id)
    return connections_db


def get_connection_to_id(db: _orm.Session, id: int) -> _models.ConnectionList:
    """
    Метод возвращает запись с соответствующем id, либо None
    """
    connection = db.query(_models.ConnectionList).filter(id == id)
    if connection:
        return connection.first()
    else:
        return None

def delete_connection_from_name(db: _orm.Session, name_connection: str) -> _models.ConnectionList:
    """
    Метод возвращает запись с соответствующем именем соединения, либо None

    * `db`(Session object) - объект соединения с базой
    * `name_connection`(str) - имя соединения
    """
    connection = db.query(_models.ConnectionList).filter(_models.ConnectionList.name == name_connection)
    if connection:
        db.delete(connection.first())
        return True
    else:
        return False
    