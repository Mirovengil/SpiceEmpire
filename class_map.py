'''
Этот модуль содержит всё необходимое для работы с игровой картой.
'''

from class_star import Star
from my_math import rdf
from class_ship import read_ship

class GameMap:
    '''
    Класс игровой карты.
    '''
    def __init__(self):
        self.stars = []
        self.ships = []
        self.size_x = None
        self.size_y = None

    def set_size(self, size_x, size_y):
        '''
        Устанавливает размеры планетарной карты в (size_x, size_y) для
        всех звёзд на карте.
        '''
        self.size_x = size_x
        self.size_y = size_y
        if self.stars != None:
            for i in range(len(self.stars)):
                self.stars[i].setSize(self.size_x, self.size_y)

    def set_stars(self, stars):
        '''
        Подключает массив звёзд в качестве игрового созвездия к карте.
        '''
        self.stars = stars
        if not self.size_x is None:
            for i in range(len(self.stars)):
                self.stars[i].setSize(self.size_x, self.size_y)

    def set_planets(self, planets):
        '''
        Подключает двумерный массив планет к звёздам.
        '''
        if self.stars is None:
            raise ValueError("Сперва задайте звёзды, к которым будут прикрепляться планеты!1")
        for i in range(len(planets)):
            self.stars[i].setPlanets(planets[i])

    def set_ships(self, ships):
        '''
        Сеттер поля ships.
        '''
        self.ships = ships

    def add_ship(self, ship):
        '''
        Добавить Ship в ships.
        '''
        self.ships.append(ship)

    def __str__(self):
        string = "Звёзды\nummer\nummer"
        for i in self.stars:
            string = string + i.str(self.stars)
        string = string + 'Корабли\nummer'
        for i in self.ships:
            string = string + i.str(self.stars)
        return string

    def next_turn(self):
        '''
        Сделать следующий игровой ход.
        '''
        for i in range(len(self.ships)):
            if self.ships[i].get_xy() == self.ships[i].get_fly_to():
                self.ships[i].heal_self()
            self.ships[i].move()

    def cache(self):
        '''
        Кеширует карту. Использовать для реализации сохранений.
        '''
        string = ""
        string = string + str(self.size_x) + "\n"
        string = string + str(self.size_y) + "\n"
        string = string + str(len(self.stars)) + "\n"
        for i in self.stars:
            string = string + i.cache()
        string = string + str(len(self.ships)) + "\n"
        for i in self.ships:
            string = string + i.cache()
        return string

    @staticmethod
    def read_map(name):
        '''
        Считывает из файла name закешированную при помощи
        gameMap.cache() игровую карту.
        '''
        fin = open(name, 'r')
        size_x = int(rdf(fin))
        size_y = int(rdf(fin))
        nummer = int(rdf(fin))
        rez = GameMap()
        rez.set_size(size_x, size_y)
        rez.set_stars([Star.read_star(fin) for i in range(nummer)])
        nummer = int(rdf(fin))
        rez.set_ships([read_ship(fin) for i in range(nummer)])
        fin.close()
        return rez
