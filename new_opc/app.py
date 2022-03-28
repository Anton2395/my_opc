from flask import Flask, jsonify, request
import uvicorn as _uvicorn
import multiprocessing as _mp

from connection.connection import app_connect
from main import app_process 
from DB import models as _models
from tool_func import control_background_processors as _service_process
from connection import services as _service_connection

process_connect = {}
process_status = {}

app = Flask('opc_service', static_url_path='',
            static_folder='static', template_folder='template')

# add router file
app.register_blueprint(app_connect, url_prefix="/connections")
app.register_blueprint(app_process, url_prefix="/process")


@app.route('/', methods=['GET'])
def index() -> str:
    str = ""
    for index, connect_str in enumerate(process_connect):
        str += f"{index+1}. {connect_str}\n"
    return str


@app.route('/delete/', methods=['POST'])
def delete_process():
    """
    Принимает параметр "name_connection" и удаляет его из базы данных и из списка процессов

    Пример: ::

        {
            "name_connection": <str>
        }
    
    """
    name_connection = request.get_json()["name_connection"]
    with _models.get_db() as db:
        if _service_connection.delete_connection_from_name(db=db, name_connection=name_connection):
            Response = "delete from db - DONE\n"
        else:
            Response = "delete from db - ERROR\n"
    if name_connection in process_connect:
        if _service_process.delete_process(all_work_process=process_connect, name_delete_porcess=name_connection):
            Response += "Process delete - DONE"
        else:
            Response += "Process delete - ERROR"
    else:
        Response += "Process delete - ERROR"
    return Response


@app.route('/stop/<name_process>', methods=['POST'])
def stop_process(name_process: str) -> str:
    if _service_process.stop_process(all_work_process=process_connect, name_stop_process=name_process):
        return "Process stop DONE"
    else:
        return "Process stop ERROR"


@app.route("/status/", methods=["GET"])
def get_status() -> dict:
    response = []
    for name_process in process_connect:
        response.append({
            "name": name_process,
            "process": process_connect[name_process]["process"].is_alive(),
            "connect": process_connect[name_process]["status"].value
        })
    return jsonify(response)



if __name__ == "__main__":
    # _mp.set_start_method("fork")
    _service_process.start_all_process(all_work_process=process_connect)
    _service_process.start_flask(app)

