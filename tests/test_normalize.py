from page_loader.loader import normalize_page_url, normalize_file_url


url = 'https://hexlet.io/courses/'
url_without_scheme = 'hexlet.io/courses/'
img_url1 = 'assets/team/you-bc72575a0e6eb39de3e28e54a8df1138beaa57cd5300061ecb5c202773131f9e.jpg'                                    # noqa: E501
img_url2 = 'https://www.hexlet.io/assets/team/you-bc72575a0e6eb39de3e28e54a8df1138beaa57cd5300061ecb5c202773131f9e.jpg'              # noqa: E501
expected_normalized_img1 = 'https://hexlet.io/assets/team/you-bc72575a0e6eb39de3e28e54a8df1138beaa57cd5300061ecb5c202773131f9e.jpg'  # noqa: E501
expected_normalized_img2 = img_url2


def test_normalize_url():
    result = normalize_page_url(url_without_scheme)
    assert result == url


def test_normalize():
    result1 = normalize_file_url(img_url1, url)
    result2 = normalize_file_url(img_url2, url)
    assert result1 == expected_normalized_img1
    assert result2 == expected_normalized_img2
