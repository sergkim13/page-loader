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
    saved_page_path = get_saved_page_path(url, dir) 
    saved_images_path = get_saved_images_path(url, dir)
    page_with_saved_images = rebuild_page_with_saved_images(page, url, saved_images_path)
    with open(saved_page_path, 'w') as file:
        file.write(page_with_saved_images)
    return saved_page_path


def rebuild_page_with_saved_images(page, url, saved_images_path):
    soup = BeautifulSoup(page.text, 'html.parser')
    page_domain = get_domain(url)
    images = soup.find_all('img')
    for image in images:
        image_url = normalize(image['src'], url)
        image_domain = get_domain(image_url)
        if page_domain in image_domain:
            image_local_path = download_image(image_url, saved_images_path)
            image['src'] = image_local_path
    return soup.prettify()


def normalize(img_url, page_url):
    img_url_domain = get_domain(img_url)
    
    if not img_url_domain:
        page_url_chunks = urlparse(page_url)
        scheme = page_url_chunks.scheme
        netloc = page_url_chunks.netloc
        img_url = f'{scheme}//{netloc}/{img_url}'
    
    return img_url


def get_saved_page_path(url, dir):
    page_name = generate_name(url) + '.html'
    saved_page_path = os.path.join(dir, page_name)
    return saved_page_path


def get_saved_images_path(url, dir):
    images_folder_name = generate_name(url) + '_files'
    saved_images_path = os.path.join(dir, images_folder_name)
    os.mkdir(saved_images_path)
    return saved_images_path


def get_image_path(url, dir):
    image_name = generate_name(url)
    image_path = os.path.join(dir, image_name)
    return image_path


def download_image(url, saved_images_path):
    image = requests.get(url)
    image_path = get_image_path(url, saved_images_path)
    with open(image_path, 'wb') as f:
        f.write(image.content)
    return image_path


def get_domain(url):
    netloc = urlparse(url).netloc
    if netloc:
        netloc_chunks = netloc.split('.')
        domain_1lvl = netloc_chunks[-1]
        domain_2lvl = netloc_chunks[-2]
        domain = f'{domain_2lvl}.{domain_1lvl}'
    else:
        domain = ''
    return domain


def generate_name(url):
    img_ext = {'.png', '.jpg', '.svg'}
    url, ext = os.path.splitext(url)
    if ext not in img_ext:
        ext = ''
    if urlparse(url).scheme:
        _, url = url.split('//')
    name = re.sub(r'[\W_]', '-', url) + ext
    return name

# download('https://ru.hexlet.io/courses')