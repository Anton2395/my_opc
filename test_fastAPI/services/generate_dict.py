from sqlalchemy import orm as _orm

from DB import models as _models

def gen_dict_con(id:int, db:_orm.Session):
    return create_connection_param(db.query(_models.ConnectionList).filter(_models.ConnectionList.id==id)[0])

def create_connection_param(query_connect) -> dict:
    data_connect = {
        "name": query_connect.name,
        "driver": query_connect.driver,
        "ip": query_connect.ip_addres,
        "port": query_connect.port,
        "slot": query_connect.slot,
        "rack": query_connect.rack,
        "switchr": query_connect.switchr,
        "matharea": create_list_math_value(query_connect.matharea),
        "area": create_list_value(query_connect.area)
    }
    return data_connect

def create_list_value(area_list) -> list:
    value_list = []
    for area in area_list:
        area_param = {
            "name": area.name,
            "area_memory": area.area_memory,
            "db": area.db,
            "start": area.start,
            "size": area.size,
            "value": []
        }
        for value in area.valuelist:
            area_param["value"].append(create_db_value(value))
        value_list.append(area_param)
    return value_list


def create_db_value(query_value) -> dict:
    data = {
        "start": query_value.start,
        "name": query_value.name_val,
        "type_value": query_value.type_value_get_data,
        "type_table": query_value.type_value_write_data,
        "if_change": query_value.if_change,
        "divide": query_value.divide,
        "divide_num": query_value.divide_number,
        "time_write": query_value.time_write_if_change,
        "time_rewrite": query_value.time_rewrite,
        "bit": query_value.bit
    }
    return data

def create_list_math_value(math_area_list):
    math_areas = []
    for area in math_area_list:
        dict_data = {
            "name_math_value": area.name_math_value,
            "type_math_value": area.type_math_value,
            "viragenie": area.viragenie,
            "area": create_list_value(area.area)
        }
        math_areas.append(dict_data)
    return math_areas