'''
В этом модуле можно найти всё необходимое для реализации корабля (Ship):
класс, функцию считывания.
'''

import my_math
from my_math import rdf

class Ship:
    '''
    Класс корабля.
    '''
    max_dist = {
        "fast" : 18**0.5 + 0.01,
        "medium" : 8**0.5 + 0.01,
        "low" : 2**0.5 + 0.01
    }
    classes = ['test']
    def __init__(self):
        self.x_y = my_math.Coords()
        self.system = None
        self.hp = 100 #percents
        self.img = None
        self.name = None
        self.master = None

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
        string = string + \
        "Координаты корабля: {}".format(str(self.x_y)) + "\n"
        string = string + \
        "Хозяин корабля: игрок номер {}".format(str(self.master)) + "\n"
        string = string + \
        "Корабль находится в системе {}".format(systems[self.system].get_name()) + "\n"
        #string = string + \
        #"Корабль видят игроки под номерами: {}".format(str(self.visible_to)) + "\n"
        return string

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
        ship.set_hp(hp)
        ship.set_x_y(my_math.Coords(int(x_y[0]), int(x_y[1])))
        ship.set_master(master)
        ship.set_system(system)
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
        return ship

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
