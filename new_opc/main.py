from crypt import methods
from flask import Blueprint

# from app import start_flask
from tool_func.create_value_list_and_other import create_all_param
from DB.models import Session


all_param = [123]
process_connect = {}

app_process = Blueprint('process', __name__)

@app_process.route('/', methods=['GET'])
def list_process():
    return str(all_param)


def start_process_back():
    all_param = create_all_param(Session())
    # start_process(all_param=all_param)