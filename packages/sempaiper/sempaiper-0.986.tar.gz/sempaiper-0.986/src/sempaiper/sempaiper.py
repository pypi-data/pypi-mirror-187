import os.path

from PIL import Image



class q1:
    def files(destdir):
        

        files = [ f for f in os.listdir(destdir) if os.path.isfile(os.path.join(destdir,f)) ]

        print(files)

    def pictures(path1,number, search=-1, w=200, h=300):
        path = 'q1_1/'
        sklad = {1: ['Дайте определение системы m линейных алгебраических уравнений c n неизвестными. Какая СЛАУ называется однородной, неоднородной. Приведите соответствующие примеры. Может ли неоднородная СЛАУ Ax = b быть неопределенной, если столбцы её матрицы линейно независимы (линейно зависимы)? Ответ необходимо обосновать.', 
                    [Image.open(f'{path1}/{path}/1/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/1') if os.path.isfile(os.path.join(f'{path1}/{path}/1', f))]]]
                 }
        if number == -1:
            numbers = []
            for i, j in sklad.items():
                if search in j[0]:
                    numbers.append(i)
            return 'есть в этих номерах: ', numbers
        print(sklad[number][0])
        new_img = []
        for a in sklad[number][1]:
            #while height > 1000:
            #    width /= 1.5
            #    height /= 1.5
            a = a.resize((w, h))
            new_img.append(a)
        return new_img


