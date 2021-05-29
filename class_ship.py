'''
В этом модуле можно найти всё необходимое для реализации корабля (Ship):
класс, функцию считывания.
'''

import my_math
from my_math import rdf
from class_card import CardStore

SHIPS_PARAMS = {
'test': {
                'speed' : 5,
                'limit' : 2,
                'hp' : 4
            },
'Мирный советский трактор': {
                'speed' : 3,
                'limit' : 1,
                'hp' : 2
            },
'Малютка': {
                'speed' : 5,
                'limit' : 2,
                'hp' : 4
            },
'Ракетный шаттл': {
                'speed' : 3,
                'limit' : 3,
                'hp' : 6
            },
'Бронеяхта': {
                'speed' : 2,
                'limit' : 3,
                'hp' : 8
            },
'Корвет': {
                'speed' : 6,
                'limit' : 4,
                'hp' : 7
            },
'Истребитель': {
                'speed' : 9,
                'limit' : 4,
                'hp' : 4
            },
'Броненосец': {
                'speed' : 5,
                'limit' : 5,
                'hp' : 10
            },
'Эсминец': {
                'speed' : 5,
                'limit' : 5,
                'hp' : 7
            },
'Канонерка': {
                'speed' : 4,
                'limit' : 2,
                'hp' : 4
            },
'Дредноут': {
                'speed' : 4,
                'limit' : 5,
                'hp' : 5
            }
}

fleet_index = 0
def generate_fleet_index():
    '''
    Создаёт уникальный номер для флота.
    '''
    global fleet_index
    answer = fleet_index
    fleet_index += 1
    return answer

