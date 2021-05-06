'''
Сий чудо-модуль содержит всё необходимое, чтобы сгенерировать игровую
карту.
'''

from random import randint

import ost_tree
import my_math
from class_planet import Planet
from class_star import Star
from class_map import GameMap
from class_ship import Ship

class GeneratorOptions:
    '''
    Класс для удобной передачи параметров генерации карты в
    generate_map и её дочерние функции.
    
    Исходные значения полей изменять можно, на своё усмотрение;
    нюансы: option.nummer < 324, потому что названий для звёзд пока
    всего 324 (можешь добавить своих); работает за
    O(option.nummer * option.nummer) -> не стоит
    делать option.nummer большим, чем sqrt(10^6): питон, всё же,
    ме-е-едленный; option.nummer * option.max_p < 196
    (названий для планет не хватит);
    '''
    def __init__(self):
        self.nummer = 10
        #кол-во систем на карте
        self.min_p = 5
        #минимальное кол-во планет в системе
        self.max_p = 10
        #максимальное кол-во планет в системе
        self.min_l = 1
        #минимальная длина пути между двумя системами
        self.max_l = 4
        #максимальная длина пути между двумя системами
        self.size_x = 20
        #размер системы по x
        self.size_y = 10
        #размер системы по у
        self.min_d = 3
        #минимальное расстояние между двумя планетами (считается Пифагором)
        self.players_number = 2
        #количество игроков (все управляются человеками)
    #Геттеры и сеттеры (сгенерированы автоматически)
    def get_nummer(self):
        '''Геттер поля nummer'''
        return self.nummer
    def set_nummer(self, value):
        '''Сеттер поля nummer'''
        self.nummer = value
    def get_min_p(self):
        '''Геттер поля min_p'''
        return self.min_p
    def set_min_p(self, value):
        '''Сеттер поля min_p'''
        self.min_p = value
    def get_max_p(self):
        '''Геттер поля max_p'''
        return self.max_p
    def set_max_p(self, value):
        '''Сеттер поля max_p'''
        self.max_p = value
    def get_min_l(self):
        '''Геттер поля min_l'''
        return self.min_l
    def set_min_l(self, value):
        '''Сеттер поля min_l'''
        self.min_l = value
    def get_max_l(self):
        '''Геттер поля max_l'''
        return self.max_l
    def set_max_l(self, value):
        '''Сеттер поля max_l'''
        self.max_l = value
    def get_size_x(self):
        '''Геттер поля size_x'''
        return self.size_x
    def set_size_x(self, value):
        '''Сеттер поля size_x'''
        self.size_x = value
    def get_size_y(self):
        '''Геттер поля size_y'''
        return self.size_y
    def set_size_y(self, value):
        '''Сеттер поля size_y'''
        self.size_y = value
    def get_min_d(self):
        '''Геттер поля min_d'''
        return self.min_d
    def set_min_d(self, value):
        '''Сеттер поля min_d'''
        self.min_d = value

def ok_xy(planets, coords, option):
    '''
    Проверяет, на достаточном ли расстоянии option.min_d от всех планет
    planets будут coords.
    '''
    for i in planets:
        if my_math.dist(coords, i.get_coordinates()) < option.get_min_d():
            return False
    return True


def get_names(place):
    '''
    Считывает список названий из файла <place>.txt и возвращает его.
    '''
    stdin = open(place, 'r')
    names = [i.replace('\n', '') for i in stdin]
    stdin.close()
    return (names, len(names))


def generate_constellation(names, names_number, option):
    '''
    Генерирует граф из n * n путей, составляет из него дерево и
    возвращает последнее.
    '''
    graph = []
    for i in range(option.get_nummer()): #Здесь создаётся звезда
        numm = randint(0, names_number - 1)
        name = names[numm]
        names[numm], names[names_number - 1] = names[names_number - 1], names[numm]
        names_number -= 1
        graph.append(Star(name, []))
    ways = []
    for i in range(option.get_nummer()):
        for j in range(option.get_nummer()):
            ways.append((randint(option.get_min_l(), option.get_max_l()), i, j))
    ways = ost_tree.build_ost_tree(option.get_nummer(), ways)
    for i in range(option.get_nummer()):
        graph[i].neighbours = ways[i]
    return graph


def generate_planets(names, names_number, option):
    '''
    Создаёт двумерный массив планет, возвращает его.
    '''
    graphs = []
    for i in range(option.get_nummer()):
        planets = []
        for j in range(randint(option.get_min_p(), option.get_max_p())): #Здесь создаётся планета
            x, y = randint(0, option.get_size_x() - 1), randint(0, option.get_size_y() - 1)
            while not ok_xy(planets, my_math.Coords(x, y), option):
                x, y = randint(0, option.get_size_x() - 1), randint(0, option.get_size_y() - 1)
            numm = randint(0, names_number - 1)
            name = names[numm]
            names[numm], names[names_number - 1] = names[names_number - 1], names[numm]
            names_number -= 1
            planets.append(Planet.new_planet(name, my_math.Coords(x, y)))
        graphs.append(planets)
    return graphs

def generate_ships(game_map, system, player, player_planet):
    '''
    Создаёт начальный набор кораблей для игрока №<player : int> и
    прикрепляет их к планете <player_planet : Planet>.
    '''

    ship_1 = Ship.new_ship('test')
    ship_1.set_master(player)
    ship_1.set_system(system)
    ship_1.set_x_y(player_planet.coordinates)

    game_map.add_ship(ship_1)

def add_players(game_map):
    '''
    Выделяет игрокам планеты и начальные корабли.
    '''
    #Массив звёзд, каждая из которых доступна для генерации.
    #Когда на любой из планет обосновался игрок, около этой
    #звезды другой игрок уже не может появиться, чтобы исключить
    #схватки уже на первых трёх-четырёх ходах.
    pst = [i[0] for i in enumerate(game_map.stars)]
    for player in range(game_map.number_of_players):
        number_of_system_in_pst = randint(0, len(pst) - 1)
        system = pst[number_of_system_in_pst]
        pst.pop(number_of_system_in_pst)
        player_planet = game_map.stars[system].planets[randint(0,\
        len(game_map.stars[system].planets) - 1)]
        player_planet.set_master(player)
        generate_ships(game_map, system, player, player_planet)
        game_map.stars[system].can_be_seen.add(player)

def generate_map(option):
    '''
    Создаёт карту с указанными параметрами.
    '''
    names, names_number = get_names('./data/stars_names.txt')
    game_map = GameMap()
    graph = generate_constellation(names, names_number, option)
    game_map.set_stars(graph)
    names, names_number = get_names('./data/planets_names.txt')
    planets = generate_planets(names, names_number, option)
    game_map.set_planets(planets)
    game_map.set_size(option.get_size_x(), option.get_size_y())
    game_map.number_of_players = option.players_number
    add_players(game_map)
    return game_map


