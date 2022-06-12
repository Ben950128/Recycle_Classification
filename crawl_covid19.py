from numpy import rec
import requests  
import json
from mysql.connector import pooling
from dotenv import load_dotenv
import os

load_dotenv()
MYSQL_DB_HOST = os.getenv('MYSQL_DB_HOST')
MYSQL_DB_DATABASE = os.getenv('MYSQL_DB_DATABASE')
MYSQL_DB_USER = os.getenv('MYSQL_DB_USER')
MYSQL_DB_PASSWORD = os.getenv('MYSQL_DB_PASSWORD')

connection_pool = pooling.MySQLConnectionPool(
    pool_name="mysql_pool",
    pool_size=5,
    pool_reset_session=True,
    host=MYSQL_DB_HOST,
    database=MYSQL_DB_DATABASE,
    user=MYSQL_DB_USER,
    password=MYSQL_DB_PASSWORD,
)
connection_object = connection_pool.get_connection()
cursor = connection_object.cursor()

response = requests.get("https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4001&limited=TWN")
date = json.loads(response.text)[0]["a04"]
total_count = json.loads(response.text)[0]["a05"]
count = json.loads(response.text)[0]["a06"]
sql = "select date from COVID19 where date = %s"
val = (date,)
cursor.execute(sql, val)
records_covid = cursor.fetchall()

if records_covid == []:
    sql = "insert into COVID19(date, total_count, count) values(%s, %s, %s)"
    val = (date, total_count, count)
    cursor.execute(sql, val)
    connection_object.commit()

cursor.close()
connection_object.close()