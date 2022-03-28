from flask import Blueprint, render_template, request, redirect, url_for, abort



from DB import models as _models
from connection import services as _services


app_connect = Blueprint('connections', __name__)

@app_connect.route("/", methods=["GET", "POST"])
def list_connections():
    if request.method == "GET":
        with _models.get_db() as db:
            connections_db = _services.get_all_connections(db)
        return render_template('connection/index.html', connections=connections_db)


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
        