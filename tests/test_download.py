from page_loader import download
import requests_mock
import tempfile
import os


# Тестовые данные
url = 'https://ru.hexlet.io/courses'

path_to_expected_html_page = 'tests/fixtures/expected_page.html'
expected_page = open(path_to_expected_html_page).read()

expected_html_files_dir = 'ru-hexlet-io-courses_files'

path_to_mock_page = 'tests/fixtures/mock_page_content.txt'
mock_text = open(path_to_mock_page).read()

path_to_expected_images_names = 'tests/fixtures/expected_images_names.txt'
expected_images_names = open(path_to_expected_images_names)
images_name_list = expected_images_names.read().split(',\n')


def test_download():

    with requests_mock.Mocker() as m:
        m.get(url, text=mock_text)
        with tempfile.TemporaryDirectory() as temp_dir:
            result_page_path = download(url, temp_dir)
            result_html_files_path = os.path.join(
                temp_dir, expected_html_files_dir)
            result_page = open(result_page_path).read()
            
            assert result_page == expected_page
            assert os.listdir(result_html_files_path) == images_name_list


def test_download_to_not_exist_dir():
    not_exist_dir = 'not_exist_dir/'
    assert download(url, not_exist_dir) == 'Указанная директория не найдена.'
