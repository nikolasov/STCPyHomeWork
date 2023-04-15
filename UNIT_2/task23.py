# todo: На вход подается список, состоящий из списков чисел, например: [[1,5,3], [2,44,1,4], [3,3]].
#  Отсортируйте этот список по возрастанию общего количества цифр в каждом списке.
#  Каждый список отсортируйте по убыванию.
# [1,45 ,3,100], [3423,2,34,4], [3,3]
print("Input lis of number list")
list_of_lists = [i.strip() for i in input().split(", ")]


for i in range(len(list_of_lists)):
    if len(list_of_lists[i])>=2:
        temp = list_of_lists[i][1:len(list_of_lists[i])-1]
        list_of_lists[i] = sorted(
                    [int(i.strip()) for i in temp.split(",")],
                                  reverse=True)


print(sorted(list_of_lists,reverse=False,key=lambda item:len(item)))