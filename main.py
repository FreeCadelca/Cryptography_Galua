import pprint


class IntM:
    def __init__(self, v: int, m: int):
        self.modulus = m
        self.value = v

    def __add__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError
            return IntM((self.value + other.value) % self.modulus, self.modulus)
        elif isinstance(other, int):
            return IntM((self.value + other) % self.modulus, self.modulus)
        else:
            raise ValueError

    def __sub__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError
            return IntM((self.value - other.value) % self.modulus, self.modulus)
        elif isinstance(other, int):
            return IntM((self.value - other) % self.modulus, self.modulus)
        else:
            raise ValueError

    def __mul__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError
            return IntM((self.value * other.value) % self.modulus, self.modulus)
        elif isinstance(other, int):
            return IntM((self.value * other) % self.modulus, self.modulus)
        else:
            raise ValueError

    def __floordiv__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError
            v = self.value
            while v % other.value != 0:
                v += self.value
            return IntM(v // other.value, self.modulus)
        elif isinstance(other, int):
            v = self.value
            while v % other != 0:
                v += self.value
            return IntM(v // other, self.modulus)
        else:
            raise ValueError

    def __gt__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError
            return self.value > other.value
        elif isinstance(other, int):
            return self.value > other
        else:
            raise ValueError

    def __str__(self):
        return f'{self.value}m{self.modulus}'


def create_intm_list(lst: list, modulus: int):
    return [IntM(i, modulus) for i in lst]


def trimListWithZeros(lst: list):
    max_pow = 0
    for i in range(len(lst) - 1, -1, -1):
        if lst[i].value != 0:
            max_pow = len(lst) - 1 - i
    lst = lst[len(lst) - 1 - max_pow:]
    return lst


class GaluaItem:
    def __init__(self, p, n, coefs: list):
        self.coefficients = coefs
        self.p = p
        self.n = n

    def copy(self):
        return GaluaItem(self.p, self.n, coefs=self.coefficients.copy())

    def __copy__(self):
        return self.copy()

    def __len__(self):
        return self.n + 1

    def __add__(self, other):
        newGaluaItem = self.copy()
        for i in range(min(len(newGaluaItem.coefficients), len(other.coefficients))):
            newGaluaItem.coefficients[i] += other.coefficients[i]

    # перемножение многочленов методом фонтанчика
    def fontain(self, other):
        self.coefficients = trimListWithZeros(self.coefficients)
        other.coefficients = trimListWithZeros(other.coefficients)

        max_pow = len(self.coefficients) + len(other.coefficients) - 2
        pre_res = [IntM(0, self.p) for i in range(max_pow + 1)]
        for i in range(len(self.coefficients)):
            for j in range(len(other.coefficients)):
                power_i = len(self.coefficients) - 1 - i
                power_j = len(other.coefficients) - 1 - j
                pre_res[max_pow - (power_i + power_j)] += self.coefficients[i] * other.coefficients[j]
        return trimListWithZeros(pre_res)

    # def __get_big_degrees__(irreducible, max_pow):

    def multiply(self, other, irreducible):
        def __get_big_degrees__(irreducible) -> dict:
            BigDegrees = dict()
            # выражаем наибольшую степень из неприводимого многочлена
            BigDegrees[len(irreducible) - 1] = \
                [irreducible[i] * -1 // irreducible[0] for i in range(1, len(irreducible))]
            BigDegrees[len(irreducible) - 1] = trimListWithZeros(BigDegrees[len(irreducible) - 1])
            for new_degree in range(len(irreducible), len(irreducible) * 2 - 3):
                lastDegreeInGaluaItem = GaluaItem(
                    BigDegrees[new_degree - 1][0].modulus,
                    len(irreducible) - 1,
                    BigDegrees[new_degree - 1].copy()
                )
                singleXInGaluaItem = GaluaItem(
                    BigDegrees[new_degree - 1][0].modulus,
                    len(irreducible) - 1,
                    create_intm_list([1, 0], BigDegrees[new_degree - 1][0].modulus)
                )
                BigDegrees[new_degree] = lastDegreeInGaluaItem.fontain(singleXInGaluaItem)
                if len(BigDegrees[new_degree]) == len(irreducible):
                    multedPoly = GaluaItem(self.p, self.n, BigDegrees[len(BigDegrees[new_degree]) - 1]).fontain(
                        GaluaItem(self.p, self.n, [BigDegrees[new_degree][0]])
                    )
                    for indexInAddPoly in range(len(multedPoly)):
                        BigDegrees[new_degree][len(BigDegrees[new_degree]) - 1 - indexInAddPoly] += multedPoly[len(multedPoly) - 1 - indexInAddPoly]
                    BigDegrees[new_degree][0].value = 0
                    BigDegrees[new_degree] = trimListWithZeros(BigDegrees[new_degree])
            for key, item in BigDegrees.items():
                print(f'x^{key}:', *item)
            return BigDegrees

        bigDegreesDict = __get_big_degrees__(irreducible)

        # Выполняем умножение методом фонтанчика
        pre_res = self.fontain(other)

        # Подставляем в высокие степени многочлена, используя наш словарь,
        # в котором мы выражали все такие "большие" степени
        for i in range(0, len(pre_res) - self.n):
            multedPoly = GaluaItem(self.p, self.n, bigDegreesDict[len(pre_res) - 1 - i]).fontain(
                GaluaItem(self.p, self.n, [pre_res[i]])
            )
            for indexInAddPoly in range(len(multedPoly)):
                pre_res[len(pre_res) - 1 - indexInAddPoly] += multedPoly[len(multedPoly) - 1 - indexInAddPoly]
            pre_res[i].value = 0
        pre_res = trimListWithZeros(pre_res)
        print(*pre_res)

        return GaluaItem(self.p, self.n, pre_res)


class GaluaField:
    def __init__(self, p, n):
        self.p = p
        self.n = n

    def display(self):
        def rec(pos=self.n - 1) -> list:
            # делаем "простые элементы", состоящие из одного компонента - последнего (0, 1, 2, 3, 4, ... (p-1))
            simple_values = [[j] for j in range(self.p)]

            # если это последняя позиция (самая последняя компонента), то возвращаем список простых элементов поля
            if pos < 0:
                return simple_values

            # иначе рекурсивно прибавляем к простым элементам следующие такие же списки
            new_values = []
            for i in range(len(simple_values)):
                for adjacent in rec(pos=pos - 1):
                    new_values.append(simple_values[i] + adjacent)
            return new_values

        # запускаем рекурсию и записываем результат в items
        items = rec()

        # собираем форматированную строку для вывода
        s = ""
        for item in items:
            # флаг, обозначающий, вывелся ли первый ненулевой элемент, чтобы знать, когда выводить " + "
            fl = 0
            for i in range(len(item)):
                if item[i] != 0:
                    if fl == 0:
                        fl = 1
                    else:
                        s += ' + '
                    if self.n - i == 0:
                        s += f'{item[i]}'
                    elif self.n - i == 1:
                        s += f'{item[i]}x'
                    else:
                        s += f'{item[i]}x{self.n - i}'
            if fl == 0:
                s += '0'
            s += ';\n'
        print(s)



# Пример неприводимого многочлена x^3 + x + 1
irreducible = create_intm_list([1, 1, 0, 1], 2)

# Пример элементов поля
a = GaluaItem(2, 3, create_intm_list([1, 1, 1], 2))
b = GaluaItem(2, 3, create_intm_list([1, 0, 0], 2))

# Умножение элементов
result = a.multiply(b, irreducible)

# Вывод результата
print("Результат умножения:")
for coef in result.coefficients:
    print(coef)
