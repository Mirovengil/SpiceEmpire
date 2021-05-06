'''
В этом модуле можно найти всё необходимое для реализации корабля (Ship):
класс, функцию считывания.
'''

import my_math
from my_math import rdf
from class_card import CardStore

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
        string = string + 'Защита: ' + str(self.dfc) + "\n"
        string = string + \
        "Координаты корабля: {}".format(str(self.x_y)) + "\n"
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

    def move(self, card, place):
        '''
        Применяет к кораблю карточку передвижения.
        '''
        if my_math.dist(place, self.x_y) > card.mov:
            raise ValueError('''Корабль не может переместиться на
                такое расстояние!''')
        self.x_y = place

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
