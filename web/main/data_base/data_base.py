from django.db import connection
import datetime


USERS_TABLE = 'USERS_TABLE'
USERS_SET_KEYS = 'Name, Login, Password, TimeCreate'
USERS_GET_KEYS = 'Id, ' + USERS_SET_KEYS


def add_record_to_db(name, login, passw):
    ts = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return db_send_commit(f"INSERT INTO {USERS_TABLE} ({USERS_SET_KEYS}) VALUES ('{name}', '{login}', '{passw}', '{ts}');")


def get_list_from_db():
    return db_send_query(f'SELECT {USERS_GET_KEYS} FROM {USERS_TABLE};')


def get_record_by_id(id):
    return db_send_query(f'SELECT {USERS_GET_KEYS} FROM {USERS_TABLE} WHERE Id = {id}')


def get_change_record_from_db(name, login, passw, id):
    return db_send_commit(f"UPDATE {USERS_TABLE} SET Name = '{name}', Login = '{login}', Password = '{passw}' WHERE Id = {id};")


def delete_record_from_db(id):
    if not get_record_by_id(id):
        return False
    else:
        return db_send_commit(f"DELETE FROM {USERS_TABLE} WHERE Id = {id};")


def db_send_commit(commit):
    result = False
    try:
        cursor = connection.cursor()
        print("Успешное получение курсора")
        cursor.execute(commit)
        connection.commit()
        print('Commit успешно выполнен')
        cursor.close()
        print('Успешное закрытие курсора')
        result = True
    except Exception:
        print(f'Ошибка при работе с базой данных: {Exception}')
    finally:
        return result


def db_send_query(query):
    result = []
    try:
        cursor = connection.cursor()
        print("Успешное получение курсора")
        cursor.execute(query)
        result = cursor.fetchall()
        print('Запрос успешно выполнен')
        cursor.close()
        print('Успешное закрытие курсора')
    except Exception:
        print(f'Ошибка при работе с базой данных: {Exception}')
    finally:
        return result
