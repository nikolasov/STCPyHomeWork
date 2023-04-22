#todo:
# Каждый третий четверг каждого месяца билеты в Эрмитаж бесплатны. Напечатайте список дат в 2023 году, когда вход бесплатен.
import calendar
month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']


def get_freebie_tick_days(_year_):
    def check_day(i_day):
        _id = i_day % 7 if i_day > 6 else i_day
        res = True if _id == 3 else False
        return res
    result = []
    for i in range(0, 12):
        c = calendar.monthrange(_year_, i + 1)
        counter = 0
        for j in range(c[1]):
            if check_day(c[0]+j):
                if counter == 2:
                    result.append(str(f"{month[i]}: {j + 1}"))
                counter = 0 if counter >= 2 else counter + 1
    return result


_year_ = 2023
print(f"{_year_}:{get_freebie_tick_days(_year_)}")
                