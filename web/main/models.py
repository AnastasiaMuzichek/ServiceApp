from django.db import models


# Create your models here.


def add_row_in_table(values: list) -> str:
    row = '<tr>'
    for x in values:
        row += f'<td>{x}</td>'
    row += '</tr>'
    return row


def create_message(text, color: str) -> str:
    return f'<span class="message" style="color:{color}">{text}</span>'


def create_table(my_list: list) -> str:
    table = '<table border="5"><tr><th>ID</th><th>Имя</th><th>Логин</th><th>Пароль</th><th>Время Создания</th></tr>'
    for x in my_list:
        table += add_row_in_table(x)
    table += '</table>'
    return table
