import os
import requests
import re


def download(url, dir=os.getcwd()):
    page = requests.get(url)
    path_to_file = os.path.join(dir, get_file_name(url))
    with open(path_to_file, 'w') as file:
        file.write(page.text)
    return path_to_file


def get_file_name(url):
    _, address = url.split('//')
    file_ext = '.html'
    name = re.sub(r'\W', '-', address) + file_ext
    return name
