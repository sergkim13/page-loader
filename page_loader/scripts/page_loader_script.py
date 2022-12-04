#!/usr/bin/env python3
from page_loader import download
from page_loader.args_parser import get_args
import logging

logger = logging.getLogger()


def main():
    args = get_args()
    try:
        print(download(args.URL, args.output))
    except FileNotFoundError:
        logger.error('Directory is not exist')


if __name__ == '__main__':
    main()
