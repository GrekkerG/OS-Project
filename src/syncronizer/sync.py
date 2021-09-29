# third-party
import os

# built in
from os import listdir
from shutil import copy, copyfile, rmtree

from loguru import logger

# local imports
from .utils import make_abs_path, make_relative_path


def _get_relative_pathes(main_path: str) -> list:
    pathes = []
    for currentpath, folders, files in os.walk(main_path):
        if folders:
            for folder in folders:
                pathes.append(
                    make_relative_path(main_path, os.path.join(currentpath, folder))
                )
        for file in files:
            pathes.append(
                make_relative_path(main_path, os.path.join(currentpath, file))
            )
    return pathes


def _sync_dirs(main_dir: list, main_dir_path: str, sub_dir: list, sub_dir_path: str):
    used_pathes = []
    for path in sub_dir:
        sub_abs_path = make_abs_path(sub_dir_path, path)
        if path not in main_dir:
            sub_abs_path = make_abs_path(sub_dir_path, path)
            try:
                if os.path.isdir(sub_abs_path):
                    rmtree(sub_abs_path)
                else:
                    os.remove(sub_abs_path)
            except FileNotFoundError:
                pass
        else:
            used_pathes.append(path)
            main_abs_path = make_abs_path(main_dir_path, path)
            if not os.path.isdir(main_abs_path):
                copyfile(main_abs_path, sub_abs_path)

    files_to_create = list(set(main_dir) - set(used_pathes))

    for file in files_to_create:
        splitted_path_file = file.split("/")
        current_path = ""

        if len(splitted_path_file) > 2:
            current_path = f"{sub_dir_path}/{'/'.join(splitted_path_file[1:-1])}"
            try:
                os.makedirs(current_path)
            except FileExistsError as exp:
                logger.debug(exp)
        else:
            current_path = sub_dir_path

        main_abs_path = make_abs_path(main_dir_path, file)

        if os.path.isdir(main_abs_path):
            try:
                os.makedirs(f"{current_path}{file[1:]}")
            except FileExistsError as exp:
                logger.debug(exp)
        else:
            if current_path and main_abs_path:
                copy(main_abs_path, current_path)


def sync(pathes: list):
    main_dir = _get_relative_pathes(pathes[0])

    for ind, path in enumerate(pathes[1:], 1):
        sub_dir = _get_relative_pathes(path)
        _sync_dirs(main_dir, pathes[0], sub_dir, pathes[ind])
