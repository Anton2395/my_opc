import multiprocessing as _mp
from ctypes import c_bool
import time as _tm

import sqlalchemy.orm as _orm

from DB import models as _models
from services import generate_dict as _gen_dict
from core import processor as _processor




def start_proc_switcher_on(process_connect: dict)-> None:
    try:
        db = _models.SessionLocal()
        for connect in db.query(_models.ConnectionList).all():
            if connect.switchr == True:
                proc_dict = _gen_dict.gen_dict_con(id=connect.id, db=db)
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
    except Exception as e:
        print(e)
        return False


def start_process(db: _orm.Session, id_proc: int, process_connect: dict):
    """
    Запускает процесс

    - **db** : объект соединения с БД
    - **process_connect** : словарь со всеми добавленными в работу процессами
    - **id_proc** : id запускаемого процесса
    """
    try:
        proc_dict = _gen_dict.gen_dict_con(id=id_proc, db=db)
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
    except:
        return False


def stop_process(all_work_process: dict, db: _orm.Session, id: int) -> bool:
    """
    Останавливает процесс

    - **all_work_process** : словарь со всеми добавленными в работу процессами
    - **name_stop_process** : имя останавливаемого процесса
    """
    try:
        connect = db.query(_models.ConnectionList).filter(_models.ConnectionList.id==id)[0]
        name_stop_process = connect.name
        if all_work_process[name_stop_process]["process"].is_alive():
            all_work_process[name_stop_process]["stop"].value = True
        del all_work_process[name_stop_process]
        return True
    except Exception as e:
        print(e)
        return False