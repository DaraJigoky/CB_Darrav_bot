from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, ContentType


censor_pack = ['педик', 'гомогей']


# флаг для лс 1
async def utils_send_message(message: Message, chat_id, char_name, char_surname, flag='', command_args=''):
    if flag == '':
        addition_text = ''
        if message.content_type == ContentType.TEXT:
            # смайлики кстати тож считаются текстом
            # Список цензурных слов пока что в utils.py сверху
            if censor_check(message.text, censor_pack):
                await message.bot.send_message(chat_id=chat_id, text=f'{addition_text}{char_name} {char_surname}:\n{message.text}')
            else:
                await message.answer('Ребят давайте без плохих слов')
        if message.content_type == ContentType.STICKER:
            await message.bot.send_message(chat_id=chat_id, text=f'{addition_text}{char_name} {char_surname}:')
            await message.bot.send_sticker(chat_id=chat_id, sticker=message.sticker.file_id)
        if message.content_type == ContentType.PHOTO:
            await message.bot.send_message(chat_id=chat_id, text=f'{addition_text}{char_name} {char_surname}:')
            await message.bot.send_photo(chat_id=chat_id, photo=message.photo[-1].file_id)
        if message.content_type == ContentType.ANIMATION:
            await message.bot.send_message(chat_id=chat_id, text=f'{addition_text}{char_name} {char_surname}:')
            await message.bot.send_animation(chat_id=chat_id, animation=message.animation.file_id)
    if flag == 1:
        addition_text = 'Из тени появился вестник-птица и в вашу руку вложился лист с посланием от:\n'
        if message.content_type == ContentType.TEXT:
            # смайлики кстати тож считаются текстом
            # Список цензурных слов пока что в utils.py сверху
            if censor_check(command_args, censor_pack):
                await message.bot.send_message(chat_id=chat_id, text=f'{addition_text}{char_name} {char_surname}:\n{command_args}')
            else:
                await message.answer('Ребят давайте без плохих слов')       
        #if message.content_type == ContentType.PHOTO:
            #await message.bot.send_message(chat_id=chat_id, text=f'{addition_text}{char_name} {char_surname}:')
            #await message.bot.send_photo(chat_id=chat_id, photo=message.photo[-1].file_id)
        #if message.content_type == ContentType.ANIMATION:
            #await message.bot.send_message(chat_id=chat_id, text=f'{addition_text}{char_name} {char_surname}:')
            #await message.bot.send_animation(chat_id=chat_id, animation=message.animation.file_id)


class PreloadDicts:
    accounts = [
        {'tg_id': '896282019', 'login': '1', 'password': '1'},
        {'tg_id': '1797687467', 'login': '2', 'password': '2'},
    ]
    # Флаги: 1 - все локи, 2 - магазины вещей, 3 - банк, 4 - магазин продуктов, 5 - 18+ локи
    locations = [
        {'name': 'Руины', 'description': 'Приветствуем', 'transport': '2_3_4', 'flag': 1}, #1 ruins
        {'name': 'Озеро', 'description': 'Не утони', 'transport': '1', 'flag': 1}, #2 lake
        {'name': 'Банк', 'description': 'Твои деньги здесь', 'transport': '1_4_5', 'flag': 3}, #3 bank
        {'name': 'Госпиталь', 'description': 'Лечитесь', 'transport': '1_2_3_5_6_7_8_10', 'flag': 1}, #4 hospital
        {'name': 'Рынок', 'description': 'Закупайтесь', 'transport': '3_4_6', 'flag': 2}, #5 market
        {'name': 'Таверна', 'description': 'Нажритесь', 'transport': '5_4_7', 'flag': 4}, #6 tavern
        {'name': 'Тюрьма', 'description': 'Вы наказаны(?)', 'transport': '4_6_8', 'flag': 1}, #7 jail
        {'name': 'Магазин', 'description': 'Закупайтесь', 'transport': '4_7_9_10', 'flag': 2}, #8 shop
        {'name': 'Крыша', 'description': 'Тут красивые звёзды', 'transport': '8_10', 'flag': 1}, #9 roof
        {'name': 'Бордель', 'description': '*битесь', 'transport': '4_8', 'flag': 5}, #10 brothel              
    ]
    
    races = [
        {'name': 'Человек', 'description': 'Человек есть человек, людб'},
        {'name': 'Ангел', 'description': 'Челы с крыльями'},
        {'name': 'Демон', 'description': 'Нелюди с рогами'},
        {'name': 'Кизомэ', 'description': 'Нежить, похожи на лис'},
        {'name': 'Эльф', 'description': 'Чел с длинными ушами'},
        {'name': 'Ламия', 'description': 'Змеюка окояная'},
        {'name': 'Неко', 'description': 'Люди-кошки'},
        {'name': 'Энт', 'description': 'Лешие'},
        {'name': 'Гном', 'description': 'Дварфы, Дворфы'},
        {'name': 'Русалка', 'description': 'ЧДева с хвостом рыбы'},
        {'name': 'Драконид', 'description': 'Родился от дракона и кого-то'},
        {'name': 'Циклоп', 'description': 'Одноглазый чел'},
        {'name': 'Орк', 'description': 'Дубина бить. Хорошо.'},
        {'name': 'Вампир', 'description': 'Кровосися'},
        {'name': 'Сатир', 'description': 'Козлоногий чел'},
        {'name': 'Лич', 'description': 'Давно мёртвый маг'},
        {'name': 'Бес', 'description': 'Черти'},
        {'name': 'Суккуб/Инкуб', 'description': 'Те же демоны, но горячее'},
        {'name': 'Дух', 'description': 'Доброе, мертвое, никого не трогает'},
        {'name': 'Зомби', 'description': 'Нежить кусачая. Мозги-и! А-ргх!'},
        {'name': 'Призрак', 'description': 'Озлобленый, мёртвый'},
        {'name': 'Грибы', 'description': 'Придумать название по лучше'},
        {'name': 'Кенку', 'description': 'Люди-вороны'},
        {'name': 'Кицунэ', 'description': 'Люди-лисы'},
    ]

    characters = [
        {'account': 1, 'inventory': 1, 'first_name': 'Dara', 'last_name': 'Okamu', 'race': 'Демон', 'age': '20', 'location': 1, 'description': 'Darochka', 'game_state': 0},
        {'account': 2, 'inventory': 2, 'first_name': 'Tolik', 'last_name': 'Bebra', 'race': 'Человек', 'age': '20', 'location': 1, 'description': 'Tolichka', 'game_state': 0},
    ]

    inventories = [
        {'char_id': 1, 'items': '1_2_2_1_1_1_4'},
        {'char_id': 2, 'items': '1_2_2_2_3_3_4'},
    ]

    items = [
        {'name': 'Первачок', 'description': 'Это первый начальный предмет'},
        {'name': 'Вторуха', 'description': 'А это второй начальный предмет'},
        {'name': 'Трута', 'description': 'Третий предмет'},
        {'name': 'Алмаз Золота', 'description': 'Самый золотой из алмазов'},
    ]

    shops = [
        {'items': '3_4'},
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
