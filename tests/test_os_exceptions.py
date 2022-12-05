import requests_mock
import tempfile
import pytest
import os
from page_loader import download


# Тестовые данные
url = 'https://yandex.ru'
mock_text = '<img src="assets/mock.png"/>'
expected_page_name = 'yandex-ru.html'
expected_html_files_dir = 'yandex-ru_files'


def test_download_to_not_exist_dir():
    not_exist_dir = 'not_exist_dir/'
    with requests_mock.Mocker() as m:
        m.get(url, text=mock_text)
        with pytest.raises(FileNotFoundError):
            download(url, not_exist_dir)


def test_download_permission():
    with requests_mock.Mocker() as m:
        m.get(url, text=mock_text)

        with tempfile.TemporaryDirectory() as temp_dir:
            os.chmod(temp_dir, 0o400)
            with pytest.raises(PermissionError):
                download(url, temp_dir)


def test_download_page_file_exist():

    with requests_mock.Mocker() as m:
        m.get(url, text=mock_text)

        with tempfile.TemporaryDirectory() as temp_dir:
            exist_file_path = os.path.join(temp_dir, expected_page_name)
            open(exist_file_path, 'w')

            with pytest.raises(FileExistsError):
                download(url, temp_dir)


def test_download_files_dir_exist():

    with requests_mock.Mocker() as m:
        m.get(url, text=mock_text)

        with tempfile.TemporaryDirectory() as temp_dir:
            exist_files_path = os.path.join(temp_dir, expected_html_files_dir)
            os.mkdir(exist_files_path)

            with pytest.raises(FileExistsError):
                download(url, temp_dir)
