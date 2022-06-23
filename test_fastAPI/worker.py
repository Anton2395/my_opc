import os
import multiprocessing as _mp
from ctypes import c_bool

from celery import Celery

from services import generate_dict as _gen_dict
from core import processor as _processor

celery = Celery('tasks', broker='pyamqp://guest@localhost//')
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@celery.task
def add(x, y):
    print(x+y)
    return x + y


process_connect = {}

@celery.task
def start_process(proc_dict:dict):
    """
    Запускает процесс

    - **db** : объект соединения с БД
    - **process_connect** : словарь со всеми добавленными в работу процессами
    - **id_proc** : id запускаемого процесса
    """
    if proc_dict["driver"] == "Snap7":
        process_connect[proc_dict["name"]] = {}
        process_connect[proc_dict["name"]]["status"] = _mp.Value(c_bool, False)
        process_connect[proc_dict["name"]]["stop"] = _mp.Value(c_bool, False)
        process_connect[proc_dict["name"]]["process"] = _processor.ConnectSnapProcess(
                name_connect=proc_dict["name"],
                ip=proc_dict["ip"],
                port=proc_dict["port"],
                slot=proc_dict["slot"],
                rack=proc_dict["rack"],
                values=proc_dict["area"],
                stop_point=process_connect[proc_dict["name"]]["stop"],
                status=process_connect[proc_dict["name"]]["status"]
            )
        process_connect[proc_dict["name"]]["process"].start()
    return True