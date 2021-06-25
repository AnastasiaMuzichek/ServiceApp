from django.shortcuts import render
from .models import create_table, create_message
from .data_base.data_base import add_record_to_db, get_list_from_db, get_record_by_id, delete_record_from_db
from .data_base.data_base import get_change_record_from_db

MENU = "0"
ACCEPT_COLOR = '#2dfa71'
DENIED_COLOR = '#fa642d'


def process_request_second_lvl(query, content: list):
    method = query['method']
    print(method)
    if method == 'add':

        if not query['name'] or not query['login'] or not query['passw']:
            content['message'] = create_message('НЕКОРРЕКТНЫЙ ВВОД ДАННЫХ!', DENIED_COLOR)
        elif add_record_to_db(query['name'], query['login'], query['passw']):
            content['message'] = create_message('ЗАПИСЬ УСПЕШНО ДОБАВЛЕНА!', ACCEPT_COLOR)
        else:
            content['message'] = create_message('ОШИБКА ПРИ ДОБАВЛЕНИИ ЗАПИСИ!', DENIED_COLOR)

    elif method == 'read':

        if query['id'] == '':
            content['message'] = create_message('ВЫ НЕ ВВЕЛИ ID!', DENIED_COLOR)
        else:
            user = get_record_by_id(query['id'])
            if not user:
                content['message'] = create_message('ЗАПИСЬ ПО ТАКОМУ ID НЕ НАЙДЕНА!', DENIED_COLOR)
            else:
                content['table'] = create_table(user)

    elif method == 'find':

        if query['id'] == '':
            content['message'] = create_message('ВЫ НЕ ВВЕЛИ ID!', DENIED_COLOR)
        else:
            user = get_record_by_id(query['id'])
            content['message'] = ''
            if user == []:
                content['message'] = create_message('ЗАПИСЬ ПО ТАКОМУ ID НЕ НАЙДЕНА!', DENIED_COLOR)
            else:
                content['id'] = user[0][0]
                content['name'] = user[0][1]
                content['login'] = user[0][2]
                content['passw'] = user[0][3]
            print(content)

    elif method == 'change':

        if not query['id'] or not query['name'] or not query['login'] or not query['passw']:
            content['message'] = create_message('НЕКОРРЕКТНЫЙ ВВОД ДАННЫХ!', DENIED_COLOR)
        elif get_change_record_from_db(query['name'], query['login'], query['passw'], query['id']):
            content['message'] = create_message('ЗАПИСЬ УСПЕШНО ОБНОВЛЕНА!', ACCEPT_COLOR)
        else:
            content['message'] = create_message('ОШИБКА ПРИ ОБНОВЛЕНИИ ЗАПИСИ!', DENIED_COLOR)

    elif method == 'delete':

        if query['id'] == '':
            content['message'] = create_message('ВЫ НЕ ВВЕЛИ ID!', DENIED_COLOR)
        else:
            if delete_record_from_db(query['id']):
                content['message'] = create_message('ЗАПИСЬ УДАЛЕНА!', ACCEPT_COLOR)
            else:
                content['message'] = create_message('ОШИБКА ПРИ УДАЛЕНИИ ЗАПИСИ!', DENIED_COLOR)


def process_post_request(request):
    global MENU
    # Запросы 1 - го уровня строятся на ключе btn
    # Запросы 2 - го уровня строятся на ключе method
    query = request.POST
    print('POST', query)
    content = {}
    if 'btn' in query:

        MENU = query['btn']

        if MENU == '2':
            users_list = get_list_from_db()
            if users_list == []:
                content['message'] = create_message('ЗАПИСИ НЕ БЫЛИ НАЙДЕНЫ!')
            else:
                content['table'] = create_table(users_list)

    elif 'method' in query:
        process_request_second_lvl(query, content)

    content['menu'] = MENU
    return render(request, 'main\index.html', content)


def index(request):
    if request.method == 'POST':
        return process_post_request(request)
    else:
        return render(request, 'main\index.html')

