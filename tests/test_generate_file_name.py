from page_loader.loader import generate_page_file_name


url = 'https://ru.hexlet.io/courses/index.html'
expected_file_name = 'ru-hexlet-io-courses-index.html'


def test_generate_file_name():
    result = generate_page_file_name(url)
    assert result == expected_file_name