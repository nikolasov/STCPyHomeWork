#todo:
#   Для задачи task12.py "Морской бой", написать Save game. Пользователь может прервать игру и сохраниться, затем продолжить либо выйти.
#   Предусмотереть возможность восстановить игру из заранее сохраненного состояния. Сохранение произвести в файл по имени.
from typing import Dict, List, Any

#todo:
# Тестовая система выгружает файл в следующем формате:
# {
#     1: 'Пупкин',
#     .......,
#     12. 'Васичкин'
# }
# id1 - дисятичное целое равное номеру задачи
# [
#  { 'id': 1 , 'fail': [ id3, id5], 'pass': [id1, id2, id4]}, 
#  { 'id': 12 , fail: [ id1, id2, id5], 'pass': [id3, id4]} ,.. 
# ]
# Ключи словаря:
#  id - идентификатор студента прошедшего тест
#  pass - количество пройденных задач
#  fail - количесто не пройденных задач
#
#
#
# Необходимо сформировать Excel файл для последующей загрузки в  Spreadsheets Google где в качестве шапки - фамилии, а в качестве
# первого номера - задачи. Поля при этом должны быть заполнены + или - в зависимости от результата проверки.
#
# Материал:
# https://realpython.com/openpyxl-excel-spreadsheets-python/
from openpyxl import Workbook
import random

student_list = {1: 'Петров',
				2: 'Антонова',
				3: 'Степанов',
				4: 'Аксенова',
				5: 'Иванова',
				6: 'Кубрик',
				7: 'Спилберг',
				8: 'Нолан',
				9: 'Карпентер',
				10: 'Лермонтов',
				11: 'Пушкин',
				12: 'Гоголь',
				13: 'Никитин',
				14: 'Патапов',
				15: 'Шишкина',
				16: 'Вовчик',
				17: 'Надоело выдумывать фамилии',
				18: 'Харэ'}

result = ['pass', 'fail']
table_of_results = []
for key, value in student_list.items():
	stud_result = {"id": key, "fail": [], "pass": []}
	for i in range(1, 6):
		stud_result[result[random.randint(0, 1)]].append(f"id{i}")
	table_of_results.append(stud_result)
print(table_of_results)

filename = "hello_world.xlsx"

workbook = Workbook()
sheet = workbook.active
for key, value in student_list.items():
	sheet[f"{chr(ord('A')+key-1)}{1}"] = value
for i in table_of_results:
	Col = chr(ord('A')+i["id"]-1)
	for val in i["fail"]:
		i_d = int(val.replace("id",""))+1
		sheet[f"{Col}{i_d}"] = "-"
	for val in i["pass"]:
		i_d = int(val.replace("id",""))+1
		sheet[f"{Col}{i_d}"] = "+"

workbook.save(filename=filename)

