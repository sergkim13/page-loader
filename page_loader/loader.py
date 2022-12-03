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

    url = normalize_page_url(url)
    page = requests.get(url)
    page_name = generate_name(url, ext='.html')
    page_path = os.path.abspath(generate_path(dir, page_name))
    page_with_saved_files = get_page_with_saved_files(url, dir, page)
    with open(page_path, 'w') as file:
        file.write(page_with_saved_files)
    print(f'Page was downloaded as {page_path}')
    return page_path


def get_page_with_saved_files(url, dir, page):
    files_folder_name = generate_name(url, ext='_files')
    files_path = make_files_path(dir, files_folder_name)
    soup = BeautifulSoup(page.text, 'html.parser')

    images = soup.find_all('img')
    download_local_files(
        url, images, files_folder_name, files_path)

    links = soup.find_all('link')
    download_local_files(
        url, links, files_folder_name, files_path, attr='href')

    scripts = soup.find_all(scripts_with_src)
    download_local_files(
        url, scripts, files_folder_name, files_path)

    return soup.prettify()


def download_local_files(url, tags, files_folder_name, files_path, attr='src'):
    page_domain = get_domain(url)
    for tag in tags:
        tag_url = normalize_file_url(tag[attr], url)
        tag_url_domain = get_domain(tag_url)
        if tag_url_domain == page_domain:
            file_relative_path = download_file(
                tag_url, files_folder_name, files_path)
            tag[attr] = file_relative_path


def download_file(file_url, files_folder_name, files_path):
    images_ext = ('.JPEG', '.GIF', '.PNG', '.SVG')
    file = requests.get(file_url)
    file_name = generate_name(file_url)
    file_relative_path = generate_path(files_folder_name, file_name)
    file_absolute_path = generate_path(files_path, file_name)

    if file_url.upper().endswith(images_ext):
        with open(file_absolute_path, 'wb') as f:
            f.write(file.content)
        return file_relative_path

    else:
        with open(file_absolute_path, 'w') as f:
            f.write(file.text)
        return file_relative_path


def make_files_path(dir, files_folder_name):
    files_path = generate_path(dir, files_folder_name)
    os.mkdir(files_path)
    return files_path


def scripts_with_src(tag):
    return tag.name == 'script' and tag.has_attr('src')


def normalize_page_url(url):
    url_parts = list(urlparse(url))
    scheme = url_parts[0]
    if not scheme:
        url = 'https://' + url
    return url


def normalize_file_url(file_url, page_url):
    file_url_parts = list(urlparse(file_url))
    file_url_netloc = file_url_parts[1]
    if not file_url_netloc:
        page_url_parts = urlparse(page_url)
        file_url_parts[0] = page_url_parts.scheme
        file_url_parts[1] = page_url_parts.netloc
        file_url = urlunparse(file_url_parts)
    return file_url


def get_domain(url):
    netloc = urlparse(url).netloc
    return netloc


def generate_name(url, ext=''):
    if url_has_path(url):
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


def url_has_path(url):
    return True if urlparse(url).path else False


def generate_path(dir, file):
    return os.path.join(dir, file)
