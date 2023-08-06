"""Программа-сервер"""
import argparse
import configparser
import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from pack_server.server import MessageProcessor
from pack_server.server.server.main_window import MainWindow
from pack_server.server.server.database import ServerStorage
from pack_server.server.common import log

# Инициализация логгера
SERVER_LOGGER = logging.getLogger('server')

# Флаг что был подключён новый пользователь, нужен чтобы не мучать БД
# постоянными запросами на обновление
# new_connection = False
# conflag_lock = threading.Lock()  # приостановка потока


@log
def arg_parser(default_port, default_address):
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    parser.add_argument('-a', default=default_address, nargs='?')
    parser.add_argument('--no_gui', action='store_true')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    gui_flag = namespace.no_gui
    return listen_address, listen_port, gui_flag


@log
def config_load():
    """
    Функция загрузки файла конфигурации ini
    :return: словарь конфигурации сервера из файла или по умолчанию
    """
    config = configparser.ConfigParser()
    dir_path = os.getcwd()
    config.read(f"{dir_path}/{'server.ini'}")
    # Если конфиг файл загружен правильно, запускаемся, иначе конфиг по умолчанию.
    if 'SETTINGS' in config:
        SERVER_LOGGER.info('Конфигурация загружена из файла ')
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'Default_port', str(DEFAULT_PORT))
        config.set('SETTINGS', 'Listen_Address', '')
        config.set('SETTINGS', 'Database_path', '')
        config.set('SETTINGS', 'Database_file', 'server_database.db3')
        SERVER_LOGGER.info('Конфигурация по умолчанию')
        return config


@log
def main():
    """Основная функция"""
    # Загрузка файла конфигурации сервера
    config = config_load()
    # Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    listen_address, listen_port, gui_flag = arg_parser(
        config['SETTINGS']['Default_port'], config['SETTINGS']['Listen_Address'])

    # Инициализация базы данных
    database = ServerStorage(
        os.path.join(
            config['SETTINGS']['Database_path'],
            config['SETTINGS']['Database_file']))
    SERVER_LOGGER.info('Инициализирована БД сервера')

    # Создание экземпляра класса - сервера и его запуск:
    server = MessageProcessor(listen_address, listen_port, database)
    server.daemon = True
    server.start()
    SERVER_LOGGER.info('Создан и запущен экземпляр класса - сервера')

    # Если указан параметр без GUI то запускаем простенький обработчик консольного ввода
    if gui_flag:
        while True:
            command = input('Введите exit для завершения работы сервера.')
            if command == 'exit':
                # Если выход, то завршаем основной цикл сервера.
                server.running = False
                server.join()  # ждет пока поток закроется
                break

    # Если не указан запуск без GUI, то запускаем GUI:
    else:
        # Создаём графическое окуружение для сервера:
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(database, server, config)
        # Запускаем GUI
        server_app.exec_()
        # По закрытию окон останавливаем обработчик сообщений
        server.running = False


if __name__ == '__main__':
    main()
