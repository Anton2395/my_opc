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

    def __init__(self, name_connect:str, ip:str, port:int, slot:int, rack:int, values:list, status:object):
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
        self.rack = rack
        self.slot = slot
        self.port = port
        self.values_list = values
        self.values = {}
        self._conn = createConnection()
        self._c = self._conn.cursor()
        self.bytearray_data_math = {}
        self.client = snap7.client.Client()
        self.client.set_connection_type(3)
        try:
            self.client.connect(self.ip, self.rack, self.slot, tcpport=self.port)
        except:
            print("Error connect to PLC")
        super(ConnectSnapProcess, self).__init__()

    # def __get_db_data(self, area) -> bool:  # получение данных в байт формате
    #     """
    #     получение данных из ДБ блока в формате bytearray
    #     """
    #     try:
    #         if area["area_memory"] == 'DB':
    #             self.bytearray_data = self.client.db_read(area["db"], area["start"], area["size"])
    #             return True
    #         elif area["area_memory"] == 'PA':
    #             self.bytearray_data = self.client.read_area(snap7.types.areas['PA'], 0, area["start"], area["size"])
    #             return True
    #         else:
    #             return False
    #     except Exception as e:
    #         print(f"Can't get data from PLC. Text error: \n{e}")
    #         return False
    
    def __get_math_data_from_db(self, area:dict) -> bool:
        """
        получение данных из PLC в формате bytearray
        """
        try:
            read_count = len(area)
            for addres_data in area:
                if addres_data["area_memory"] == 'DB':
                    self.bytearray_data_math[addres_data["name"]] = self.client.db_read(
                        addres_data["db"],
                        addres_data["start"],
                        addres_data["size"]
                    )
                    read_count -= 1
                elif addres_data["area_memory"] == 'PA':
                    self.bytearray_data_math[addres_data["name"]] = self.client.read_area(
                        snap7.types.areas['PA'],
                        0,
                        addres_data["start"],
                        addres_data["size"]
                    )
                    read_count -= 1
            if read_count == 0:
                return True
            else:
                return False
        except Exception as e:
            print(f"Can't get math data from PLC. Text error: \n{e}")
            return False

    def __reconect_to_plc(self) -> bool:
        #DONE
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
            self.status.value = False
            time.sleep(3)
            return False



    def __create_table_if_not_exist(self) -> None:
        #DONE
        """фнкция создания таблиц в БД"""
        for area in self.values_list:
            if area["type_math_value"] == 'int':
                type_sql = 'INT'
            if area["type_math_value"] == 'float':
                type_sql = 'REAL'
            if area["type_math_value"] == 'double':
                type_sql = 'BIGINT'
            area['table_name'] =  self.name_connect + "_" + area["name"]
            self._c.execute(f'''CREATE TABLE IF NOT EXISTS mvlab_{area['table_name']}
                                (key serial primary key,
                                now_time TIMESTAMP  WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                value {type_sql})''')
            self._conn.commit()
            print('create table')

    def __parse_bytearray(self, value_param_list: list) -> any:
        """разбор полученных данных с ПЛК"""
        #DONE
        result = {}
        for value_param in value_param_list:
            type = value_param['type_value']
            start = value_param['start']
            if (type == 'int'):
                offset = 2
                end = int(start) + int(offset)
                result[value_param["name"]] = self.disassemble_int(self.bytearray_data[int(start):int(end)])
                if value_param['divide']:
                    result[value_param["name"]] = result[value_param["name"]] / int(value_param['divide_num'])
            elif (type == 'float'):
                offset = 4
                end = int(start) + int(offset)
                result[value_param["name"]] = self.disassemble_float(self.bytearray_data[int(start):int(end)])
            elif (type == 'double'):
                offset = 4
                end = int(start) + int(offset)
                result[value_param["name"]] = self.disassemble_int(self.bytearray_data[int(start):int(end)])
                if value_param['divide']:
                    result[value_param["name"]] = result[value_param["name"]] / int(value_param['divide_num'])
        return result

    def __write_to_db(self, tablename, value) -> None:
        """Запись распаршеных данных в БД"""
        self._c.execute(
            '''INSERT INTO mvlab_''' + tablename + ''' (value) VALUES (''' + str(value) + ''');''')

    def _thread_for_write_data(self, value_param_list: list) -> None:
        value = self.__parse_bytearray(value_param_list)#DONE
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
        self.__create_table_if_not_exist()  # создание таблиц если их нет DONE
        while True:
            try:
                for area in self.values_list:
                    if (not self.__get_math_data_from_db(area["area"])):#DONE
                        self.__reconect_to_plc()#DONE
                    else:
                        threads = list()
                        for value in area["area"]:
                            data_get_process = threading.Thread(target=self._thread_for_write_data, args=(value["value"],))
                            threads.append(data_get_process)
                            while threading.active_count() > 250:
                                time.sleep(0.01)
                            data_get_process.start()
                        self.status.value = True
                    for thread in threads:
                        thread.join()
                    self._conn.commit()
                # for math_area in self.math_values_list:
                #     for area in math_area["area"]:
                #         if (not self.__get_math_data_from_db(area)):
                #             self.__reconect_to_plc()
                #             self.status.value = False
                #         else:
                #             threads_math = list()
                #             data_get_math_process = threading.Thread(args=(area,))

                #     pass
                    
            except:
                self.status.value = False

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
