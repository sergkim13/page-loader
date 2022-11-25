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

    soup = BeautifulSoup(page.text, 'html.parser')
    page_with_saved_images = rebuild_page_with_saved_images(soup, url, saved_images_path)
        
    with open(saved_page_path, 'w') as file:
        file.write(page_with_saved_images)
    return saved_page_path


def rebuild_page_with_saved_images(soup, url, saved_images_path):
    domain = get_domain(url)
    image_links = get_images_in_domain(soup, domain)
    saved_image_links = list(map(lambda link: download_image(link, saved_images_path), image_links))
    image_links_iter = iter(saved_image_links)
    for img in image_links:
        img['src'] = next(image_links_iter)
    return soup.prettify()


def get_images_in_domain(soup, domain):
    return soup.find_all('img', src=re.compile(domain))  # TODO скачивать только jpg и png


## Объединить эти три функции:
def get_saved_page_path(url, dir):
    page_name = generate_name(url) + '.html'
    return os.path.join(dir, page_name)


def get_saved_images_path(url, dir):
    images_folder_name = generate_name(url) + '_files'
    return os.path.join(dir, images_folder_name)


def get_image_path(url, dir):
    image_name = generate_name(url)
    return os.path.join(dir, image_name)


def download_image(url, saved_images_path):
    image = requests.get(url)   # TODO сгенерировать имя изображения, сохранять функцию, и вернуть полный путь до изображения
    image_path = get_image_path(url, saved_images_path)
    with open(image_path, 'wb') as f:
        f.write(image.content)
    return image_path
 

def get_domain(url):
    netloc = urlparse(url).netloc
    netloc_chunks = netloc.split('.')
    domain = f'{netloc_chunks[-2]}.{netloc_chunks[-1]}'
    return domain


def generate_name(url):
    img_ext = {'png', 'jpg'}
    url, ext = os.path.splitext(url)
    if ext not in img_ext:
        ext = ''
    if urlparse(url).scheme:
        _, url = url.split('//')
    name = re.sub(r'[\W_]', '-', url) + ext
    return name
