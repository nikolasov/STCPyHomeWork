# todo:
#     Напишите программу, которая определяет и печатает «похожие» слова. Слово называется похожим на другое слово,
#     если его гласные буквы находятся там же, где находятся гласные буквы другого слова, например:
#     дорога и пароход - похожие слова (гласные буквы на втором, четвертом и шестом местах),
#     станок и прыжок - похожие слова, питон и удав непохожие слова.
#     Считаем, что в русском языке 10 гласных букв (а, у, о, ы, и, э, я, ю, ё, е).
#     Ввод: x –первое слово, например, питон. n – количество слов для сравнения, например 6.
#     Дальше вводятся 6 слов, например: поросенок, титан, итог, лавка, погост, кино.
#     Вывод - слова, похожие на питон: титан, погост, кино
vocalics = ('а', 'у', 'о', 'ы', 'и', 'э', 'я', 'ю', 'ё', 'е')

print("введите первое слово")
word_1 = input()
check_pos = [i for i in range(len(word_1)) if word_1[i] in vocalics]

print("введите число слов для сравнения")
n = int(input())

print(f"введите {n} слов разделенных запятой и знаком пробел") 
words = [i.strip() for i in input().split(", ")]


def find_ident_words(main_word_vocalic_pos, vocalics_list, words_list):
    identical = []
    vocalic_len = len(main_word_vocalic_pos)
    for w in words_list:
        is_ident = True
        nn = [i for i in range(len(w)) if w[i] in vocalics_list]

        if(len(nn) != vocalic_len): #В условии не указано, но судя по всему общее количесвто гласных в словах должно совпадатьпито
            continue
        for i in range(vocalic_len): 
            if main_word_vocalic_pos[i] != nn[i]:
                is_ident = False
                continue
        if is_ident:
            identical.append(w)
    return identical


print(f"слова похожие на {word_1}: {', '.join(find_ident_words(check_pos,vocalics,words))}")