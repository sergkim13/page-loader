from bs4 import BeautifulSoup
from page_loader.tools import (
    generate_name, generate_path, get_domain, normalize_url)


def parse_html(url, dir, page):
    soup = BeautifulSoup(page.text, 'html.parser')
    tags = get_local_tags(soup, url)
    assets = get_assets(tags, dir)
    return soup.prettify(), assets


def get_assets(tags, dir):
    assets = []
    for tag in tags:
        if tag.has_attr('src'):
            attr = 'src'
        else:
            attr = 'href'
        tag_url = tag[attr]
        name = generate_name(tag_url)
        path = generate_path(dir, name)
        asset = (tag_url, name)
        assets.append(asset)
        tag[attr] = path
    return assets


def get_local_tags(soup, url):
    page_domain = get_domain(url)

    def imgs_links_scripts_in_domain(tag):
        return (
            tag.name == 'img'
            and get_domain(normalize_url(tag['src'], url)) == page_domain

            or tag.name == 'link'
            and get_domain(normalize_url(tag['href'], url)) == page_domain

            or tag.name == 'script' and tag.has_attr('src')
            and get_domain(normalize_url(tag['src'], url)) == page_domain)

    tags = soup.find_all(imgs_links_scripts_in_domain)
    for tag in tags:
        if tag.has_attr('src'):
            attr = 'src'
        else:
            attr = 'href'
        tag[attr] = normalize_url(tag[attr], url)
    return tags
