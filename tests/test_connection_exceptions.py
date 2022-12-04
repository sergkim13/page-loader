from page_loader import download
import requests_mock
import tempfile
import pytest


# Тестовые данные
url401 = 'https://vk.com'
url403 = 'https://rutor.info'
url404 = 'https://google.com'
url500 = 'https://ya.ru'
url501 = 'https://rutracker.org'


def test_exception_ConnectionError():
    with requests_mock.Mocker() as m:
        # m.get(url401, status_code=401)
        # m.get(url403, status_code=403)
        # m.get(url404, status_code=404)
        # m.get(url500, status_code=500)
        m.get(url501, status_code=500)

        with tempfile.TemporaryDirectory() as temp_dir:

            with pytest.raises(ConnectionError):
                # download(url401, temp_dir)
                # download(url403, temp_dir)
                # download(url404, temp_dir)
                # download(url500, temp_dir)
                download(url501, temp_dir)
