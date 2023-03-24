from flask import abort


def get_result(querys: tuple, file_name: str) -> list:
    """
    Получить итоговый результат
    :param querys: запросы
    :param file_name: имя файла
    :return: list
    """
    strings = _get_string(file_name)
    query_1 = querys[0]
    query_2 = querys[1]
    res = _choose_command(command=query_1[0], value=query_1[1], data=strings)
    res = _choose_command(command=query_2[0], value=query_2[1], data=res)
    return list(res)


def _choose_command(command: str, value: str, data):
    """
    Произвести обработку по названию команды
    :param command: название команды
    :param value: значение для команды
    :param data: данные
    :return: данные после обработки
    """
    if command == 'filter':
        return _filter_data(value, data)
    elif command == 'map':
        return _map_data(value, data)
    elif command == 'unique':
        return _unique_data(data)
    elif command == 'sort':
        return _sort_data(value, data)
    elif command == 'limit':
        return _limit_data(value, data)
    else:
        abort(400, 'Bad command')


def _filter_data(value: str, data: iter) -> iter:
    """
    Фильтрация данных
    :param value: значение для фильтрации
    :param data: данные
    """
    return filter(lambda string: value in string, data)


def _map_data(value: str, data: iter) -> iter:
    """
    Преобразование данных
    :param value: номер колонки
    :param data: данные
    """
    if not value.isdigit():
        abort(400, 'Bad value')
    return map(lambda x: x.split()[int(value)], data)


def _unique_data(data: iter) -> set:
    """
    Получение уникальных данных
    :param data: данные
    :return: set
    """
    return set(data)


def _sort_data(value: str, data: iter):
    """
    Сортировка данных
    :param value: выбор вида сортировки
    :param data: данные
    """
    if value == 'asc':
        choice = False
    elif value == 'desc':
        choice = True
    else:
        abort(400, 'Bad value')

    return sorted(list(data), key=lambda x: x.split()[3], reverse=choice)


def _limit_data(value: str, data: iter) -> list:
    """
    Ограничение данных
    :param value: лимит
    :param data: данные
    :return: list
    """
    if not value.isdigit():
        abort(400, 'Bad value')
    return list(data)[:int(value)]


def _get_string(filename: str) -> iter:
    """
    Генератор получения данных из файла
    :param filename: название файла
    :return: iter
    """
    with open(f'./data/{filename}', 'r', encoding='utf-8') as file:
        for string in file.readlines():
            yield string
