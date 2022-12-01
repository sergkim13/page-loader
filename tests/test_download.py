from page_loader import download
import requests_mock
import tempfile
import os


# Тестовые данные
url = 'https://ru.hexlet.io/courses'
img1 = 'https://ru.hexlet.io/assets/logo_ru-495f05850e0095ea722a2b583565d492719579c02b0ce61d924e4f895fabf781.svg'      # noqa: E501
img2 = 'https://ru.hexlet.io/assets/team/you-bc72575a0e6eb39de3e28e54a8df1138beaa57cd5300061ecb5c202773131f9e.jpg'     # noqa: E501
img3 = 'https://ru.hexlet.io/assets/at_a_laptop-8c6e59267f91a6bf13bae0e5c0f7e1f36accc440b8d760bca08ab244e2b8bdbf.png'  # noqa: E501


path_to_expected_html_page = 'tests/fixtures/expected_page.html'
expected_page = open(path_to_expected_html_page).read()

expected_html_files_dir = 'ru-hexlet-io-courses_files/'

path_to_expected_images_names = 'tests/fixtures/img_mocks/expected_images_names.txt'                                   # noqa: E501
expected_images_names = open(path_to_expected_images_names)
images_name_list = set(expected_images_names.read().split(',\n'))

path_to_mock_page = 'tests/fixtures/mock_page_content.txt'
mock_text = open(path_to_mock_page).read()


path_to_mock_img1 = 'tests/fixtures/img_mocks/mock_img1_content.svg'
path_to_mock_img2 = 'tests/fixtures/img_mocks/mock_img2_content.jpg'
path_to_mock_img3 = 'tests/fixtures/img_mocks/mock_img3_content.png'
mock_img1 = open(path_to_mock_img1, 'rb').read()
mock_img2 = open(path_to_mock_img2, 'rb').read()
mock_img3 = open(path_to_mock_img3, 'rb').read()



def test_download():

    with requests_mock.Mocker() as m:
        m.get(url, text=mock_text)
        m.get(img1, content=mock_img1)
        m.get(img2, content=mock_img2)
        m.get(img3, content=mock_img3)
        with tempfile.TemporaryDirectory() as temp_dir:
            result_page_path = download(url, temp_dir)
            result_html_files_path = os.path.join(
                temp_dir, expected_html_files_dir)
            result_page = open(result_page_path).read()
            assert result_page == expected_page
            assert set(os.listdir(result_html_files_path)) == images_name_list


def test_download_to_not_exist_dir():
    not_exist_dir = 'not_exist_dir/'
    assert download(url, not_exist_dir) == 'Указанная директория не найдена.'
