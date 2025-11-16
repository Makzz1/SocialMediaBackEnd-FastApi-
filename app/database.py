import psycopg2
from psycopg2.extras import RealDictCursor
import time

conn = None
cursor = None

def startup():
    while True:
        try:
            global conn,cursor
            conn = psycopg2.connect(host='localhost',
                                    database='fastapi',
                                    user='postgres',
                                    password='1@Maghizh',
                                    cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print("database is connecteed")
            break

        except Exception as e:
            print(e,"connection to data base is falied")
            time.sleep(2)

def shutdown():
    cursor.close()
    conn.close()