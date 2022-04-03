from contextlib import contextmanager

from sqlalchemy import Float, create_engine, delete
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('postgresql+psycopg2://mvlab:z1x2c3@10.0.1.2:5432/postgres')
base = declarative_base()

class ConnectionList(base):
    """
    Таблица хронящая сущности для подключения к устройства. Хранит в себе следующие параметры:

    * `id`(int) - уникальный идентификатор записи 
    * `name`(str) - уникальное имя устройства
    * `driver`(str) - драйвер используемый для сбора данных
    * `ip_addres`(str) - IP адрес устройства с которого забираются данные
    * `port`(int) - порт для соединения с устройством
    * `slot`(int) - слот устройства (параметр для драйвера `snap7`)
    * `rack`(int) - ракель устройства (параметр для драйвера `snap7`)
    """
    __tablename__ = 'connectionlist'
    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String(30), nullable=False, unique=True, default='No name')
    driver = Column(String(20), nullable=False)
    ip_addres = Column(String(15), nullable=False)
    port = Column(Integer, nullable=False)
    slot = Column(Integer, nullable=False)
    rack = Column(Integer, nullable=False)
    switchr = Column(Boolean, nullable=False, default=False)
    area = relationship('Area', cascade="all, delete")
    matharea = relationship('MathArea', cascade="all, delete")
 

class MathArea(base):
    """
    Таблица для определения вида записываемых данных (простая запись или с производимым предварительным расчётом)
    """
    __tablename__ = "matharea"
    id = Column(Integer, primary_key=True)
    connection_id = Column(Integer, ForeignKey('connectionlist.id'), nullable=False)
    name_math_value = Column(String(30), nullable=True)
    type_math_value = Column(String(5), nullable=False)
    viragenie = Column(String(150), nullable=True)
    area = relationship("Area", cascade="all, delete")

class Area(base):
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True)
    connection_id = Column(Integer, ForeignKey('connectionlist.id'), nullable=True)
    matharea_id = Column(Integer, ForeignKey('matharea.id'), nullable=True)
    name = Column(String(20), nullable=True)
    area_memory = Column(String(15), nullable=True)
    group = Column(Boolean, nullable=False, default=False)
    valuelist = relationship('ValueList', cascade="all, delete")
    db = Column(Integer, nullable=True)
    start = Column(Integer, nullable=False)
    size = Column(Integer, nullable=True)
    valuelist = relationship('ValueList', cascade="all, delete")
    

class ValueList(base):
    __tablename__ = 'valuelist'
    id = Column(Integer, primary_key=True)
    area_id = Column(Integer, ForeignKey('area.id'), nullable=False)
    start = Column(Integer, nullable=False)
    name_val = Column(String(60), nullable=False)
    type_value_get_data = Column(String(10))
    type_value_write_data = Column(String(10))
    if_change = Column(Boolean, nullable=False, default=False)
    divide = Column(Boolean, nullable=False, default=False)
    divide_number = Column(Float, nullable=True, default=1)
    time_write_if_change = Column(Integer, default=1000)
    time_rewrite = Column(Integer, default=120)
    bit = Column(Integer, nullable=True)



base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

@contextmanager
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()