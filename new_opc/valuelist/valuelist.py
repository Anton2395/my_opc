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
    """
    POST URI - http://<server>/value/add_area
    {
        "name":<str>,
        "connection_id":<int>,
        "area_memory":<str>,
        "db":<int>,
        "start":<int>,
        "size":<int>
    }
    """
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
    """
    PUT URI - http://<server>/value/update_area
    {
        "name":<str>,
        "area_id":<int>,
        "area_memory":<str>,
        "db":<int>,
        "start":<int>,
        "size":<int>
    }
    """
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

@app_value.route("/delete_area", methods=["DELETE"])
def delete_area() -> str:
    """
    DELETE URI - http://<server>/value/delete_area
    {
        "area_id":<int>,
    }
    """
    try:
        data_psot = request.json
        db = _models.Session()
        area = db.query(_models.Area).get(data_psot["area_id"])
        db.delete(area)
        db.commit()
        db.close()
        return 'seccses'
    except:
        return 'error'

@app_value.route('/add_value', methods=["POST"])
def add_value() -> str:
    """
    POST URI - http://<server>/value/add_value
    {
        "area_id":<int>,
        "start":<int>,
        "name_val":<str>,
        "type_value_get_data":<str>(select "int" or "flot" or "double" or "bool"),
        "type_value_write_data":<str>(select "int" or "flot" or "double" or "bool"),
        "if_change":<bool>,
        "divide":<bool>,
        "divide_number":<float>,
        "time_write_if_change":<int>(sec?),
        "time_rewrite":<int>(min?),
        "bit":<int>
    }
    """
    data_post = request.json
    db = _models.Session()
    new_value = _models.ValueList(
        area_id=data_post['area_id'],
        start=data_post['start'],
        name_val=data_post['name_val'],
        type_value_get_data=data_post['type_value_get_data'],
        type_value_write_data=data_post['type_value_write_data'],
        if_change=data_post['if_change'],
        divide=data_post['divide'],
        divide_number=data_post['divide_number'],
        time_write_if_change=data_post['time_write_if_change'],
        time_rewrite=data_post['time_rewrite'],
        bit=data_post['bit'],
    )
    db.add(new_value)
    db.commit()
    db.close()
    return 'secces'


@app_value.route('/update_value', methods=["PUT"])
def update_value() -> str:
    """
    PUT URI - http://<server>/value/update_value
    {
        "value_id":<int>,
        "start":<int>,
        "name_val":<str>,
        "type_value_get_data":<str>(select "int" or "flot" or "double" or "bool"),
        "type_value_write_data":<str>(select "int" or "flot" or "double" or "bool"),
        "if_change":<bool>,
        "divide":<bool>,
        "divide_number":<float>,
        "time_write_if_change":<int>(sec?),
        "time_rewrite":<int>(min?),
        "bit":<int>
    }
    """
    try:
        data_post = request.json
        db = _models.Session()
        value = db.query(_models.ValueList).get(data_post['value_id'])
        value.start = data_post['start']
        value.name_val = data_post['name_val']
        value.type_value_get_data = data_post['type_value_get_data']
        value.type_value_write_data = data_post['type_value_write_data']
        value.if_change = data_post['if_change']
        value.divide = data_post['divide']
        value.divide_number = data_post['divide_number']
        value.time_write_if_change = data_post['time_write_if_change']
        value.time_rewrite = data_post['time_rewrite']
        db.commit()
        db.close()
        return 'secces'
    except:
        return 'error'


@app_value.route('/delete_value', methods=['DELETE'])
def delete_value() -> str:
    """
    DELETE URI - http://<server>/value/delete_value
    {
        "value_id":<int>,
    }
    """
    try:
        data_post = request.json
        db = _models.Session()
        value = db.query(_models.ValueList).get(data_post['value_id'])
        db.delete(value)
        db.commit()
        db.close()
        return 'secces'
    except:
        return 'error'