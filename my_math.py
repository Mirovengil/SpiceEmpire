'''
Сий чудо-модуль реализует некоторые необычные функции, которые обозваны
арифметикой чисто для того, чтобы никто не заглядывал в этот файл --
чтобы над их автором не ржали в голос.
'''

EPS = 0.00001

class Coords:
    '''
    Kласс Coords реализован во избежание лишнего использования кортежей. 
    Поля:
        x : int -- координата на оси х;
        y : int -- координата на оси y;
    '''
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    #Геттеры и сеттеры (сгенерированы автоматически)
    def get_x(self):
        '''Геттер поля x'''
        return self.x
    def set_x(self, value):
        '''Сеттер поля x'''
        self.x = value
    def get_y(self):
        '''Геттер поля y'''
        return self.y
    def set_y(self, value):
        '''Сеттер поля y'''
        self.y = value


def dist(coords1, coords2):
    '''
    dist(coords1 : Coords, coords2 : Coords) -- возвращает расстояние
    между точками coords2 и coords2.
    '''
    x_1 = coords1.get_x()
    x_2 = coords2.get_x()
    y_1 = coords1.get_y()
    y_2 = coords2.get_y()
    return ((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2) ** 0.5

def rdf(file_opened):
    '''
    rdf(f : file) -- считывает из файла f (открыть заранее) строку,
    стирает "/n" и возвращает результат.
    '''
    return file_opened.readline().replace("\n", "")

def equal(real_1, real_2):
    '''
    equal(real_1 : float, real_2 : float) : bool -- возвращает True,
    если два вещественных числа real1 и real2 приблизительно равны
    (точность -- до 10-6), в противном случае -- False.
    '''
    return abs(real_1 - real_2) < EPS

def main():
    '''
    Функция main() предназначена для быстрого написания геттеров и сеттеров.
    Порядок работы следующий:

    1.Запустить модуль;
    2.Ввести название выходного файла;
    3.Ввести название поля;
    4.Повторять третий шаг, пока не кончатся поля;
    5.Нажать ENTER;
    6.Открыть выходной файл;
    7.Скопировать готовые геттеры и сеттеры;
    8.Удалить выходной файл;
    9.Использовать готовые геттеры и сеттеры по назначению;
    '''
    fin = open(input("Имя выходного файла:"), "w")
    name = "Шок! Фиолетовое чмо утопило жучка..."

    print("#Геттеры и сеттеры (сгенерированы автоматически)", file=fin)

    while name != "":
        name = input('Название поля:')

        if name == "":
            continue

        print("def get_" + name + "(self):", file=fin)
        print("    '''Геттер поля " + name + "'''", file=fin)
        print("    return self." + name, file=fin)

        print("def set_" + name + "(self, value):", file=fin)
        print("    '''Сеттер поля " + name + "'''", file=fin)
        print("    self." + name + " = value", file=fin)

        print('ДОБАВЛЕНО!')
    print('ГОТОВО!')
    fin.close()

def choose_from(objects):
    '''
    Выводит список объектов под номерами, считывает номер и возвращает
    выбранный объект.
    '''
    for i in enumerate(objects):
        print(i[0] + 1, '. ', i[1], sep='')
    chosen = int(input('ВВОД: '))
    return objects[chosen]

if __name__ == "__main__":
    main()
