'''
Сий чудо-модуль содержит заморский класс звезды, написанный руссийским
гением Иваном.

А если серьёзно, то здесь размещён класс звезды Star и некоторые
связанные с ним функции, отображённые в качестве статических методов.
'''

from my_math import rdf
from class_planet import Planet
import my_math

SIZE = 20
MARKER = ' @'
PLANET = ' *'
NONE = ' _'

class Star:
    '''
    Класс звезды.
    '''
    @staticmethod
    def get_neighbour(way):
        '''
            Возвращает номер звезды, к которой ведёт way.
        '''
        return way[1]

    @staticmethod
    def get_way_len(way):
        '''
        Возвращает длину пути way.
        '''
        return way[0]

    def __init__(self, name, neighbours):
        self.name = name
        self.neighbours = neighbours
        self.planets = None
        self.size_x = 0
        self.size_y = 0
        self.can_be_seen = set()

    def set_size(self, size_x, size_y):
        '''
        Устанавливает размеры планетарной карты звезды в (size_x, size_y)
        '''
        self.size_x = size_x
        self.size_y = size_y

    def get_name(self):
        '''
            Геттер, возвращает значение поля name.
        '''
        return self.name

    def get_neighbours(self):
        '''
            Геттер, возвращает значение поля neighbours.
        '''
        return self.neighbours

    def set_planets(self, planets):
        '''
            Сеттер, задаёт значение поля planets.
        '''
        self.planets = planets

    def planets_number(self):
        '''
            Геттер, возвращает длину поля planets.
        '''
        return len(self.planets)

    def str(self, other):
        '''
        Конвертирует Star в строку. Может быть использовано для
        логгирования, например. Или для ASCII-графики.
        '''
        string = ""
        temp_coords = []
        string = string + "-" * SIZE + "\n"
        string = string + 'Название звезды: ' + str(self.name) + "\n"
        string = string + 'Кол-во планет: ' + \
        str(self.planets_number()) + "\n"
        string = string + 'Соседи: ' + "\n"
        for j in self.get_neighbours():
            string = string + '    > ' + \
            other[Star.get_neighbour(j)].get_name() + ' (' + \
            str(Star.get_way_len(j)) +  'ПА' +  ')' + "\n"
        string = string + "\n"
        string = string + 'Планеты: ' + "\n"
        for j in self.planets:
            string = string + str(j)
            temp_coords.append(j.get_coordinates())
        string = string + "Положение планет: " + "\n"
        string = string + self.to_matrix()
        string = string + '-' * SIZE + "\n"
        return string

    def cache(self):
        '''
        Кеширует Star. Предполагается, что это будет использовано для
        реализации сохранений.
        '''
        string = ""
        string = string + self.name + "\n"
        string = string + str(len(self.neighbours)) + "\n"
        for i in self.neighbours:
            string = string + str(i[0]) + "\n"
            string = string + str(i[1]) + "\n"
        string = string + str(len(self.planets)) + "\n"
        for i in self.planets:
            string = string + i.cache()
        return string

    @staticmethod
    def read_star(fin):
        '''
        Считывает звезду из файла при условии, что звезда была
        закеширована через Star.cache().
        '''
        name = str(rdf(fin))
        nummer = int(rdf(fin))
        neighbours = []
        for i in range(nummer):
            way_len = int(rdf(fin))
            way_target = int(rdf(fin))
            neighbours.append((way_len, way_target))
        nummer = int(rdf(fin))
        planets = [Planet.read_planet(fin) for i in range(nummer)]
        rez = Star(name, neighbours)
        rez.set_planets(planets)
        return rez

    def to_matrix(self, marker=None):
        '''
        Преобразовывает карту в картину, где отображены планеты и (при
        передаче его в параметры) маркер.
        '''
        temp_coords = []
        for j in self.planets:
            temp_coords.append(j.get_coordinates())
        string = ""
        for y in range(self.size_y):
            for x in range(self.size_x):
                if not marker is None and my_math.Coords(x, y) == marker:
                    string = string + MARKER
                elif my_math.Coords(x, y) in temp_coords:
                    string = string + PLANET
                else:
                    string = string + NONE
            string = string + "\n"
        return string
