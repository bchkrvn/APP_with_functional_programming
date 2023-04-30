import re
from typing import List, Dict, Any, Set, Callable

from flask import abort
from marshmallow import ValidationError

from container import user_request_schema
from data_classes import UserRequest


def get_result(user_request: UserRequest) -> List[str]:
    """
    Получить итоговый результат
    :param user_request: запрос пользователя
    :return: list
    """
    commands: Dict[str, Callable] = {
        'filter': _filter_data,
        'map': _map_data,
        'unique': _unique_data,
        'sort': _sort_data,
        'limit': _limit_data,
        'regex': _regex_data,
    }
    data = _get_logs(user_request.filename)

    for command in user_request.commands:

        if command.cmd in commands:
            data = commands[command.cmd](data=data, value=command.value)
        else:
            abort(400, 'Wrong command')

    return list(data)


def get_commands(json_commands: Dict[str, Any]) -> UserRequest:
    try:
        return user_request_schema().load(json_commands)
    except ValidationError:
        abort(400, 'wrong data')


def _filter_data(value: str, data: List[str]) -> List[str]:
    """
    Фильтрация данных
    :param value: значение для фильтрации
    :param data: данные
    """
    return list(filter(lambda string: value in string, data))


def _map_data(value: str, data: List[str]) -> List[str]:
    """
    Преобразование данных
    :param value: номер колонки
    :param data: данные
    """
    if not value.isdigit():
        abort(400, 'Bad value')
    return list(map(lambda x: x.split()[int(value)], data))


def _unique_data(data: List, value: None) -> Set[str]:
    """
    Получение уникальных данных
    :param data: данные
    :return: set
    """
    return set(data)


def _sort_data(data: List[str], value: str):
    """
    Сортировка данных
    :param value: выбор вида сортировки
    :param data: данные
    """
    choice = value == 'desc'
    return sorted(list(data), key=lambda x: x.split()[3], reverse=choice)


def _limit_data(data: List[str], value: str) -> List[str]:
    """
    Ограничение данных
    :param value: лимит
    :param data: данные
    :return: list
    """
    if not value.isdigit():
        abort(400, 'Bad value')
    return list(data)[:int(value)]


def _regex_data(data: List[str], value: str) -> List[str]:
    regexp = re.compile(value, re.DOTALL)
    return [string for string in data if regexp.search(string)]


def _get_logs(filename: str) -> List[str]:
    """
    Генератор получения данных из файла
    :param filename: название файла
    :return: iter
    """
    try:
        with open(f'./data/{filename}', 'r', encoding='utf-8') as file:
            return list(file.readlines())

    except FileNotFoundError:
        abort(400, 'Bad filename')
