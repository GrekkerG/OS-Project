# third-party
# built in
from argparse import ArgumentParser

from loguru import logger


def parse_args() -> tuple:
    parser = ArgumentParser()

    parser.add_argument(
        "--config", default=None, type=str, help="Input path to config file"
    )
    parser.add_argument(
        "--active", default=False, type=bool, help="Whether to keep in sync"
    )

    args = parser.parse_args()

    return args.config, args.active


def read_conf(conf_filename: str) -> list:
    with open(conf_filename, "r") as filehandler:
        dirs = filehandler.read().split("\n")

        return dirs


def make_relative_path(base_dir_path: str, abs_path: str) -> str:
    cutting_index = len(base_dir_path)

    try:
        relative_path = f".{abs_path[cutting_index:]}"

        if relative_path == "./":
            raise ValueError

        return relative_path
    except ValueError as exp:
        logger.debug("Got unexpected base dir path or abs path", exp)


def make_abs_path(abs_path_to_base: str, relative_path: str) -> str:
    return f"{abs_path_to_base}{relative_path[1:]}"
