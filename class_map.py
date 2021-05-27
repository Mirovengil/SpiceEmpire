'''
Этот модуль содержит всё необходимое для работы с игровой картой.
'''

from class_star import Star
from my_math import rdf
from class_ship import Ship
import class_ship
from battle_map import BattleMap
import class_planet
import random

class GameMap:
    '''
    Класс игровой карты.
    '''
    chance_of_profit = 100
    def __init__(self):
        self.stars = []
        self.ships = []
        self.fleets = []
        self.size_x = None
        self.size_y = None
        self.number_of_players = None
        self.player = 0
        self.option = None
        self.turn = 0
        self.limits = []
        self.battle_is_on = False
        self.battle_map = None
        self.profit = None

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
        Если необходимо, выдать игрокам карточки кораблей.
        '''
        self.player = self.player + 1
        self.refresh_war_thunder()
        if self.player == self.number_of_players:
            self.player = 0
            self.refresh_limits()
            self.refresh_ships_speeds()
            self.try_to_get_profit()
        return self.check_to_finish()

    def refresh_ships_speeds(self):
        '''
        Восстанавливает всем кораблям скорости перемещения.
        '''
        ship = 0
        while ship < len(self.ships):
            self.ships[ship].restore_speed()
            ship += 1

    def move_ship_to_system(self, ship_index, system_index):
        '''
        Перемещает корабль под номером ship_index : int в систему номером system_index : int.
        '''
        if not self.ships[ship_index].has_full_fuel():
            raise ValueError('Корабль должен зарядить двигатели полностью!')
        #В массиве соседей ищется та звезда, куда летит корабль; берётся длина пути до неё.
        #И по прилёте корабль будет бездействовать эту же величину.
        self.ships[ship_index].system =\
        Star.get_neighbour(self.stars[self.ships[ship_index].system].neighbours[system_index])
        self.refresh_war_thunder()
        #Корабль мог прилететь в клетку, где стоит противник. Это надо обработать.
        self.try_to_battle(ship_index)

    def get_ships_star(self, ship_index):
        '''
        Возвращает номер звезды, около которой находится корабль под
        номером ship_index : int.
        '''
        return self.ships[ship_index].system

    def check_to_finish(self):
        '''
        Если игра закончилась, возвращает True.
        Игра заканчивается, если остаются планеты только одного игрока.
        '''
        players = set()
        for star in self.stars:
            for planet in star.planets:
                if not planet.is_neitral():
                    players.add(planet.master)
        return len(players) == 1

    def get_winner(self):
        '''
        Возвращает номер игрока победителя.
        Если игра ещё не закончилась, роняет исключение (для соответствия логике и
        чтобы никто не вздумал узнавать победителя до конца игры, а то это уже
        какой-то договорной матч получается).
        '''
        if not self.check_to_finish():
            raise BaseException('''Здесь вам не футбол! Нельзя получить победителя, если
            игра ещё не закончилась!!1''')
        for star in self.stars:
            for planet in star.planets:
                if not planet.is_neitral():
                    return planet.master

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

    def refresh_limits(self):
        '''
        Обновляет количество доступных игроку лимитов.
        '''
        self.limits = [0 for i in range(self.number_of_players)]
        star = 0
        while star < len(self.stars):
            planet = 0
            while planet < len(self.stars[star].planets):
                if not self.stars[star].planets[planet].is_neitral():
                    self.limits[self.stars[star].planets[planet].master] +=\
                    self.stars[star].planets[planet].limits[class_planet.Planet.LIM_SIZE]
                planet += 1
            star += 1
        ship = 0
        while ship < len(self.ships):
            self.limits[self.ships[ship].master] -= self.ships[ship].limit
            ship += 1

    def move_ship_on_global_map(self, ship, place):
        '''
        Выполняет некоторые проверки, после чего перемещает корабль ship : Ship в клетку
        place : Coords той системы, где он сейчас находится.
        '''
        if self.ships[ship].master != self.player:
            raise ValueError('Вы не можете управлять чужим кораблём!!')
        if place.x < 0 or place.x >= self.size_x or place.y < 0 or place.y >= self.size_y:
            raise ValueError('Координаты точки должны находиться в пределах системы!!11')
        self.ships[ship].move_on_global_map(place)
        #Корабль мог переместиться в клетку с противником. Этот случай надо обработать.
        self.try_to_battle(ship)

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
        rez.refresh_limits()
        rez.refresh_war_thunder()
        return rez

    def try_to_battle(self, ship_index):
        '''
        На вход принимает ship_index : int -- номер корабля, который совершил какое-либо
        перемещение на глобальной карте. Это сделано во избежание O(n * n), где n -- сумма
        кораблей у всех игроков. Реализация же за O(n) гораздо жизнеспособнее (потому что до
        n = 10 ** 5 работает практически неощутимо моментально, а такое количество кораблей
        на поле уже невозможно физически (гарантируют правила игры).
        Если на карте нет ситуации, когда корабли РАЗНЫХ игроков находятся в одной клетке, то
        ничего  интересного функция не совершает.
        Если же такая ситуация сложилась, то она переводит игру в режим битвы и создаёт поле
        для сражения.
        '''
        ships_must_be_in_battle = []
        for ship in self.ships:
            if ship.x_y == self.ships[ship_index].x_y and\
            ship.system == self.ships[ship_index].system:
                ships_must_be_in_battle.append(ship)
        ship = 0
        while ship < len(ships_must_be_in_battle):
            if ships_must_be_in_battle[ship].master != self.player:
                #Начинается битва.
                self.battle_is_on = True
                self.battle_map = BattleMap(ships_must_be_in_battle)
                return 0
            ship += 1

    def try_to_finish_battle(self):
        '''
        Если бой окончен, то self.battle_map хранит номер победителя (необходимо для
        интерфеса), а self.battle_is_on -- ложь.
        Также, если бой окончен, то должен обновиться список кораблей (кто-то из участников
        битвы погиб, раз последняя закончилась).
        '''
        if self.battle_is_on and self.battle_map.is_finished() != -1:
            self.battle_is_on = False
            self.battle_map = self.battle_map.is_finished()
            self.refresh_list_of_ships()
            self.refresh_war_thunder()

    def refresh_list_of_ships(self):
        '''
        Обновляет список кораблей, участвующих в игре.
        Если кто-то погиб, то он удаляется из оного списка.
        Также все корабли выводятся из боевого режима.
        '''
        new_ships_list = []
        for ship in self.ships:
            if ship.is_live():
                ship.battle_mode_off()
                new_ships_list.append(ship)
        self.ships = new_ships_list

    def ship_can_move_on_battle_map(self, ship_index):
        '''
        Возвращает истину, если корабль под индексом ship_index : int v
        '''
        return self.ships[ship_index].can_move_on_battle_map()

    def start_ships_moving(self, ship_index, card_index):
        '''
        Выдаёт кораблю очки на перемещение по боевой карте (берутся из
        карточки свойств под индексом card_index : int корабля под индексом ship_index : int).
        '''
        self.ships[ship_index].use(card_index, 'move', None)

    def move_ship_on_battle_map(self, ship_index, place):
        '''
        Перемещает корабль ship_index в позицию places, eсли это возможно.
        Всё происходит на боевой kарте и при условии, что бой начался.
        '''
        if not self.battle_is_on:
            raise BaseException('''Бой не начат, поэтому нельзя переместить корабль на
            боевой карте!''')
        if not place in self.battle_map.get_possible(self.ships[ship_index].battle_x_y,\
        self.ships[ship_index].can_move_in_battle):
            raise BaseException('''Вы не можете переместиться на данный гекс!''')
        self.ships[ship_index].battle_x_y = place
        self.ships[ship_index].use_fuel()

    def battle_index_from_usable_to_real(self, index):
        '''
        Приводит корабль, который находится в массиве self.battle_map.usable_ships()
        '''
        cnt = 0
        ship = 0
        while ship < len(self.battle_map.ships):
            if self.battle_map.ships[ship].master == self.battle_map.player_turns_now() and\
            self.battle_map.ships[ship].is_available:
                if cnt == index:
                    return ship
                cnt += 1
            ship += 1

    def show_attack_distance(self, ship_index, card_index):
        '''
        Возвращает в формате str боевое поле, где отмечена дальность атаки
        корабля ship_index : int, если он собирается атаковать через карточку
        card_index : int.
        '''
        return self.battle_map.str(ship_index, self.ships[ship_index].card_store.cards[card_index].dst)

    def try_to_attack(self, ship_index, card_index, enemy_object):
        '''
        Пытается атаковать кораблём с индексом ship_index : int при помощи карточки
        с индексом card_index : int корабль противника enemy_object.
        Выполняются проверки на:
            Принадлежность обоих кораблей одному игроку.
            Нахождение противника в пределах досягаемости.
        '''
        if self.ships[ship_index].master == enemy_object.master:
            raise BaseException('Какой-то душевнобольной атакует своих!!1')
        if not enemy_object.battle_x_y in self.battle_map.get_possible(\
        self.ships[ship_index].battle_x_y, self.ships[ship_index].card_store.cards[card_index].dst):
            raise BaseException('Дальности атаки не хватает!')
        self.ships[ship_index].use(card_index, 'attack', enemy_object)

    def get_limits_of_now_player(self):
        '''
        Возвращает количество лимитов, доступных данному игроку.
        '''
        return self.limits[self.player]
    
    def try_to_get_profit(self):
        '''
        При помощи корейской случайности определяет, необходимо ли
        выдать игрокам лимиты, и определяет величину выдаваемого (если надо).
        '''
        chance = random.randint(0, 100)
        if chance > GameMap.chance_of_profit:
            self.profit = 0
        else:
            self.profit = 5


    def get_players_planets(self):
        '''
        Возвращает список планет, принадлежащих игроку, который сейчас совершает
        ход, в следующем виде:
        'planet' : int -- индекс планеты, принадлежаещей игроку.
        'system' : int -- индекс системы, где находится оная планета.
        '''
        planets = []
        star = 0
        while star < len(self.stars):
            planet = 0
            while planet < len(self.stars[star].planets):
                if self.stars[star].planets[planet].master == self.player:
                    planets.append({
                        'planet': planet,
                        'system': star
                    })
                planet += 1
            star += 1
        return planets

    def get_players_planet_by_id(self, index):
        '''
        Возвращает планету, которая находится на месте index : int в списке планет игрока,
        который возвращается при помощи метода get_players_planets : [{
            'planet' : int,
            'system' : int
        }].
        '''
        planet_index = self.get_players_planets()[index]['planet']
        star_index = self.get_players_planets()[index]['system']
        return self.stars[star_index].planets[planet_index]

    def add_ships(self, list_of_ships):
        '''
        Добавляет корабли из списка list_of_ships : [Ship] в игру.
        '''
        for ship in list_of_ships:
            self.ships.append(ship)
        self.refresh_limits()
        self.refresh_war_thunder()

    def refresh_fleets(self):
        '''
        Обновляет информацию о флотах в игре (корабль мог погибнуть, корабль мог
        переместиться поотдельности от флота и т.п.).
        '''
        fleets = dict()
        ship = 0
        while ship < len(self.ships):
            if not self.ships[ship].fleet in fleets:
                fleets[self.ships[ship].fleet] = class_ship.Fleet(self.ships[ship])
            else:
                fleets[self.ships[ship].fleet].add_ship(self.ships[ship])
            ship += 1
        self.fleets = []
        ship = 0
        while ship < len(self.ships):
            self.fleets.append(fleets[self.ships[ship].fleet])
            ship += 1

    def get_fleets_of_player(self):
        '''
        Возвращает массив : [Fleet], который содержит флоты того, кто сейчас ходит.
        '''
        fleets = []
        for fleet in self.fleets:
            if fleet.master == self.player:
                fleets.append(fleet)
        return fleets