class Ship:
    '''
    Класс корабля.
    '''
    def __init__(self):
        self.x_y = my_math.Coords()
        self.system = None
        self.img = None
        self.name = None
        self.master = None
        self.card_store = CardStore()
        self.speed = None
        self.limit = None
        self.fleet = None
        #Следующие параметры не сохраняются, так как появляются только на время боя,
        #а положение внутри боя не сохраняется (в "Героев" играли?).
        self.battle_x_y = None
        self.dfc = None
        self.hp = None
        self.is_available = None
        self.can_move_in_battle = 0
    def is_live(self):
        '''
        Возвращает, жив ли корабль.
        '''
        return self.hp > 0

    def is_died(self):
        '''
        Возвращает, мёртв ли корабль.
        '''
        return not self.is_live()

    def str(self, systems):
        '''Записывает данные о корабле в строковом виде. Использовать
        для логгирования или для ASCII-графики.'''
        string = ""
        string = string + \
        "Тип корабля: {}".format(self.name) + "\n"
        string = string + 'Занимает лимитов: ' + str(self.limit) + '\n'
        string = string + 'Единиц перемещения: ' + str(self.speed) + "\n"
        string = string + \
        "Координаты корабля: ({}, {})".format(self.x_y.x + 1, self.x_y.y + 1) + "\n"
        string = string + \
        "Хозяин корабля: игрок номер {}".format(str(self.master)) + "\n"
        string = string + \
        "Корабль находится в системе {}".format(systems[self.system].get_name()) + "\n"
        #string = string + str(self.card_store)
        #string = string + \
        #"Корабль видят игроки под номерами: {}".format(str(self.visible_to)) + "\n"
        return string

    def battle_str(self):
        '''
        Выводит информацию, которая влияет на ход сражения, о корабле.
        Записывает данные о корабле в строковом виде. Использовать
        для логгирования или для ASCII-графики.
        '''
        string = ""
        string = string + \
        "Тип корабля: {}".format(self.name) + "\n"
        string = string + \
        "Хозяин корабля: игрок номер {}".format(str(self.master)) + "\n"
        string = string + "HP: " + str(self.hp) + "\n"
        string = string + "Защита корабля: " + str(self.dfc) +\
        (' (НЕ ЗАЩИЩАЕТСЯ)' if self.dfc == 0 else '') + "\n"
        string = string + "Карточки: " + "\n"
        for card in enumerate(self.card_store.cards):
            string = string + str(card[0] + 1) + ". " + card[1].tit + '\n'
        return string

    def restore_card(self):
        '''
        Восстанавливает ту карточку корабля, которая имеет наибольший приоритет.
        '''
        self.card_store.restore_card()

    def cache(self):
        '''
        Кеширует корабль. Необходимо для реализации сохранений.
        '''
        string = ""
        string = string + self.name + "\n"
        string = string + str(self.x_y) + "\n"
        string = string + str(self.master) + "\n"
        string = string + str(self.system) + "\n"
        string = string + self.card_store.cache()
        string = string + str(self.fleet) + "\n"
        return string

    @staticmethod
    def read_ship(fin):
        '''
        Считывает корабль, который был захеширован через Ship.cache(),
        из файла fin.
        '''
        ship = Ship()
        ship.set_name(rdf(fin))
        x_y = rdf(fin).replace(")", "").replace("(", "").split(", ")
        master = int(rdf(fin))
        system = int(rdf(fin))
        card_store = CardStore.load(fin)
        ship.set_x_y(my_math.Coords(int(x_y[0]), int(x_y[1])))
        ship.set_master(master)
        ship.set_system(system)
        ship.card_store = card_store
        ship.speed = SHIPS_PARAMS[ship.name]['speed']
        ship.limit = SHIPS_PARAMS[ship.name]['limit']
        ship.set_img('./img/' + ship.name + '.img')
        ship.fleet = int(rdf(fin))
        return ship

    @staticmethod
    def new_ship(class_of_ship):
        '''
        Создаёт готовый корабль, подгружает картинку.
        '''
        ship = Ship()
        ship.set_hp(SHIPS_PARAMS[class_of_ship]['hp'])
        ship.set_name(class_of_ship)
        ship.set_img('./img/' + class_of_ship + '.img')
        ship.card_store = CardStore(class_of_ship)
        ship.speed = SHIPS_PARAMS[class_of_ship]['speed']
        ship.limit = SHIPS_PARAMS[class_of_ship]['limit']
        ship.fleet = generate_fleet_index()
        return ship

    def attack(self, card, enemy):
        '''
        Применяет к кораблю карточку атаки.
        Корабль self наносит урон кораблю enemy.
        Из величины урона вычитается защита противника.
        Естественно, ухода в минус быть не может.
        '''
        enemy.hp -= max(card.dmg - enemy.dfc, 0)

    def defence(self, card, stub):
        '''
        Применяет к кораблю карточку защиты.
        '''
        self.dfc += card.dfc

    def move_on_global_map(self, place):
        '''
        Перемещает корабль на глобальной карте, расходуя единицы перемещения.
        '''
        if my_math.dist(self.x_y, place) > self.speed:
            raise ValueError('Вы не можете переместиться так далеко!')
        self.speed = int(self.speed - my_math.dist(self.x_y, place))
        self.x_y = place

    def on_side(self, game_map):
        '''
        Возвращает True, если корабль может совершить прыжок в другую систему.
        '''
        min_x = 0
        max_x = game_map.size_x - 1
        min_y = 0
        max_y = game_map.size_y - 1
        on_vertical_border = (self.x_y.x == min_x or self.x_y.x == max_x)
        on_horizontal_border = (self.x_y.y == min_y or self.x_y.y == max_y)
        return on_vertical_border or on_horizontal_border

    def restore_speed(self):
        '''
        Восстанавливает единицы перемещения корабля.
        '''
        self.speed = SHIPS_PARAMS[self.name]['speed']

    def move(self, card, stub):
        '''
        Применяет к кораблю карточку передвижения.
        Используется на поле боя.
        Выдаёт кораблю очки на перемещение по боевой карте.
        '''
        self.can_move_in_battle = card.mov

    def use_fuel(self):
        '''
        Расходует единицу перемещения у корабля.
        Используется только на боевой карте.
        '''
        self.can_move_in_battle -= 1
        if self.can_move_in_battle < 0:
            self.can_move_in_battle = 0

    def can_move_on_battle_map(self):
        '''
        Возвращает True, если корабль может совершать перемещение на боевой
        карте.
        Метод необходим для реализации интерфейса в АСКИ.
        '''
        return self.can_move_in_battle > 0

    def use(self, index, act, param):
        '''
        Применяет к кораблю карточку.
        '''
        action = {
            'attack' : Ship.attack,
            'defence' : Ship.defence,
            'move' : Ship.move
        }
        if not act in action:
            raise ValueError('Недопустимое действие с карточки!!11')
        usable_card = self.card_store.use(index)
        action[act](self, usable_card, param)

    #Геттеры и сеттеры (сгенерированы автоматически)
    def get_x_y(self):
        '''Геттер поля x_y'''
        return self.x_y
    def set_x_y(self, value):
        '''Сеттер поля x_y'''
        self.x_y = value
    def get_system(self):
        '''Геттер поля system'''
        return self.system
    def set_system(self, value):
        '''Сеттер поля system'''
        self.system = value
    def get_hp(self):
        '''Геттер поля hp'''
        return self.hp
    def set_hp(self, value):
        '''Сеттер поля hp'''
        self.hp = value
    def get_img(self):
        '''Геттер поля img'''
        return self.img
    def set_img(self, value):
        '''Сеттер поля img'''
        self.img = value
    def get_name(self):
        '''Геттер поля name'''
        return self.name
    def set_name(self, value):
        '''Сеттер поля name'''
        self.name = value
    def get_master(self):
        '''Геттер поля master'''
        return self.master
    def set_master(self, value):
        '''Сеттер поля master'''
        self.master = value

    def has_full_fuel(self):
        '''
        Возвращает True, если корабль полностью заправлен.
        '''
        return self.speed == SHIPS_PARAMS[self.name]['speed']

    def battle_mode_on(self):
        '''
        Переводит корабль в боевой режим: задаёт боевые характеристики.
        '''
        self.hp = SHIPS_PARAMS[self.name]['hp']
        self.dfc = 0
        self.is_available = True
    
    def battle_mode_off(self):
        '''
        Выводит корабль из боевого режима: удаляет боевые характеристики.
        Не знаю, на кой она нужна, но пусть пока будет _/=(*~*)=\_.
        '''
        self.hp = None
        self.dfc = None
        self.is_available = False

