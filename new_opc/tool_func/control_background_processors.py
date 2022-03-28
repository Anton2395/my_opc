from ctypes import c_bool
import time as _time
import multiprocessing as _mp


from core import processor as _processor
from tool_func import create_value_list_and_other as _generator_db
from DB import models as _models


def add_new_process(all_work_process: dict, new_name_connection: str, all_work_status:dict) -> bool:
    """
    Добавляет в словарь новый процесс, но не запускает его

    - **all_work_process** : словарь со всеми добавленными в работу процессами
    - **new_name_connection** : имя запускаемого нового процесса 
    """
    try:
        for connection in _generator_db.create_all_param():
            if connection["name"] == new_name_connection:
                all_work_status[new_name_connection] = _mp.Value(c_bool, False)
                all_work_process[new_name_connection] = _processor.ConnectSnapProcess(
                    name_connect=connection["name"],
                    ip=connection["ip"],
                    port=connection["port"],
                    slot=connection["slot"],
                    rack=connection["rack"],
                    values=connection["area"],
                    status=all_work_status[new_name_connection]
                )
                break
        return True
    except:
        return False


def delete_process(all_work_process: dict, name_delete_porcess: str) -> bool:
    """
    Останавливает (если это необходимо) и удаляет процесс из общего словоря процессов

    - **all_work_process** : словарь со всеми добавленными в работу процессами
    - **name_delete_process** : имя удаляемого процесса
    """
    try:
        while all_work_process[name_delete_porcess]["process"].is_alive():
            all_work_process[name_delete_porcess]["process"].terminate()
            _time.sleep(1)
        del all_work_process[name_delete_porcess]
        with _models.get_db() as db:
            connection_db = db.query(_models.ConnectionList).filter(_models.ConnectionList.name==name_delete_porcess).first()
            db.delete(connection_db)
            db.commit()
        return True
    except:
        return False


def start_process(all_work_process: dict, name_started_process: str) -> bool:
    """
    Запускает процесс

    - **all_work_process** : словарь со всеми добавленными в работу процессами
    - **name_started_process** : имя запускаемого процесса
    """
    try:
        while all_work_process[name_started_process]["process"].is_alive():
            all_work_process[name_started_process]["process"].start()
            _time.sleep(1)
        return True
    except:
        return False


def stop_process(all_work_process: dict, name_stop_process: str) -> bool:
    """
    Останавливает процесс

    - **all_work_process** : словарь со всеми добавленными в работу процессами
    - **name_stop_process** : имя останавливаемого процесса
    """
    try:
        while all_work_process[name_stop_process]["process"].is_alive():
            all_work_process[name_stop_process]["process"].terminate()
            _time.sleep(1)
        return True
    except:
        return False


def start_all_process(all_work_process: dict) -> bool:
    """
    Запуск Всех процессов на основе данных из базы

    - **all_work_process** : словарь со всеми добавленными в работу процессами
    """
    try:
        print("start all process - load")
        for connect in _generator_db.create_all_param():
            if connect["driver"] == "snap7":
                all_work_process[connect["name"]] = {}
                
                all_work_process[connect["name"]]["status"] = _mp.Value(c_bool, False)
                all_work_process[connect["name"]]["process"] = _processor.ConnectSnapProcess(
                    name_connect=connect["name"],
                    ip=connect["ip"],
                    port=connect["port"],
                    slot=connect["slot"],
                    rack=connect["rack"],
                    values=connect["area"],
                    status=all_work_process[connect["name"]]["status"]
                )

            all_work_process[connect["name"]]["process"].start()
        print("start all process - done")
        all_work_process["test"].terminate()
        return True
    except Exception as e:
        print(e)
        print("start all process - error")
        return False


def start_flask(app_flask: object) -> bool:
    """
    Запуск Flask

    - **app_flask** : главный объект Flask
    """
    try:
        app_flask.run(host='0.0.0.0', port=8000, debug=True, use_reloader=True)
        return True
    except Exception as e:
        print(e)
        return False