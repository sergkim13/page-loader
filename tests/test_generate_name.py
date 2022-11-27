from page_loader.loader import generate_name


url = 'https://ru.hexlet.io/courses'
url_with_ext = 'https://ru.hexlet.io/courses.index'
img_url = 'assets/team/you-bc72575a0e6eb39de3e28e54a8df1138beaa57cd5300061ecb5c202773131f9e.jpg'                                  # noqa: E501
img_domain_url = 'https://cdn2.hexlet.io/assets/team/you-bc72575a0e6eb39de3e28e54a8df1138beaa57cd5300061ecb5c202773131f9e.jpg'    # noqa: E501

expected_page_name = 'ru-hexlet-io-courses.html'
expected_files_folder_name = 'ru-hexlet-io-courses_files'
expected_img_name = 'assets-team-you-bc72575a0e6eb39de3e28e54a8df1138beaa57cd5300061ecb5c202773131f9e.jpg'                        # noqa: E501
expected_img_domain_name = 'cdn2-hexlet-io-assets-team-you-bc72575a0e6eb39de3e28e54a8df1138beaa57cd5300061ecb5c202773131f9e.jpg'  # noqa: E501


def test_generate_page_name():
    result = generate_name(url, ext='.html')
    assert result == expected_page_name


def test_generate_files_folder_name():
    result = generate_name(url, ext='_files')
    assert result == expected_files_folder_name


def test_generate_img_name():
    result = generate_name(img_url)
    assert result == expected_img_name


def test_generate_name_with_ext():
    result = generate_name(url, ext='.html')
    assert result == expected_page_name


def test_genereate_name_img_domain():
    result = generate_name(img_domain_url)
    assert result == expected_img_domain_name
