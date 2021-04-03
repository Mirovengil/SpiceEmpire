#рукописная библиотека для специфической арифметики
EPS = 0.00001

class Coords:
    def __init__(self, x = None, y = None):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
    #Геттеры и сеттеры (сгенерированы автоматически)
    def get_x(self):
        return self.x
    def set_x(self, value):
        self.x = value
    def get_y(self):
        return self.y
    def set_y(self, value):
        self.y = value


def dist(coords1, coords2):
    x1 = coords1.get_x()
    x2 = coords2.get_x()
    y1 = coords1.get_y()
    y2 = coords2.get_y()
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def rdf(f):
    return f.readline().replace("\n", "")

def equal(real_1, real_2):
    return True if abs(real_1 - real_2) < EPS else False

def main():
    #Генерирует геттеры и сеттеры для всех полей класса. 
    #Ввести имя выходного файла и необходимые поля (пустая строка -- конец ввода).
    f = open(input("Имя выходного файла:"), "w")
    name = "Шок! Фиолетовое чмо утопило жучка..."
    print("#Геттеры и сеттеры (сгенерированы автоматически)", file = f)
    while name != "":
        name = input('Название поля:')
        if name == "":
            continue
        print("def get_" + name + "(self):", file = f)
        print("    return self." + name, file = f)
        
        print("def set_" + name + "(self, value):", file = f)
        print("    self." + name + " = value", file = f)
        
        print('ДОБАВЛЕНО!')
    print('ГОТОВО!')
    f.close()

if __name__ == "__main__":
    main()
