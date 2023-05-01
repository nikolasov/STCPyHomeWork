#todo
# Создайте декоратор, которые переводит все текстовые аргументы функции в верхний регистр и возвращает их в виде списка текстовых аргументов.


def uper_decorator(func):

    def wraper(*args):
        upper_args_list = [i.upper() for i in args if type(i) == type(str())]
        func(*args)
        return upper_args_list
    return wraper


@uper_decorator
def print_args(*args):
    print("All args: "+", ".join([str(i) for i in args]))


result_list = print_args(12, "test", [1, 9854, 123], "dsadfdasf")
print(result_list)
