import requests_mock
import tempfile
import pytest
import os
from page_loader import download


# Тестовые данные
url = 'https://yandex.ru'
mock_text = 'mock_text'
expected_page_name = 'yandex_ru.html'
expected_html_files_dir = 'yandex_ru_files/'


def test_download_to_not_exist_dir():
    not_exist_dir = 'not_exist_dir/'
    with pytest.raises(FileNotFoundError):
        download(url, not_exist_dir)


def test_download_permission():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chmod(temp_dir, 0o400)
        with pytest.raises(PermissionError):
            download(url, temp_dir)


def test_download_file_exist():

    with requests_mock.Mocker() as m:
        m.get(url, text=mock_text)

        with tempfile.TemporaryDirectory() as temp_dir:
            exist_file_path = os.path.join(temp_dir, expected_page_name)
            with open(exist_file_path, 'w') as exist_file:
                exist_file.write('some content')
            
            with pytest.raises(FileExistsError):
                download(url, temp_dir)
