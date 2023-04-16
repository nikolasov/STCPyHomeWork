from argparse import ArgumentParser
import logging
import os
from pathlib import Path
import json

def init_loger(modeDebug=False):
    logger = logging.getLogger()
    logger.name = "My Application"
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(name)s - %(message)s')
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

def find_files_by_ext(catalog, ext):
    find_files = []
    for root, dirs, files in os.walk(catalog):
        find_files += [os.path.join(root, name) for name in files if name.endswith('.txt')]
    return find_files

def save_to_json(_dict, outfile):
    if type(_dict) != type(dict()):
        return False
    
    fp = open(outfile, 'w')
    fp.write(json.dumps({"VectorTelemetry":_dict}))
    fp.close()
    return True


if __name__ == "__main__":
    # Парсим аргументы командной строки
    args = arguments().parse_args()
    # Определяем рабочую папку. Так как параметр необязательный 
    # дефолтный путь считается рабочая директория
    root_dir = "."
    if args.root_dir: root_dir = args.root_dir

    # Инициализируем логер
    logger = init_loger(args.debug)
    logger.info("Аргументы: "+ str(args))
    # Определяем список искомых файлов
    VectorTelemetry = dict.fromkeys(['w','x','y','z'])
    # Ищем все фйлы с расширением txt
    files_list = find_files_by_ext(root_dir,"*.txt")
    logger.debug(files_list)

    #Пробегаем по найденным файлам, если они имеются в словаре
    #читаем содержимое и фиксируем в словаре
    #проверку на 
    for file in files_list:
        p = Path(file).name.removesuffix(Path(file).suffix)
        if not (p in VectorTelemetry):
            continue
        f = open(file)
        val = f.read()
        try:
            temp = float(val)
            val = temp
        except:
            logger.error("Cant converting string to float!")
        f.close()
        VectorTelemetry[p] = val 

    logger.debug("save dictionary to json path = "+root_dir+"/"+args.output)
    if save_to_json(VectorTelemetry,root_dir+"/"+args.output):
        logger.info("Success writing file "+ root_dir+"/"+args.output)
    else:
        logger.warn("Cant't save file "+ root_dir+"/"+args.output)