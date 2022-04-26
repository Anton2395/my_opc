from crypt import methods
import time as _tm

from flask import Blueprint, render_template, request, redirect, url_for, abort

from DB import models as _models




app_value = Blueprint('valuelist', __name__)


@app_value.route("/<id_connection>", methods=["GET"])
def list_value_page(id_connection:int) -> str:
    db = _models.Session()
    data = None
    area = db.query(_models.ConnectionList).filter(_models.ConnectionList.id==id_connection)
    for i in area:
        data = {
            "id": i.id,
            "name": i.name
        }
    return render_template('valuelist/index.html', data=data)

@app_value.route("/list_volue/<id_connection>", methods=["GET"])
def list_value_data(id_connection: int) -> str:
    data = {}
    _tm.sleep(2)
    return data


@app_value.route("/add_area", methods=["POST"])
def add_new_area() -> str:
    try:
        db = _models.Session()
        data_post = request.json
        new_area = _models.Area(
            name=data_post['name'],
            connection_id=data_post['connection_id'],
            area_memory=data_post['area_memory'],
            db=data_post['db'],
            start=data_post['start'],
            size=data_post['size']
        )
        db.add(new_area)
        db.commit()
        db.close()
        return 'seccses'
    except:
        return 'error'
    


@app_value.route("/update_area", methods=["PUT"])
def update_area() -> str:
    try:
        db = _models.Session()
        data_post = request.json
        area = db.query(_models.Area).get(data_post['area_id'])
        area.name = data_post['name']
        area.area_memory = data_post['area_memory']
        area.db = data_post['db']
        area.start = data_post['start']
        area.size = data_post['size']
        db.commit()
        db.close()
        return 'seccses'
    except:
        return 'error'
