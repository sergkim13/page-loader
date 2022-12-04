from page_loader import download
import requests_mock
import tempfile
import os


# Тестовые данные
url = 'https://ru.hexlet.io/courses'
img1 = 'https://ru.hexlet.io/assets/logo_ru-495f05850e0095ea722a2b583565d492719579c02b0ce61d924e4f895fabf781.svg'            # noqa: E501
img2 = 'https://ru.hexlet.io/assets/team/you-bc72575a0e6eb39de3e28e54a8df1138beaa57cd5300061ecb5c202773131f9e.jpg'           # noqa: E501
img3 = 'https://ru.hexlet.io/assets/at_a_laptop-8c6e59267f91a6bf13bae0e5c0f7e1f36accc440b8d760bca08ab244e2b8bdbf.png'        # noqa: E501
link1 = 'https://ru.hexlet.io/course'
link2 = 'https://ru.hexlet.io/assets/hexlet_logo_wide-56fe12bf29287c1ac237ef1e5fa70e861e99a954af1f49504f654ae4990fa42b.png'  # noqa: E501
link3 = 'https://ru.hexlet.io/assets/application-8dcc80087a1e4a2cb78752144707fc8b1bd5dede573dfe6174d69fcdf88eb50b.css'       # noqa: E501
script1 = 'https://ru.hexlet.io/assets/sprockets-423c98b6a28c3fab45c96e660879310c4f39c8694f8c4763628f45148bb06d4d.js'        # noqa: E501
script2 = 'https://ru.hexlet.io/assets/bf_promo_banner-c973c1c9fec9bc51fd65442de9aa21e4ab32738bda309c63fdb4b1baf76960e6.js'  # noqa: E501
script3 = 'https://ru.hexlet.io/assets/notifications-3084db50a6641d548dfcf6e0e325750522d40958c5c9625b4acf1222e599ee36.js'    # noqa: E501

# Ожидаемая страница
path_to_expected_html_page = 'tests/fixtures/expected_page.html'
expected_page = open(path_to_expected_html_page).read()

# Ожидаемая директория файлов и имена файлов
expected_html_files_dir = 'ru-hexlet-io-courses_files/'
path_to_expected_files_names = 'tests/fixtures/expected_files_names.txt'                                                     # noqa: E501
expected_files_names_set = set(open(path_to_expected_files_names).read().split(',\n'))                                       # noqa: E501

# Мок страницы
path_to_mock_page = 'tests/fixtures/mock_page_content.txt'
mock_text = open(path_to_mock_page).read()

# Моки изображений
path_to_mock_img1 = 'tests/fixtures/img_mocks/mock_img1_content.svg'
path_to_mock_img2 = 'tests/fixtures/img_mocks/mock_img2_content.jpg'
path_to_mock_img3 = 'tests/fixtures/img_mocks/mock_img3_content.png'
mock_img1 = open(path_to_mock_img1, 'rb').read()
mock_img2 = open(path_to_mock_img2, 'rb').read()
mock_img3 = open(path_to_mock_img3, 'rb').read()

# Моки ссылок
path_to_mock_link1 = 'tests/fixtures/link_mocks/mock_link1_content.html'
path_to_mock_link2 = 'tests/fixtures/link_mocks/mock_link2_content.png'
path_to_mock_link3 = 'tests/fixtures/link_mocks/mock_link3_content.css'
mock_link1 = open(path_to_mock_link1, 'r').read()
mock_link2 = open(path_to_mock_link2, 'rb').read()
mock_link3 = open(path_to_mock_link3, 'r').read()

# Моки скриптов
path_to_mock_script1 = 'tests/fixtures/script_mocks/mock_script1_content.js'
path_to_mock_script2 = 'tests/fixtures/script_mocks/mock_script2_content.js'
path_to_mock_script3 = 'tests/fixtures/script_mocks/mock_script3_content.js'
mock_script1 = open(path_to_mock_script1, 'r').read()
mock_script2 = open(path_to_mock_script2, 'r').read()
mock_script3 = open(path_to_mock_script3, 'r').read()


def test_download():

    with requests_mock.Mocker() as m:

        m.get(url, text=mock_text)
        m.get(img1, content=mock_img1)
        m.get(img2, content=mock_img2)
        m.get(img3, content=mock_img3)
        m.get(link1, text=mock_link1)
        m.get(link2, content=mock_link2)
        m.get(link3, text=mock_link3)
        m.get(script1, text=mock_script1)
        m.get(script2, text=mock_script2)
        m.get(script3, text=mock_script3)

        with tempfile.TemporaryDirectory() as temp_dir:
            result = download(url, temp_dir)
            result_page_path = result[24:-1]
            result_html_files_path = os.path.join(
                temp_dir, expected_html_files_dir)
            result_page = open(result_page_path).read()
            assert result_page == expected_page
            assert set(os.listdir(result_html_files_path)) == expected_files_names_set                                     # noqa: E501
