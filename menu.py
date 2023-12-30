import db


MENU = "Список команд:\n" \
       "1 - Создание объекта базы данных\n" \
       "2 - Создание в базе данных таблицы с заданным именем и набором полей\n" \
       "3 - Добавление одной записи в выбранную таблицу базы данных\n" \
       "4 - Добавление нескольких записей в выбранную таблицу базы данных\n" \
       "5 - Вывод на экран всех записей выбранной таблицы базы данных\n" \
       "6 - Выход\n"
INPUT = "Введите команду: "


def do_menu():
    command = 0
    db_name = "PhoneDirectory_DataBase1.db"
    db_methods = db.DatabaseMethods(db_name)
    while command != 6:
        print(MENU)
        print(INPUT, end='')
        command = int(input())
        command_handling(db_methods, command)


def command_handling(db_methods, command):
    if command == 1:
        db_methods.create_db()
    if command == 2:
        db_methods.create_table()
    if command == 3:
        db_methods.insert_one()
    if command == 4:
        db_methods.insert_many()
    if command == 5:
        db_methods.print_table()
