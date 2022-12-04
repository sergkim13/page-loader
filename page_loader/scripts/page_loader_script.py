#!/usr/bin/env python3
import logging
import sys
import requests
from page_loader import download
from page_loader.args_parser import get_args


logger = logging.getLogger()


def main():
    args = get_args()
    try:
        print(download(args.URL, args.output))
    except FileNotFoundError:
        logger.error(f'Directory \'{args.output}\' does not exist. ')
        sys.exit(72)
    except PermissionError:
        logger.error(
            f"You don't have access to directory \'{args.output}\'."
            f"Check permissions.")
        sys.exit(72)
    except FileExistsError:
        logger.error('File is already exists.')
        sys.exit(72)
    except requests.exceptions.ConnectionError:
        logger.error('Failed to connect URL.')


if __name__ == '__main__':
    main()
