'''
Рукописная библиотека для реализации специфических процедур.
'''

EPS = 0.00001

class Coords:
    '''
        Класс координат на декартовой оси для удобной работы  с оными.
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
    Вычисляет расстояние между двумя координатами типа Coords.
    '''
    x_1 = coords1.get_x()
    x_2 = coords2.get_x()
    y_1 = coords1.get_y()
    y_2 = coords2.get_y()
    return ((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2) ** 0.5

def rdf(file_opened):
    '''
    Возвращает строку из открытого файла без переноса строки.
    '''
    return file_opened.readline().replace("\n", "")

def equal(real_1, real_2):
    '''
    Сравнивает два float числа через epsilone.
    '''
    return abs(real_1 - real_2) < EPS

def main():
    '''
    Генерирует геттеры и сеттеры для всех полей класса.
    Ввести имя выходного файла и необходимые поля (пустая строка -- конец ввода).
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

if __name__ == "__main__":
    main()
