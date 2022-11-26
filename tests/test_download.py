from page_loader import download
from page_loader.loader import download_image
import requests_mock
import tempfile


# Тестовые данные
url = 'https://ru.hexlet.io/courses'
img1 = 'https://cdn2.hexlet.io/assets/logo_ru-495f05850e0095ea722a2b583565d492719579c02b0ce61d924e4f895fabf781.svg'  # noqa: E501
img2 = 'https://cdn2.hexlet.io/assets/team/you-bc72575a0e6eb39de3e28e54a8df1138beaa57cd5300061ecb5c202773131f9e.jpg'  # noqa: E501
img3 = 'https://cdn2.hexlet.io/assets/at_a_laptop-8c6e59267f91a6bf13bae0e5c0f7e1f36accc440b8d760bca08ab244e2b8bdbf.png'  # noqa: E501
img4 = 'https://cdn2.hexlet.io/assets/flag-en-f0b48c6562bb27879fbd685ece0133271ea043384dd9793843c246f862ac7cc1.svg'  # noqa: E501
img5 = 'https://cdn2.hexlet.io/assets/flag-ru-593864ce87ae202b2c2e9393b2a6cf9384ac9cbb1c70632f4c6eeca34341483e.svg'  # noqa: E501


path_to_expected_html_page = 'tests/fixtures/expected_page.html'
expected_page = open(path_to_expected_html_page).read()

expected_html_files_dir = 'ru-hexlet-io-courses_files/'

path_to_expected_images_names = 'tests/fixtures/expected_images_names.txt'
expected_images_names = open(path_to_expected_images_names)
images_name_list = expected_images_names.read().split(',\n')

path_to_mock_page = 'tests/fixtures/mock_page_content.txt'
mock_text = open(path_to_mock_page).read()


path_to_mock_img1 = 'tests/fixtures/mock_img1_content.svg'
path_to_mock_img2 = 'tests/fixtures/mock_img2_content.jpg'
path_to_mock_img3 = 'tests/fixtures/mock_img3_content.png'
path_to_mock_img4 = 'tests/fixtures/mock_img4_content.svg'
path_to_mock_img5 = 'tests/fixtures/mock_img5_content.svg'
mock_img1 = open(path_to_mock_img1, 'rb').read()
mock_img2 = open(path_to_mock_img2, 'rb').read()
mock_img3 = open(path_to_mock_img3, 'rb').read()
mock_img4 = open(path_to_mock_img4, 'rb').read()
mock_img5 = open(path_to_mock_img5, 'rb').read()


def test_download():

    with requests_mock.Mocker() as m:
        m.get(url, text=mock_text)
        m.get(img1, content=mock_img1)
        m.get(img2, content=mock_img2)
        m.get(img3, content=mock_img3)
        m.get(img4, content=mock_img4)
        m.get(img5, content=mock_img5)
        with tempfile.TemporaryDirectory() as temp_dir:
            result_page_path = download(url, temp_dir)
            # result_html_files_path = os.path.join(
            #     temp_dir, expected_html_files_dir)
            result_page = open(result_page_path).read()
            assert result_page == expected_page
            # assert os.listdir(result_html_files_path) == images_name_list


def test_download_to_not_exist_dir():
    not_exist_dir = 'not_exist_dir/'
    assert download(url, not_exist_dir) == 'Указанная директория не найдена.'


def test_download_image():
    with requests_mock.Mocker() as m:
        m.get(img1, content=mock_img1)
        with tempfile.TemporaryDirectory() as temp_dir:
            path_to_image = download_image(img1, temp_dir)
            result_image = open(path_to_image, 'rb').read()
            assert result_image == mock_img1
