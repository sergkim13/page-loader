from bs4 import BeautifulSoup
from pprint import pprint

def scripts_with_src(tag):
    return tag.name == 'script' and tag.has_attr('src')

with open('tests/fixtures/mock_page_content.txt') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')
    links = soup.find_all('link')
    scripts = soup.find_all(scripts_with_src)
    # with open('tests/fixtures/link_mocks/links.txt', 'w') as fo:
    #     fo.write(str(links))
    with open('tests/fixtures/script_mocks/scripts.txt', 'w') as fo:
        fo.write(str(scripts))
    # pprint(links)
    # pprint(scripts)
    # pprint(len(scripts))