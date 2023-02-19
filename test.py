import datetime
import argparse
import requests

# HOST = '0.0.0.0'
HOST = '127.0.0.1'
PORT = 5000
parser = argparse.ArgumentParser(  # объект обрабатывающий аргументы(как в функции)
    description="convert integers to decimal system")
parser.add_argument('--clear', default='0', type=str, help='need to delete all data?(yes(1)/no(0))')


def clear_db(data):
    url = f'http://{HOST}:{PORT}/api/clear'
    response = requests.post(url, json=data)
    # print(response, response.json())


"""Тест соединения"""


def test_connection():
    print('Внимание, Тестирование запустит очистку базы данных')
    ans = input('Продолжить?(y/n)')
    assert ans == 'y'
    test_url = f'http://{HOST}:{PORT}/api/test'
    response = requests.get(test_url)
    # print('Something went wrong: Connection Error')
    # print('Try to rerun service')
    if response:
        print(response.json())
    else:
        print(response)
    clear_db({'code': 'zhern0206eskiy'})
