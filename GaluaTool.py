from GaluaField import *

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
print("Отображение элементов поля:")
gf.display()

while True:
    print("Выберите действие:\n"
          "[0] Закончить работу\n"
          "[1] Сложить два элемента поля\n"
          "[2] Умножить два элемента поля\n"
          "[3] Нахождение образующих группы и разложение элементов по степеням выбранного образующего")
    mode = int(input())
    if mode == 0:
        break
    elif mode == 1:
        print("Введите два элемента:")
        a = GaluaItem(gf.p, gf.n, create_intm_list([int(i) for i in input()], p))
        b = GaluaItem(gf.p, gf.n, create_intm_list([int(i) for i in input()], p))
        c = a + b
        print("Результат:", *c.coefficients)
    elif mode == 2:
        a = GaluaItem(gf.p, gf.n, create_intm_list([int(i) for i in input()], p))
        b = GaluaItem(gf.p, gf.n, create_intm_list([int(i) for i in input()], p))
        c = a.multiply(b, gf.irreducible)
        print("Результат:", *c.coefficients)
    elif mode == 3:
        forming = gf.find_forming_elements()
        print("Образующие элементы:")
        for i in range(len(forming)):
            print(f'{i}:', *forming[i].coefficients)
        print("Напишите номер образующего элемента, по которому нужно разложить элементы")
        ind = int(input())
        gf.decompose_by_forming_element(forming[ind])
