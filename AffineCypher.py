from AlphabetConfig121 import *
from GaluaField import *


def from_10_to_n(number: str, n: int) -> list[int]:
    number = int(number)
    res = []
    while number > 0:
        res.append(number % n)
        number //= n
    res = res[::-1]
    return res


def from_n_to_10(number: list[IntM], n: int) -> int:
    return sum([number[i].value * n ** (len(number) - 1 - i) for i in range(len(number))])


# def text_to_nums(s: str, p: int, n: int):
#     return ''.join(f'{from_10_to_n(A_ID[i], p):0>{n}}' for i in s)

def text_to_galuas(s: str, p: int, n: int):
    arr = []
    for i in s:
        i_p = from_10_to_n(A_ID[i], p)
        new_coefs = [c for c in i_p]
        arr.append(GaluaItem(p, n, create_intm_list(new_coefs, p)))
    return arr


# def nums_to_galuas(s: str, p: int, n: int):
#     return [GaluaItem(p, n, create_intm_list([int(j) for j in s[i:i + n]], p)) for i in range(0, len(s), n)]


# def galuas_to_nums(galua_items: list[GaluaItem], p: int, n: int):
#     return ''.join(''.join(f'{coef.value}' for coef in galua_item.coefficients) for galua_item in galua_items)


def galuas_to_text(galua_items: list[GaluaItem], p: int, n: int):
    text = ''
    for item in galua_items:
        new_num = from_n_to_10(item.coefficients, p)
        text += A[new_num]
    return text


# def nums_to_text(s: str, p: int, n: int):
#     return ''.join(A[int(from_n_to_10(s[i:i + n], p))] for i in range(0, len(s), n))


# s = '!%$a'
# nums = text_to_nums(s, 10, 2)
# galuas = nums_to_galuas(nums, 10, 2)
# nums_s = galuas_to_nums(galuas, 10, 2)
# s_s = nums_to_text(nums_s, 10, 2)
# print(s_s)


class AffineCypher:
    def __init__(self, key_alpha: GaluaItem, key_beta: GaluaItem, p: int, n: int, irreducible: list):
        self.__key_alpha = key_alpha
        self.__key_beta = key_beta
        self.__p = p
        self.__n = n
        self.__irreducible = irreducible

    def encrypt(self, x):
        x_galuas = text_to_galuas(x, self.__p, self.__n)
        y_galuas = []
        for galua_item_x in x_galuas:
            new_item_1 = galua_item_x.multiply(self.__key_alpha, self.__irreducible)
            new_item = new_item_1 + self.__key_beta

            if len(new_item.coefficients) != x_galuas[0].n:
                new_item.coefficients = [IntM(0, x_galuas[0].p) for _ in range(x_galuas[0].n - len(new_item.coefficients))] + new_item.coefficients
            y_galuas.append(new_item)
        y = galuas_to_text(y_galuas, self.__p, self.__n)
        return y

    def decrypt(self, y):
        y_galuas = text_to_galuas(y, self.__p, self.__n)
        x_galuas = []
        for galua_item_y in y_galuas:
            if len(galua_item_y.coefficients) < self.__n:
                diff = self.__n - len(galua_item_y.coefficients)
                galua_item_y.coefficients = create_intm_list([0] * diff, self.__p) + galua_item_y.coefficients
            x_galuas.append((galua_item_y - self.__key_beta).multiply(
                self.__key_alpha.inv(self.__irreducible), self.__irreducible)
            )
            if len(x_galuas[-1].coefficients) < self.__n:
                diff = self.__n - len(x_galuas[-1].coefficients)
                x_galuas[-1].coefficients = create_intm_list([0] * diff, self.__p) + x_galuas[-1].coefficients
        x = galuas_to_text(x_galuas, self.__p, self.__n)
        return x

    def info(self):
        print(f'keys: ({self.__key_alpha}, {self.__key_beta})')


p, n = map(int, input("Введите p и n для поля:\n").split())
irr = []
choose = int(input("Введёте неприводимый многочлен[0] или сгенерировать[1]?\n"))
if choose == 0:
    print("Вводите многочлен в виде abcde..., "
          "где a - коэффициент при старшем члене, b - при втором по старшинству и т.д.\n")
    irr = create_intm_list([int(i) for i in input()], p)
else:
    irr = find_irreducible(p, n, 1)[0]
    print("Сгенерированный неприводимый многочлен:", *irr)
gf = GaluaField(p, n, irr)
print("Введите ключи alpha и beta для шифра:")
alpha = GaluaItem(gf.p, gf.n, create_intm_list([int(i) for i in input()], p))
beta = GaluaItem(gf.p, gf.n, create_intm_list([int(i) for i in input()], p))
cypher = AffineCypher(alpha, beta, gf.p, gf.n, gf.irreducible)
while True:
    mode = input("Введите операцию (E/D - Encrypt/Decrypt)\n")
    print("Введите строку для зашифрования/расшифрования:")
    text = input()
    if mode == "E":
        print(cypher.encrypt(text))
    elif mode == "D":
        print(cypher.decrypt(text))
    elif mode == "exit":
        break


# p = 5
# n = 3
# alpha = GaluaItem(p, n, create_intm_list([4, 2, 1], p))
# beta = GaluaItem(p, n, create_intm_list([1, 3, 0], p))
# irreducible = find_irreducible(p, n)[0]
# cipher = AffineCypher(alpha, beta, p, n, irreducible)
# text = 'Mother is most important person'
# print(text)
# cipher_text = cipher.encrypt(text)
# print(cipher_text)
# new_text = cipher.decrypt(cipher_text)
# print(new_text)

# p = 11
# n = 2
# alpha = GaluaItem(p, n, create_intm_list([10, 7], p))
# beta = GaluaItem(p, n, create_intm_list([5, 2], p))
# irreducible = find_irreducible(p, n)[0]
# cipher = AffineCypher(alpha, beta, p, n, irreducible)
# text = 'Mother is most important person'
# print(text)
# cipher_text = cipher.encrypt(text)
# print(cipher_text)
# new_text = cipher.decrypt(cipher_text)
# print(new_text)