class Fleet:
    '''
    Класс флота, состоящего из кораблей.
    Поля:
        ships : [Ship] -- массив кораблей, из которых состоит флот.
        x_y : Coords -- местонахождение флота.
        master : int -- игрок, который может управлять флотом.
        system : int -- номер системы, в которой находится флот.
        index : int -- порядковый номер флота, который используется для
        объединения кораблей в, собственно, флоты.
    '''
    def __init__(self, ship):
        '''
        ship : Ship -- корабль, который является "основой" флота.
        Остальные следует добавлять / отсоединять.
        Так как флотов не может быть больше, чем кораблей, то такая система вполне
        жизнеспособна (мне нравится).
        '''
        self.ships = [ship]
        self.x_y = ship.x_y
        self.master = ship.master
        self.system = ship.system
        self.index = ship.fleet

    def move(self, place):
        '''
        Перемещает все корабли флота в позицию place : Coords.
        '''
        ship = 0
        while ship < len(self.ships):
            self.ships[ship].move_on_global_map(place)
            ship += 1
        self.x_y = place

    def set_system(self, value):
        '''
        Перемещает все корабли флота в систему value : int.
        '''
        ship = 0
        while ship < len(self.ships):
            self.ships[ship].set_system(value)
            ship += 1
        self.system = value

    def size(self):
        '''
        Возвращает количество : int кораблей во флоте.
        '''
        return len(self.ships)

    def add_ship(self, ship):
        '''
        Добавляет корабль ship : Ship во флот, если это возможно.
        '''
        if self.x_y != ship.x_y:
            raise BaseException('''Корабль корабль нельзя присоединить ко флоту, если
            они имеют разные координаты!''')
        if self.system != ship.system:
            raise BaseException('''Корабль корабль нельзя присоединить ко флоту, если
            они находятся в разных системах!''')
        if self.master != ship.master:
            raise BaseException('''Нельзя добавлять чужой корабль в свой флот!
            И вообще, почему не началась битва!!??''')
        ship.fleet = self.index
        self.ships.append(ship)

    def remove_ship(self, ship_index):
        '''
        Переводит корабль ship_index : int в новый, свежесозданный флот из одного корабля.
        '''
        self.ships[ship_index].fleet = generate_fleet_index()
        self.ships.pop(ship_index)

    @staticmethod
    def merge_two_different_fleets(first, second):
        '''
        Объединяет два флота: first : Fleet и second : Fleet.
        При этом, новому флоту присваивается индекс того, который больше по размеру.
        Также все корабли меньшего флота переводятся в большой.
        Это сделано для того, чтобы избежать ситуации, когда при объединении флота
        из одного корабля и флота из сотни кораблей, вместо добавления одной операции
        по добавлению элемента в массив, будут произведены сотни. (НАГЛЯДНЫЙ
        ПРИМЕР это, а не вода в комментариях для увеличения кол-ва строчек кода).
        '''
        if first.x_y != second.x_y:
            raise BaseException('Нельзя объединять флоты, находящиеся на разных клетках!')
        if first.system != second.system:
            raise BaseException('Нельзя объединять флоты, находящиеся в разных системах!')
        if first.master != second.master:
            raise BaseException('''Нельзя объединить флоты разных игроков! Да
            и как они вообще оказались на одной клетке, не вступив в бой!!??''')
        if first.index == second.index:
            raise BaseException('''Капитан болен шизофренией и пытается объединить
            свой флот со своим же!''')
        if first.size() < second.size():
            first, second = second, first
        for ship in second.ships:
            ship.fleet = first.index
            first.ships.append(ship)
        del second

    def has_full_fuel(self):
        '''
        Возвращает True, если все корабли во флоте имеют полный бак топлива.
        '''
        for ship in self.ships:
            if not ship.has_full_fuel():
                return False
        return True

    def is_on_side(self, game_map):
        '''
        Возвращает True, если все корабли флота находятся на краю
        карты game_map : GameMap.
        '''
        for ship in self.ships:
            if not ship.on_side(game_map):
                return False
        return True

