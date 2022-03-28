# import sqlite3
import psycopg2


BASE_DIR_DB ='test.db'



def createConnection():
    # return sqlite3.connect(BASE_DIR_DB, check_same_thread=False)
    return psycopg2.connect(dbname='postgres', user='mvlab',
                                password='z1x2c3', host='10.0.1.2',
                                port=5432)
    