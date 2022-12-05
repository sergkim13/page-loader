from urllib.parse import urlparse, urlunparse
import os
import re


def normalize_url(url, reference_url=''):
    if not reference_url:
        url = add_scheme(url)
    else:
        reference_url = add_scheme(reference_url)
        url_parts = list(urlparse(url))
        print(url_parts[0])
        print(url_parts[1])
        url_netloc = url_parts[1]
        if not url_netloc:
            reference_url_parts = urlparse(reference_url)
            url_parts[0] = reference_url_parts.scheme
            url_parts[1] = reference_url_parts.netloc
            url = urlunparse(url_parts)
    return url


def add_scheme(url):
    url_parts = list(urlparse(url))
    scheme = url_parts[0]
    if not scheme:
        url = 'https://' + url
    return url


def get_domain(url):
    netloc = urlparse(url).netloc
    return netloc


def generate_name(url, ext=''):
    if url_has_path(url):
        url, extension = os.path.splitext(url)
        if not extension:
            extension = '.html'

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
