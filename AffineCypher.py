from AlphabetConfig100 import *
from GaluaField import *


def from_10_to_n(number: str, n: int):
    number = int(number)
    res = ''
    while number > 0:
        res += str(number % n)
        number //= n
    res = res[::-1]
    return res


def from_n_to_10(number: str, n: int):
    return sum([int(number[i]) * n ** (len(number) - 1 - i) for i in range(len(number))])


def text_to_nums(s: str, p: int, n: int):
    return ''.join(f'{from_10_to_n(A_ID[i], p):0>{n}}' for i in s)


def nums_to_galuas(s: str, p: int, n: int):
    return [GaluaItem(p, n, create_intm_list([int(j) for j in s[i:i + n]], p)) for i in range(0, len(s), n)]


def galuas_to_nums(galua_items: list, p: int, n: int):
    return ''.join(''.join(f'{coef.value}' for coef in galua_item.coefficients) for galua_item in galua_items)


def nums_to_text(s: str, p: int, n: int):
    return ''.join(A[int(from_n_to_10(s[i:i + n], p))] for i in range(0, len(s), n))


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
        x_galuas = nums_to_galuas(text_to_nums(x, self.__p, self.__n), self.__p, self.__n)
        y_galuas = []
        for galua_item_x in x_galuas:
            y_galuas.append(galua_item_x.multiply(self.__key_alpha, self.__irreducible) + self.__key_beta)
        y = nums_to_text(galuas_to_nums(y_galuas, self.__p, self.__n), self.__p, self.__n)
        return y

    def decrypt(self, y):
        y_galuas = nums_to_galuas(text_to_nums(y, self.__p, self.__n), self.__p, self.__n)
        x_galuas = []
        for galua_item_y in y_galuas:
            x_galuas.append((galua_item_y - self.__key_beta).multiply(
                self.__key_alpha.inv(self.__irreducible), self.__irreducible)
            )
            if len(x_galuas[-1].coefficients) < self.__n:
                diff = self.__n - len(x_galuas[-1].coefficients)
                x_galuas[-1].coefficients = create_intm_list([0] * diff, self.__p) + x_galuas[-1].coefficients
        try:
            x = nums_to_text(galuas_to_nums(x_galuas, self.__p, self.__n), self.__p, self.__n)
        except Exception:
            exit(0)
        return x

    def info(self):
        print(f'keys: ({self.__key_alpha}, {self.__key_beta})')


p = 10
n = 2
alpha = GaluaItem(p, n, create_intm_list([5, 2], p))
beta = GaluaItem(p, n, create_intm_list([1, 9], p))
irreducible = create_intm_list([1, 0, 1], p)
cipher = AffineCypher(alpha, beta, p, n, irreducible)
text = 'Mother is most important person'
print(text)
cipher_text = cipher.encrypt(text)
print(cipher_text)
new_text = cipher.decrypt(cipher_text)
print(new_text)