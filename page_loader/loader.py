import os
import requests
import re


def download(url, dir=os.getcwd()):
    '''
    Функция скачивает страницу и сохраняет ее содержимое
    в файл в указанной директории (по умолчанию - текущая директория).
    Имя файла генерируется по принципу:
    1) Берется адрес без схемы и расширения, если оно есть.
    2) Все символы, кроме букв и цифр, заменяются на дефис -.
    3) В конце ставится .html.
    '''
    if not os.path.exists(dir):
        return 'Указанная директория не найдена.'
        
    page = requests.get(url)
    path_to_file = os.path.join(dir, get_file_name(url))
    with open(path_to_file, 'w') as file:
        file.write(page.text)
    return path_to_file


def get_file_name(url):
    url, _ = os.path.splitext(url)
    _, address = url.split('//')
    name = re.sub(r'\W', '-', address) + '.html'
    return name
