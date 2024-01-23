import time

import psycopg2

from psycopg2 import sql
from datetime import datetime

def connect_db():
    """
    postgresql DB connection
    """
    connection = psycopg2.connect(
        host="192.168.103.13",
        port="5432",
        user="qaauto",
        password="qadb29cm",
        database="ui_automation_log"
    )
    cursor = connection.cursor()
    return connection, cursor


def insert_data(connection, cursor, self, result_data):
    """
    column_name: platform, error_code, error_reason, timestamp, error_scenario, test_result, test_progress_time
    """
    # 삽입할 데이터
    if result_data.get("test_result") == 'PASS':
        data_to_insert = {
            "platform": self.device_platform,
            "error_code": None,
            "error_reason": None,
            "insert_time": datetime.now(),
            "error_scenario": result_data.get("test_name"),
            "test_result": result_data.get("test_result"),
            "test_progress_time": result_data.get("run_time")
        }
    else:
        data_to_insert = {
            "platform": self.device_platform,
            "error_code": result_data.get("error_texts")[0],
            "error_reason": result_data.get("error_texts")[1],
            "insert_time": datetime.now(),
            "error_scenario": result_data.get("test_name"),
            "test_result": result_data.get("test_result"),
            "test_progress_time": result_data.get("run_time")
        }

    # SQL 쿼리 생성 및 실행
    insert_query = """
           INSERT INTO test_result (
               platform, error_code, error_reason, insert_time, error_scenario, test_result, test_progress_time
           ) VALUES (%s, %s, %s, %s, %s, %s, %s)
       """

    cursor.execute(insert_query, (
        data_to_insert["platform"],
        data_to_insert["error_code"],
        data_to_insert["error_reason"],
        data_to_insert["insert_time"],
        data_to_insert["error_scenario"],
        data_to_insert["test_result"],
        data_to_insert["test_progress_time"],
    ))

    # 변경사항 저장
    connection.commit()


def disconnect_db(connection, cursor):
    cursor.close()
    connection.close()


# try:
#     connection, cursor = connect_db()
#     result = insert_data(cursor)
#     disconnect_db(cursor, connection)
# except Exception as e:
#     print(e)
#     disconnect_db(cursor, connection)