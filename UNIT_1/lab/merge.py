from argparse import ArgumentParser
import logging
import os
import sys
from pathlib import Path

def init_loger(modeDebug=False):
    logger = logging.getLogger()
    logger.name = "My Application"
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if modeDebug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    return logger

def arguments():
    version = "0.0.1"
    parser = ArgumentParser(prog="argparse_simple", description="Программа для знакомства с библ. argparse.", epilog="Приятного пользования!")
    parser.add_argument('output', help="выходной файл")  # positional argument
    parser.add_argument("-v", "--version", action="version", version=version)
    parser.add_argument("--debug", action="store_true", help="enable debug mode")
    parser.add_argument("--root_dir", help="Принимает папку для обработки")

    return parser

def find_files(catalog, f):
    find_files = []
    for root, dirs, files in os.walk(catalog):
        print(files)
        find_files += [os.path.join(root, name) for name in files if name == f]
    return find_files

def find_files_by_ext(catalog, ext):
    find_files = []
    for root, dirs, files in os.walk(catalog):
        print(files)
        find_files += [os.path.join(root, name) for name in files if name.endswith('.txt')]
    return find_files


if __name__ == "__main__":
    args = arguments().parse_args()
    root_dir = "."
    if args.root_dir: root_dir = args.root_dir
    print(root_dir)
    logger = init_loger(args.debug)
    logger.info("Аргументы: "+ str(args))
    files_list = find_files_by_ext(root_dir,"*.txt")
    logger.info(files_list)

    VectorTelemetry = dict()
    for file in files_list:
        pass
        #VectorTelemetry[Path(file).name.removesuffix] = 
