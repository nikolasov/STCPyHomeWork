#!/usr/bin/python3
# -*- coding: utf-8 -*-
# documentation: https://docs.python.org/3/library/argparse.html

# todo: Ознакомившись с документаций  необходимо к парсеру добавить два аргумента
# 1 позиционный параметр output который принимает название создаваемого файла в формате json
# 2 Опциональный аргумент --root_dir для указания директории обхода

# При запусе скрипта:
# $ ./argparse_.py -h
# Итоговый вывод должен получиться таким:
# argparse_ [-h] [-v] [--debug] [--root ROOT] output

from argparse import ArgumentParser

version = "0.0.1"
parser = ArgumentParser(prog="argparse_simple", description="Программа для знакомства с библ. argparse.", epilog="Приятного пользования!")
parser.add_argument('output', help="выходной файл")  # positional argument
parser.add_argument("-v", "--version", action="version", version=version)
parser.add_argument("--debug", action="store_true", help="enable debug mode")
parser.add_argument("--root_", help="Принимает папку для обработки")


args = parser.parse_args()

if __name__ == "__main__":
    print("Welcome")
    args = parser.parse_args()
    print(args)
    if args.debug:
        print("Включить режим отладки")
    else:
        print("Выключить  режим отладки")
