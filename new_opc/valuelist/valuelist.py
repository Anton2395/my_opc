import time as _tm

from flask import Blueprint, render_template, request, redirect, url_for, abort

from DB import models as _md




app_value = Blueprint('valuelist', __name__)


@app_value.route("/<id_connection>", methods=["GET"])
def list_value_page(id_connection:int) -> str:
    db = _md.Session()
    data = None
    area = db.query(_md.ConnectionList).filter(_md.ConnectionList.id==id_connection)
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