import os
import re


def download(url, dir=os.getcwd()):
    pass


def get_file_name(url):
    _, address = url.split('//')
    file_ext = '.html'
    name = re.sub(r'\W', '-', address) + file_ext
    return name