class q2:
    def pictures(path1,number, search=-1, w=200, h=300):
        path = 'q2_1/'
        sklad = {1: ['Дайте определение комплексного числа в алгебраической форме. Приведите тригонометрическую и показательную формы комплексного числа. Выведите формулу площади параллелограмма с вершинами в точках z1 и z2 комплексной плоскости.', 
                    [Image.open(f'{path1}/{path}/1/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/1') if os.path.isfile(os.path.join(f'{path1}/{path}/1', f))]]],
                 2: ['Выведите формулы для извлечения корня n-ой степени из комплексного числа и приведите геометрическую интерпретацию о расположении n значений корня. Какой корень называется примитивным. Приведите свойства примитивных корней.',
                     [Image.open(f'{path1}/{path}/2/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/2') if os.path.isfile(os.path.join(f'{path1}/{path}/2', f))]]],
                 3: ['(картинок нет)Дайте определение наибольшего общего делителя многочленов, наименьшего общего кратного многочленов. Приведите линейное разложение наибольшего общего делителя. Какие многочлены называются взаимно простыми? Приведите соответствующие примеры. Найдите многочлены u(x) и v(x) такие, что (2x^3 − 7x^2 − 9x + 63)u(x) + (x^3 + x^2 − 19x − 9)v(x) = 1.'+
                     '\n Решение: Наибольшим общим делителем НОД (f, g) = (f, g), где f, g ∈ R[x], называется многочлен d(x) ∈ R[x] максимальной степени, на который делятся (без остатка) оба многочлена.\nОбозначение: d(x) = НОД(f, g) = (f, g).\nОпределение. Наименьшим общим кратным НОК(f,g) = (f,g), где f,g ∈ R[x], называется многочлен L(x) ∈ R[x] наименьшей степени, который де- лится (без остатка) на каждый из многочленов f(x) и g(x).\nОбозначение: L(x) = НОK(f, g). \nТеорема. 1) Для ∀f, g ∈ R[x] найдутся d = НОД(f, g) и L = НОK(f, g).\n2) (The polynomial extended euclidean algorithm) При помощи алгоритма\nЕвклида найдутся многочлены u, v ∈ R[x] такие, что fu + gv = НОД(f, g) = d.\nОпределение. Многочлены f, g ∈ R[x] называются взаимно-простыми, если d = НОД(f,g) = 1.\nПример: Пусть p(x) = x**3 - x**2 + x - 1 ; q(x) = x**3 -x**2 + 1, то НОД(p,q) = 1 => они взаимнопростые',
                     [Image.open(f'{path1}/{path}/3/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/3') if os.path.isfile(os.path.join(f'{path1}/{path}/3', f))]]],
                 4: ['Дайте определение неприводимого многочлена. Будет ли неприводимым многочленом над R многочлен вида x^4 + 4? Ответ необходимо обосновать.'+
                     '\n Решение: Многочлен f ненулевой степени из R[x] (или C[x], в общем слу- чае K[x]) называется неприводимым (или неприводимым над полем K), ес- ли он не делится ни на какой другой многочлен g ∈ R[x] меньшей степени, 0 < deg(g) < deg(f).\nНе будет. Он приводим над R так как он делится на другие многочлены меньшей степени которые принадлежат R, разложение:',
                     [Image.open(f'{path1}/{path}/4/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/4') if os.path.isfile(os.path.join(f'{path1}/{path}/4', f))]]],
                 5: ['Дайте определение алгебраической кратности корня многочлена. Приведите соответствующие примеры. Сформулируйте основную теорему алгебры комплексных чисел. Является ли поле C алгебраически замкнутым? Ответ необходимо обосновать.',
                     [Image.open(f'{path1}/{path}/5/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/5') if os.path.isfile(os.path.join(f'{path1}/{path}/5', f))]]],
                 6: ['Приведите (с выводом) формулы Виета для многочлена f ∈ C[z], deg(f) = n',
                     [Image.open(f'{path1}/{path}/6/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/6') if os.path.isfile(os.path.join(f'{path1}/{path}/6', f))]]],
                 7: ['Приведите свойства (с доказательством) комплексных корней для многочленов с вещественными коэффициентами f ∈ R[z], deg(f) = n. Разложите на множители над R многочлен x^5 − 1 ∈ R[x].',
                     [Image.open(f'{path1}/{path}/7/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/7') if os.path.isfile(os.path.join(f'{path1}/{path}/7', f))]]],
                 8: ['Дайте определение многочлена от нескольких переменных. Какой многочлен называется симметричеcким? Приведите выражения основных симметрических многочленов.',
                     [Image.open(f'{path1}/{path}/8/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/8') if os.path.isfile(os.path.join(f'{path1}/{path}/8', f))]]],
                 9: ['Приведите формулы элементарных симметрических многочленов sk(x1, x2, . . . , xn). Укажите их в явном виде для случая n = 4, k = 4.',
                     [Image.open(f'{path1}/{path}/9/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/9') if os.path.isfile(os.path.join(f'{path1}/{path}/9', f))]]],
                 10: ['Приведите формулы Ньютона, которые связывают многочлены Ньютона (степенные суммы) с элементарными симметрическими многочленами sk(x1, x2, . . . , xn).',
                     [Image.open(f'{path1}/{path}/10/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/10') if os.path.isfile(os.path.join(f'{path1}/{path}/10', f))]]],
                 11: ['Приведите основную теорему симметрических многочленов и проиллюстрируйте её на примере симметрического многочлена f(x1,x2,x3)=x1^3*x2+x2^3*x3+x3^3*x1+x1*x2^3+x2*x3^3+x3*x1^3 представив его в виде явного многочлена от элементарных симметрических многочленов.',
                     [Image.open(f'{path1}/{path}/11/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/11') if os.path.isfile(os.path.join(f'{path1}/{path}/11', f))]]],
                 12: ['Дайте определение дискриминанта мночочлена n-ой степени с комплексными коэффициентами и приведите основные свойства дискриминанта многолена. Приведите формулу для определения дискриминанта многочлена и пользуясь этой формулой найдите дискриминант многочлена f(z) = z^3 + a*z + b.' +
                      '\n Решение: *картинка0* \n 1) Дискриминант равен нулю тогда и только тогда, когда многочлен имеет кратные корни. \n2) Дискриминант является симметрическим многочленом относительно корней многочлена и поэтому является многочленом от его коэффициентов; более того, коэффициенты этого многочлена целые независимо от расширения, в котором берутся корни.\n *картинка1*',
                     [Image.open(f'{path1}/{path}/12/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/12') if os.path.isfile(os.path.join(f'{path1}/{path}/12', f))]]],
                 13: ['Дайте определение результанта двух многочленов n-ой и m-ой степеней. Приведите основные свойства результанта многочленов. Найдите многочлены u(x) и v(x) такие, что f(x)u(x) + g(x)v(x) = Res(f(x); g(x)),где f(x) = x4 − 10x2 + 1, g(x) = x4 − 4√2x3 + 6x2 + 4√2x + 1.',
                     [Image.open(f'{path1}/{path}/13/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/13') if os.path.isfile(os.path.join(f'{path1}/{path}/13', f))]]]}
        if number == -1:
            numbers = []
            for i, j in sklad.items():
                if search in j[0]:
                    numbers.append(i)
            return 'есть в этих номерах: ', numbers
        print(sklad[number][0])
        new_img = []
        for a in sklad[number][1]:
            #while height > 1000:
            #    width /= 1.5
            #    height /= 1.5
            a = a.resize((w, h))
            new_img.append(a)
        return new_img


class q3:
    def pictures(path1,number, search=-1, w=200, h=300):
        path = 'q3_1/'
        sklad = {1: ['Дайте определение линейного пространства и приведите примеры линейных пространств. Является ли линейным пространством V1 = {f ∈ R4[x] : f(5) = 0}, V2 = {f ∈ R4[x] : f(5) = 2}? Ответ необходимо обосновать.', 
                    [Image.open(f'{path1}/{path}/1/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/1') if os.path.isfile(os.path.join(f'{path1}/{path}/1', f))]]]}
        if number == -1:
            numbers = []
            for i, j in sklad.items():
                if search in j[0]:
                    numbers.append(i)
            return 'есть в этих номерах: ', numbers
        print(sklad[number][0])
        new_img = []
        for a in sklad[number][1]:
            #while height > 1000:
            #    width /= 1.5
            #    height /= 1.5
            a = a.resize((w, h))
            new_img.append(a)
        return new_img
