from lib2to3.pgen2 import driver
from pydantic import BaseModel
import datetime as _dt
from typing import Union

class ConnectionCreate(BaseModel):
    name: str
    driver: str
    ip_addres: str
    port: int
    slot: int
    rack: int
    switchr: bool

    class Config:
        orm_mode = True


class Connection(ConnectionCreate):
    id: int

class MathAreaChange(BaseModel):
    name_math_value: str
    type_math_value: str
    viragenie: str

class MathAreaCreate(MathAreaChange):
    connection_id: int

class MathArea(MathAreaCreate):
    id: int

class AreaChange(BaseModel):
    name: str
    area_memory: str
    group:bool
    db: int
    start: int
    size: int

    class Config:
        orm_mode = True

class AreaCreate(AreaChange):
    connection_id: int
    
class Area(AreaCreate):
    id: int

class ValueChange(BaseModel):
    start: int
    name_val: str
    type_value_get_data: str
    type_value_write_data: str
    if_change: bool
    divide: bool
    divide_number: Union[float, None]
    time_write_if_change: int
    time_rewrite: int
    bit: Union[int, None]

    class Config:
        orm_mode = True

class ValueCreate(ValueChange):
    area_id: int

class Value(ValueCreate):
    id: int

class AreaAll(Area):
    valuelist: list[Value]

class MathAreaAll(MathArea):
    area: list[AreaAll]

class AllData(Connection):
    area: list[AreaAll]
    matharea: list[MathAreaAll]

class StatusCommand(BaseModel):
    status: bool
    text: str

class Command(BaseModel):
    id: int
    name: str