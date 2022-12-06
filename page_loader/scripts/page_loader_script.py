#!/usr/bin/env python3
import logging
import sys
import requests
from page_loader import download
from page_loader.args_parser import get_args
from page_loader.logger import init_logger


# Создаем логгер
init_logger(__name__)
logger = logging.getLogger(__name__)


def main():
    args = get_args()
    try:
        download(args.URL, args.output)
    except FileNotFoundError:
        logger.error(f'Directory \'{args.output}\' does not exist.')
        sys.exit(72)
    except PermissionError:
        logger.error(
            f"You don't have access to directory \'{args.output}\'."
            f"Check permissions.")
        sys.exit(72)
    except FileExistsError:
        logger.error('File or directory is already exists.')
        sys.exit(72)
    except (requests.exceptions.RequestException, OSError):
        logger.error(f'Failed to download {args.URL}.')
        sys.exit(1)


if __name__ == '__main__':
    main()
