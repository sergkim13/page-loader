import argparse
import os


def get_args():
    page_loader = argparse.ArgumentParser(
        description='Downloads page and saves content to file in set dir.')
    page_loader.add_argument('url')
    page_loader.add_argument('-o', '--output', help='set directory',
                             default=os.getcwd())
    args = page_loader.parse_args()
    return args
