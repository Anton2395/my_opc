import time as _tm

from flask import Blueprint, render_template, request, redirect, url_for, abort




app_value = Blueprint('valuelist', __name__)


@app_value.route("/", methods=["GET"])
def list_value_page():
    return render_template('valuelist/index.html')

@app_value.route("/list_volue/<id_connection>", methods=["GET"])
def list_value_data(id_connection: int) -> str:
    data = {}
    _tm.sleep(2)
    return data