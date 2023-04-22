# todo: Создайте функцию, которая принимает два аргумента, год и месяц, и возвращает list comprehension,
# содержащий все даты этого месяца в этом году. Используйте функцию monthrange(year, month) из модуля
# calendar для нахождения числа дней в месяце.
import calendar


def all_data_in_y_m(year, month):
    head = ['Пн', "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    c = calendar.monthrange(year, month)

    def get_day_id(i_day):
        _id = (i_day % 7) if i_day > 6 else i_day
        return _id
        
    return [str(f"{head[get_day_id(c[0]+i)]}: {i+1}")for i in range(c[1])]


print(all_data_in_y_m(2023, 4)) 
