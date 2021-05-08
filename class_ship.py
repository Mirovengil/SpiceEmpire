'''
В этом модуле можно найти всё необходимое для реализации корабля (Ship):
класс, функцию считывания.
'''

import my_math
from my_math import rdf
from class_card import CardStore

SHIPS_PARAMS = {
'test' : {
                'speed' : 5,
                'limit' : 2
            }
}

class Ship:
    '''
    Класс корабля.
    '''
    classes = ['test']
    def __init__(self):
        self.x_y = my_math.Coords()
        self.system = None
        self.hp = 100 #percents
        self.img = None
        self.name = None
        self.master = None
        self.card_store = CardStore()
        self.dfc = float(0)
        self.speed = None
        self.limit = None

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
        string = string + \
        'HP: {}'.format(str(self.hp)) + "\n"
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
        string = string + str(self.hp) + "\n"
        string = string + str(self.x_y) + "\n"
        string = string + str(self.master) + "\n"
        string = string + str(self.system) + "\n"
        string = string + self.card_store.cache()
        string = string + str(self.dfc) + "\n"
        return string

    @staticmethod
    def read_ship(fin):
        '''
        Считывает корабль, который был захеширован через Ship.cache(),
        из файла fin.
        '''
        ship = Ship()
        ship.set_name(rdf(fin))
        hp = int(rdf(fin))
        x_y = rdf(fin).replace(")", "").replace("(", "").split(", ")
        master = int(rdf(fin))
        system = int(rdf(fin))
        card_store = CardStore.load(fin)
        ship.dfc = float(rdf(fin))
        ship.set_hp(hp)
        ship.set_x_y(my_math.Coords(int(x_y[0]), int(x_y[1])))
        ship.set_master(master)
        ship.set_system(system)
        ship.card_store = card_store
        ship.speed = SHIPS_PARAMS[self.name]['speed']
        ship.limit = SHIPS_PARAMS[self.name]['limit']
        return ship

    @staticmethod
    def new_ship(class_of_ship):
        '''
        Создаёт готовый корабль, подгружает картинку.
        '''
        if not class_of_ship in Ship.classes:
            raise ValueError('Корабль несуществующего типа!11')
        ship = Ship()
        ship.set_hp(100)
        ship.set_name(class_of_ship)
        ship.set_img('./img/' + class_of_ship + '.img')
        ship.card_store = CardStore(class_of_ship)
        ship.speed = SHIPS_PARAMS[class_of_ship]['speed']
        ship.limit = SHIPS_PARAMS[class_of_ship]['limit']
        return ship

    def attack(self, card, enemy):
        '''
        Применяет к кораблю карточку атаки.
        Корабль self наносит урон кораблю enemy.
        '''
        enemy.hp -= card.dmg

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
        max_x = game_map.size_x
        min_y = 0
        max_y = game_map.size_y
        on_vertical_border = (self.x_y.x == min_x or self.x_y.x == max_x)
        on_horizontal_border = (self.x_y.y == min_y or self.x_y.y == max_y)
        return on_vertical_border or on_horizontal_border

    def restore_speed(self):
        '''
        Восстанавливает единицы перемещения корабля.
        '''
        self.speed = SHIPS_PARAMS[self.name]['speed']

    def move(self, card, place):
        '''
        Применяет к кораблю карточку передвижения.
        Используется на поле боя.
        '''
        raise ValueError('Функцию придётся переписывать!')

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
