import pprint


class IntM:
    def __init__(self, v: int, m: int):
        self.modulus = m
        self.value = v

    def __add__(self, other):
        if self.modulus != other.modulus:
            raise ValueError
        self.value = (self.value + other.value) % self.modulus

    def __sub__(self, other):
        if self.modulus != other.modulus:
            raise ValueError
        self.value = (self.value - other.value) % self.modulus

    def __gt__(self, other):
        if self.modulus != other.modulus:
            raise ValueError
        self.value = (self.value - other.value) % self.modulus


def createList(lst: list, modulus: int):
    return [IntM(i, modulus) for i in lst]


class GaluaItem:
    def __init__(self, p, n, coefs: list):
        self.coefficients = coefs
        self.p = p
        self.n = n

    def __add__(self, other):
        for i in range(min(len(self.coefficients), len(other.coefficients))):
            self.coefficients[i] += other.coefficients[i]

    def __mul__(self, other):
        pass


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


GaluaField(4, 3).display()
