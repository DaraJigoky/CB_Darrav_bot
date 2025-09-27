from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, ContentType

class PreloadDicts:
    accounts = [
        {'tg_id': '896282019', 'flag_admin': 1, 'flag_vld': 1},
    ]
   
    characters = [
        {'account': 1, 'inventory': 1, 'name': 'Dara', 'game_state': 0},
    ]

    inventories = [
        {'char_id': 1, 'money': '1000'},
    ]

    donat_shop = [
        {'items': '100 darks', 'price': '100'},
    ]
    

############ Тестовый стенд получения из файлов по категории её содержимое ######################
# Для работы нужно рядом с исполнительным файлом создать текстовик test_file.txt (или другое название, но нужно будет его поменять в коде) с примерным текстом, представленным в самом низу
# Пробелы не помешают нам, их можно делать
# Для проверки рекомендую отдельно создать файл для удобства там где это будет удобнее, но при желании можно и тут проверять


from itertools import islice


# Поиск индекса позиции начала искомой категории объектов
def find_line_index(file_path: str, line_to_find: str) -> int:  
    with open(file_path, 'r', encoding='utf-8') as file:
        for index, line in enumerate(file):
            if line_to_find in line:              
                return index


# По индексу объектов перебираем всё содержимое до начала следующей категории и возвращаем список содержимого
def find_lines_of_category(file_path: str, index_to_start: int) -> list[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        index_to_start += 1
        output_lines = []
        lines = islice(file, index_to_start, None)
        for line in lines:
            if line.startswith('#'):
                break
            else:
                if not line.isspace():
                    output_lines.append(line.rstrip('\n'))
        
        return output_lines


# Объединяем две функции в одну и по итогу мы по названию категории получаем списком её содержимое
def get_lines_in_category(file_path: str, line_to_find: str) -> list[str]:
    """
    Аргументы:
        file_path (str): Путь до нужного файла, например: 'text.txt' или 'app/utils/text.txt'
        line_to_find (str): Название категории по которому будет произведён поиск. В данном случае категории начинаются со знака #

    Возвращает:
        list[str]: Список строк из категории файла
    """
    index = find_line_index(file_path, line_to_find)
    output_lines = find_lines_of_category(file_path, index)
    return output_lines


# Сам тестовый стенд. Вписываем нужное название категории из файла и получаем его содержимое
line_to_find = '# Список имён'
file_path = 'app/utils/test_text.txt'
output_lines = get_lines_in_category(file_path, line_to_find)
print(output_lines)


# Пример рабочего текстовика откуда мы достанем содержимое категории
# Кавычки не пишем
"""
# Список имён

Вася
Петя
Жопик

# Список локаций

Гора
Землянка
Пещера

# Список оружий

Лук
Меч
Шит
"""
# Кавычки не пишем


def censor_check(text: str, censor: list[str]):
    words = text.split()
    for word in words:
        if word.lower() in censor:
            return False
    return True
