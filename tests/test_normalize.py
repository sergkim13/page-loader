from page_loader.loader import normalize
from urllib.parse import urlparse

url = 'https://hexlet.io/courses/'
img_url1 = 'assets/team/you-bc72575a0e6eb39de3e28e54a8df1138beaa57cd5300061ecb5c202773131f9e.jpg'
img_url2 = 'https://www.hexlet.io/assets/team/you-bc72575a0e6eb39de3e28e54a8df1138beaa57cd5300061ecb5c202773131f9e.jpg'
expected_normalized_img1 = 'https://hexlet.io/assets/team/you-bc72575a0e6eb39de3e28e54a8df1138beaa57cd5300061ecb5c202773131f9e.jpg'
expected_normalized_img2 = img_url2


def test_normalize():
    result1 = normalize(img_url1, url)
    result2 = normalize(img_url2, url)
    assert result1 == expected_normalized_img1
    assert result2 == expected_normalized_img2
