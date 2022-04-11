import datetime
import multiprocessing
import struct
import threading
import time
from multiprocessing import Process
import snap7
from snap7.util import get_bool
import sqlite3
import ctypes

from core.DB_connect import createConnection


class ConnectSnapProcess(Process):

    def __init__(self, name_connect:str, ip:str, port:int, slot:int, rack:int,
                status:object, stop_point:object, values:list=[]):
        """Класс процесса для подключения к ПЛК по адресу address, с портом port (по умолчанию 102) и получения заданных
        значений из блока данных db в промежутке с start_address_db по start_address_db+offset_db
        (offset_db - количество забираемых byte из блока). После получения данных разбирает bytearray по
        списку values_list.

        :param ip: ip адрес ПЛК
        :param rack:  линейка ПЛК (смотри в Step7 или Tia POrtal)
        :param slot: номер слота ПЛК (смотри в Step7 или Tia POrtal)
        :param values: список значений которые взять из ПЛК
        :param port: номер порта (по умолчанию 102)
        :param name_connect: префикс названия таблиц для подключения
        :param status: статус соединения(передаётся Value из multiprocessing)
        

        """

        self.name_connect = name_connect
        self.ip = ip
        self.status = status
        self.stop_point = stop_point
        self.rack = rack
        self.slot = slot
        self.port = port
        self.values_list = values
        self.bytearray_data = bytearray()
        self.values = {}
        self._conn = createConnection()
        self._c = self._conn.cursor()
        
        self.client = snap7.client.Client()
        self.client.set_connection_type(3)
        try:
            # print(self.ip, self.rack, self.slot, self.port)
            self.client.connect(self.ip, self.rack, self.slot, tcpport=self.port)
            print("Connect to PLC DONE")
            self.status.value = True
        except:
            print("Error connect to PLC")
        super(ConnectSnapProcess, self).__init__()

    def __get_db_data(self, area) -> bool:  # получение данных в байт формате
        """
        получение данных из ДБ блока в формате bytearray
        """
        try:
            if area["area"] == 'DB':
                self.bytearray_data = self.client.db_read(area["db"], area["start"], area["size"])
                return True
            elif area["area"] == 'PA':
                self.bytearray_data = self.client.read_area(snap7.types.areas['PA'], 0, area["start"], area["size"])
                return True
            else:
                return False
        except Exception as e:
            print("Can't get data from PLC. Text error:")
            print(e)
            return False

    def __reconect_to_plc(self) -> bool:
        """пере подключение к плк в случае ошибки валидации данных"""
        print(f"Try connect to PLC, name_connect:{self.name_connect} \n ip address: {self.ip}")
        self.client.destroy()
        try:
            self.client = snap7.client.Client()
            self.client.set_connection_type(3)
            self.client.connect(self.ip, self.rack, self.slot, tcpport=self.port)
            print(f"Reconnect name_connect:{self.name_connect}, ip address: {self.ip} --- DONE")
            # cprint.cprint.info("Good connect to %s" % self.address)

            self.status.value = True
            return True
        except:
            time.sleep(3)
            return False



    def __create_table_if_not_exist(self) -> None:
        """фнкция создания таблиц в БД"""
        for area in self.values_list:
            for value in area["value"]:
                if value["type_table"] == 'int':
                    type_sql = 'INT'
                if value["type_table"] == 'float':
                    type_sql = 'REAL'
                if value["type_table"] == 'double':
                    type_sql = 'BIGINT'
                if value["type_table"] == 'bool':
                    type_sql = 'INT'
                value['table_name'] =  self.name_connect + "_" + area["name"] + "_" + value["name"]
                self._c.execute(f'''CREATE TABLE IF NOT EXISTS mvlab_{value['table_name']}
                                    (key serial primary key,
                                    now_time TIMESTAMP  WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                    value {type_sql})''')
                self._conn.commit()
                print('create table')

    def __parse_bytearray(self, value_param: dict) -> any:
        """разбор полученных данных с ПЛК"""
        type = value_param['type_value']
        start = value_param['start']
        if (type == 'int'):
            offset = 2
            end = int(start) + int(offset)
            result = self.disassemble_int(self.bytearray_data[int(start):int(end)])
            if value_param['divide']:
                result = result / int(value_param['divide_num'])
        elif (type == 'float'):
            offset = 4
            end = int(start) + int(offset)
            result = self.disassemble_float(self.bytearray_data[int(start):int(end)])
        elif (type == 'double'):
            offset = 4
            end = int(start) + int(offset)
            result = self.disassemble_int(self.bytearray_data[int(start):int(end)])
            if value_param['divide']:
                result = result / int(value_param['divide_num'])
        elif (type == 'bool'):
            bit = value_param['bit']
            result = self.from_bytearray_to_bit(bit=bit, start=start)
        else:
            result = False
        return result

    def __write_to_db(self, tablename, value) -> None:
        """Запись распаршеных данных в БД"""
        self._c.execute(
            '''INSERT INTO mvlab_''' + tablename + ''' (value) VALUES (''' + str(value) + ''');''')

    def _thread_for_write_data(self, value_param) -> None:
        #DONE
        value = self.__parse_bytearray(value_param)
        if type(value) == bool:
            value = int(value)
        now = datetime.datetime.now()
        minimal_write_time = value_param["time_write"] / 1000
        
        if 'if_change' in value_param and value_param["if_change"] and not value_param["table_name"] in self.values:
            print(self.values)
            self.values[value_param["table_name"]] = value
            self.values[f'write_time_{value_param["table_name"]}'] = datetime.datetime.now()
            self.__write_to_db(tablename=value_param["table_name"], value=value)
            
        if 'if_change' in value_param and value_param['if_change'] and \
            (self.values[value_param['table_name']] != value or \
            ((now - self.values[f'write_time_{value_param["table_name"]}']).total_seconds() > value_param['time_rewrite']*60)):
            if (now - self.values[f'write_time_{value_param["table_name"]}']).total_seconds() > minimal_write_time:
                print((now - self.values[f'write_time_{value_param["table_name"]}']).total_seconds(), minimal_write_time)
                self.values[value_param['table_name']] = value
                self.values[f'write_time_{value_param["table_name"]}'] = datetime.datetime.now()
                self.__write_to_db(tablename=value_param["table_name"], value=value)
                
        if 'if_change' in value_param and not value_param['if_change']:
            if not f'write_time_{value_param["table_name"]}' in self.values or \
                 (now - self.values[f'write_time_{value_param["table_name"]}']).total_seconds() > minimal_write_time:
                print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                self.values[f'write_time_{value_param["table_name"]}'] = datetime.datetime.now()
                self.__write_to_db(tablename=value_param['table_name'], value=value)


    def run(self):
        self.__create_table_if_not_exist()  # создание таблиц если их нет
        while True:
            time.sleep(1)
            try:
                if self.stop_point.value:
                    break
                for area in self.values_list:
                    if (not self.__get_db_data(area)):
                        self.__reconect_to_plc()
                        self.status.value = False
                    else:
                        threads = list()
                        for value in area["value"]:
                            data_get_process = threading.Thread(target=self._thread_for_write_data, args=(value,))
                            threads.append(data_get_process)
                            while threading.active_count() > 250:
                                time.sleep(0.01)
                            data_get_process.start()
                        self.status.value = True
                    for thread in threads:
                        thread.join()
                    self._conn.commit()                    
            except:
                self.status.value = False
        self.stop_point.value = False

    def disassemble_float(self, data) -> float:  # метод для преобразования данных в real
        val = struct.unpack('>f', data)
        return val[0]

    def disassemble_double(self, data) -> int:  # метод для преобразования данных в bigint
        val = struct.unpack('>d', data)
        return val[0]

    def disassemble_int(self, data) -> int:  # метод для преобразования данных в int
        return int.from_bytes(data, "big", signed=True)

    def from_bytearray_to_bit(self, bit, start) -> int:
        value = int.from_bytes(self.bytearray_data[int(start):int(start) + 1], byteorder='little', signed=True)
        bits = bin(value)
        bits = bits.replace("0b", "")
        bits = bits[::-1]
        try:
            # result = bits[bit]
            result = get_bool(self.bytearray_data[int(start):int(start) + 1], 0, bit)
        except:
            result = 0
        return result
