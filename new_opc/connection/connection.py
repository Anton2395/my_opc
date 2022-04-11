from sqlite3 import connect
from flask import Blueprint, render_template, request, redirect, url_for, abort



from DB import models as _models
from connection import services as _services


app_connect = Blueprint('connections', __name__)

@app_connect.route("/", methods=["GET", "POST"])
def list_connections():
    if request.method == "GET":
        with _models.get_db() as db:
            connections_db = db.query(_models.ConnectionList).order_by(_models.ConnectionList.id)
        connections = []
        for connection in connections_db:
            connection_dict = {
                "id": connection.id,
                "name": connection.name,
                "port": connection.port,
                "driver": connection.driver,
                "ip": connection.ip_addres,
                "slot": connection.slot,
                "rack": connection.rack,
                "switchr": connection.switchr
            }
            connections.append(connection_dict)
        if connections:
            data = {
                "connections": connections,
                "last_id": connections_db[-1].id
            }
        else:
            data = {
                "connections": connections,
                "last_id": 0
            }
        return render_template('connection/connection_list.html', data=data)


@app_connect.route("/<id_connection>", methods=["GET", "POST"])
def refactor_record(id_connection: int):
    if request.method == "GET":
        with _models.get_db() as db:
            connect_db = _services.get_connection_id(db=db, id=id_connection)
        return render_template('connection/refactor.html', connect=connect_db)
    elif request.method == "POST":
        with _models.get_db() as db:
            if _services.change_record_connection(db=db, form=request.form, id=id_connection):
                return redirect(url_for('connections.list_connections'))
            else:
                abort(400)

@app_connect.route("/add_connection", methods=["POST"])
def add_connection():
    try:
        id = int(request.form['id'])
        print(id)
        name = request.form['name'].replace(" ", "_")
        ip = request.form['ip'].replace(" ", "")
        driver = request.form['driver'].replace(" ", "")
        slot = int(request.form['slot'].replace(" ", ""))
        rack = int(request.form['rack'].replace(" ", ""))
        with _models.get_db() as db:
            new_connection = _models.ConnectionList(
                id=id,
                name=name,
                driver=driver,
                ip_addres=ip,
                port=102,
                slot=slot,
                rack=rack
            )
            db.add(new_connection)
            db.commit()
            db.refresh(new_connection)
        answer = {
            "status": True,
            "connection": {
                "id": new_connection.id,
                "name": new_connection.name,
                "driver": new_connection.driver,
                "ip_addres": new_connection.ip_addres,
                "port": new_connection.port,
                "slot": new_connection.slot,
                "rack": new_connection.rack
            }
        }
    except Exception as e:
        answer = {
            "status": False,
            "text": str(e),
        }
    return answer