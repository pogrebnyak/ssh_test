import random

def loto(bol_comb,bol):
    #bol_comb = 6 Количество шаров в комбинации
    #bol = 52 Количество шаров
    mess = ''


    bol_basket = []
    bol_number = [x for x in range(1,bol + 1)]

    for i in range(bol_comb):
        bol_basket.append(bol_number.pop(bol_number.index(random.choice(bol_number))))

    bol_basket.sort()

    for i in bol_basket:
        if i == bol_basket[len(bol_basket) - 1]:
            mess += f'{i:02}'
            break
        mess += f'{i:02}-'
        
    return mess



