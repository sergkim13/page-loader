import os
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse


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
    page_name = generate_name(url, ext='.html')
    page_path = generate_path(dir, page_name)
    page_with_saved_files = get_page_with_saved_files(url, dir, page)
    with open(page_path, 'w') as file:
        file.write(page_with_saved_files)
    return page_path


def get_page_with_saved_files(url, dir, page):

    files_folder_name = generate_name(url, ext='_files')
    files_path = make_files_path(dir, files_folder_name)
    soup = BeautifulSoup(page.text, 'html.parser')

    images = soup.find_all('img')
    page_domain = get_domain(url)
    for image in images:
        image_url = normalize(image['src'], url)
        image_domain = get_domain(image_url)
        if image_domain == page_domain:
            image_relative_path = download_image(
                image_url, files_folder_name, files_path)
            image['src'] = image_relative_path

    return soup.prettify()


def make_files_path(dir, files_folder_name):
    files_path = generate_path(dir, files_folder_name)
    os.mkdir(files_path)
    return files_path


def download_image(image_url, files_folder_name, files_path):
    image = requests.get(image_url)
    image_name = generate_name(image_url)
    image_relative_path = generate_path(files_folder_name, image_name)
    image_absolute_path = generate_path(files_path, image_name)
    with open(image_absolute_path, 'wb') as f:
        f.write(image.content)
    return image_relative_path


def normalize(img_url, page_url):
    img_url_parts = list(urlparse(img_url))
    img_url_netloc = img_url_parts[1]
    if not img_url_netloc:
        page_url_parts = urlparse(page_url)
        img_url_parts[0] = page_url_parts.scheme
        img_url_parts[1] = page_url_parts.netloc
        img_url = urlunparse(img_url_parts)
    return img_url


def get_domain(url):
    netloc = urlparse(url).netloc
    return netloc


def generate_name(url, ext=''):
    url, extension = os.path.splitext(url)
    if ext != '':
        extension = ext
    url_parts = list(urlparse(url))
    url_parts[0] = ''
    url = urlunparse(url_parts)
    if url.startswith('//'):
        url = url[2:]
    name = re.sub(r'[\W_]', '-', url) + extension
    return name


def generate_path(dir, file):
    return os.path.join(dir, file)
