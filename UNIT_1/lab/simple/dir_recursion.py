#! /usr/bin/python
# -*- coding: utf-8 -*-
# https://docs-python.ru/standart-library/modul-os-python/funktsija-walk-modulja-os/
#


import os
import sys

#Функция ищет все файлы с именем filename во всех подкаталогах каталога catalog

def find_files(catalog, f):
    find_files = []
    for root, dirs, files in os.walk(catalog):
        print(files)
        find_files += [os.path.join(root, name) for name in files if name == f]
    return find_files

print(find_files(sys.argv[1], sys.argv[2]))
