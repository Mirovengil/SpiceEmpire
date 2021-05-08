'''
Этот модуль содержит всё необходимое для работы с игровой картой.
'''

from class_star import Star
from my_math import rdf
from class_ship import Ship
import class_ships_shop

class GameMap:
    '''
    Класс игровой карты.
    '''

    def __init__(self):
        self.stars = []
        self.ships = []
        self.size_x = None
        self.size_y = None
        self.number_of_players = None
        self.player = 0
        self.option = None
        self.turn = 0
        self.limits = []

    def set_size(self, size_x, size_y):
        '''
        Устанавливает размеры планетарной карты в (size_x, size_y) для
        всех звёзд на карте.
        '''
        self.size_x = size_x
        self.size_y = size_y
        if self.stars != None:
            for i in range(len(self.stars)):
                self.stars[i].set_size(self.size_x, self.size_y)

    def set_stars(self, stars):
        '''
        Подключает массив звёзд в качестве игрового созвездия к карте.
        '''
        self.stars = stars
        if not self.size_x is None:
            for i in range(len(self.stars)):
                self.stars[i].set_size(self.size_x, self.size_y)

    def set_planets(self, planets):
        '''
        Подключает двумерный массив планет к звёздам.
        '''
        if self.stars is None:
            raise ValueError("Сперва задайте звёзды, к которым будут прикрепляться планеты!1")
        for i in range(len(planets)):
            self.stars[i].set_planets(planets[i])

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
        string = "Звёзды\n"
        for i in self.stars:
            string = string + i.str(self.stars)
        string = string + 'Корабли\n'
        for i in self.ships:
            string = string + i.str(self.stars)
        return string

    def next_turn(self):
        '''
        Сделать следующий игровой ход.
        Ход переходит к следующему игроку.
        Обновляется видимость (т.н. "Туман войны") для игроков.
        Вернуть, не закончилась ли игра.
        Если круг хождения завершился.
        Перейти к первому игроку.
        Разрешить всем кораблям двигаться.
        Обновить состояние лимитов игроков.
        '''
        #10.
        self.player = self.player + 1
        #20.
        self.refresh_war_thunder()
        if self.player == self.number_of_players:
            self.player = 0
            class_ships_shop.add_limits(self)
            ship = 0
            while ship < len(self.ships):
                self.ships[ship].restore_speed()
                ship += 1
        #30.
        return self.check_to_finish()
        
    def check_to_finish(self):
        '''
        Если игра закончилась, возвращает True.
        Игра заканчивается, если остаются корабли только одного игрока.
        '''
        i = 0
        while i + 1 < len(self.ships):
            if self.ships[i].master != self.ships[i + 1].master:
                return False
        return True

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
        string = string + str(self.player) + "\n"
        string = string + str(self.number_of_players) + "\n"
        return string

    def refresh_war_thunder(self):
        '''
        Обновляет зоны видимости (т.н. "туман войны") для всех игроков
        '''
        star = 0
        while star < len(self.stars):
            self.stars[star].can_be_seen = set()
            star += 1
        ship = 0
        while ship < len(self.ships):
            self.stars[self.ships[ship].system].can_be_seen.add(self.ships[ship].master)
            ship += 1

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
        rez.set_ships([Ship.read_ship(fin) for i in range(nummer)])
        rez.player = int(rdf(fin))
        rez.number_of_players = int(rdf(fin))
        fin.close()
        return rez