class ShipsShop:
    '''
    Класс, отвечающий за покупку кораблей.
    Гарантирует корректное распределение "лимит/покупка" и
    выбор корректного класса корабля. 
    points : int -- количество единиц чего-то-там ("лимитов") для
    закупки корабля.
    ships : [str] -- список кораблей, которые предполагается купить.
    '''
    SHIPS_LIST = [
        'Мирный советский трактор'
        'Малютка',
        'Ракетный шаттл',
        'Бронеяхта',
        'Корвет',
        'Истребитель',
        'Броненосец',
        'Эсминец',
        'Канонерка',
        'Дредноут'
    ]
    CANT_BUY = 'НИЧЕГО'
    
    def __init__(self, profit, max_limit, player):
        '''
        profit : int -- кол-во очков для закупки кораблей, пришедшее на очередном ходе.
        max_limit : int -- кол-во очков, которые доступны игроку (зависит от количества планет,
        находящихся в его распоряжении).
        player : int -- номер игрока, который использует класс для покупки кораблей.
        '''
        available_points = min(max_limit - profit, profit)
        self.available_points = available_points
        self.ships = []
        self.player = player

    def get_available_points(self):
        '''
        Возвращает в виде строки (str) количество доступных для закупки очков.
        '''
        if self.available_points > 0:
            return str(self.available_points)
        return ShipsShop.CANT_BUY


    def get_available_ships(self):
        '''
        Возвращает список типов кораблей ( [str] ), которые могут быть куплены
        на имеющуюся сумму.
        '''
        list_of_available_ships = []
        for ship in ShipsShop.SHIPS_LIST:
            if SHIPS_PARAMS[ship]['limit'] <= self.available_points:
                list_of_available_ships.append({
                'ship': ship,
                'cost': SHIPS_PARAMS[ship]['limit']
                })
        return list_of_available_ships

    def add_ship_to_list(self, ship, system, planet):
        '''
        Добавляет корабль ship : str в список покупок с учётом планеты planet : Planet и
        системы system : int, где тот будет покупаться. 
        '''
        if not ship in SHIPS_PARAMS:
            raise ValueError('Вы пытаетесь купить несуществующий корабль!')
        if SHIPS_PARAMS[ship]['limit']  > self.available_points:
            raise ValueError('Вы пытаетесь купить слишком дорогой корабль!')
        self.available_points -= SHIPS_PARAMS[ship]['limit'] 
        ship = {
            'ship' : ship,
            'system' : system,
            'planet' : planet
        }
        self.ships.append(ship)

    def remove_ship_from_list(self, ship_index):
        '''
        Удаляет корабль под номером ship_index : int из "списка покупок".
        '''
        if ship_index < 0 or ship_index >= len(self.ships):
            raise ValueError('Вы пытаетесь удалить корабль, которого нет в списке покупок!')
        self.available_points += SHIPS_PARAMS[self.ships[ship_index]['ship']]['limit'] 
        self.ships.pop(ship_index)

    def buy_ships(self):
        '''
        Возвращает список купленных кораблей [Ship].
        Предполагается, что после этого действия объект класса удаляется.
        '''
        ships_list = []
        for ship in self.ships:
            new_ship = Ship.new_ship(ship['ship'])
            new_ship.system = ship['system']
            new_ship.x_y = ship['planet'].coordinates
            new_ship.master = self.player
            ships_list.append(new_ship)
        return ships_list

    
    #Осторожно, дальше начинается быдлокод.
    def __str__(self):
        '''
        Возвращает строку, которая являет собой представление информации о списке
        заказанных к покупке кораблей.
        Использовать для логгирования и/или реализации интерфейса в ASCII.
        '''
        string = ""
        for ship in enumerate(self.ships):
            string = string + str(ship[0] + 1) + ". " + ship[1]['ship'] + " (появится на"\
            + " планете " + ship[1]['planet'].name + ")\n"
        string = (string if string != "" else "НИЧЕГО ВЫ НЕ ЗАКАЗЫВАЛИ!")
        return string

    @staticmethod
    def get_planet_by_pair(pair, game_map):
        '''
        Возвращает планету : Planet, которая описана парой pair :
            'planet' : int -- индекс планеты.
            'system' : int -- индекс системы, где находится оная планета.
        Работает корректно при условии, что планета находится на карте game_map : GameMap.
        '''
        star_index = pair['system']
        planet_index = pair['planet']
        return game_map.stars[star_index].planets[planet_index]
