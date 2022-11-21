#!/usr/bin/env python3
from page_loader import download
from page_loader.args_parser import get_args


def main():
    args = get_args
    print(download(args.url, args.output))


if __name__ == '__main__':
    main()
