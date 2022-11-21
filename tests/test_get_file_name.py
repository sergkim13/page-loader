from page_loader.loader import get_file_name


url = 'https://ru.hexlet.io/courses/index.html'
expected_file_name = 'ru-hexlet-io-courses-index.html'


def test_get_name():
    result = get_file_name(url)
    assert result == expected_file_name