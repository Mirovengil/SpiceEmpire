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

    def __init__(self):
        self.cost = None
        self.heal = None
        self.x_y = my_math.Coords()
        self.system = None
        self.fly_to = my_math.Coords()
        self.hp = 100 #percents
        self.damage = None
        self.defence = None
        self.img = None
        self.speed = None
        self.name = None #name of ship's type
        self.visible_to = []
        self.master = None

    def set_target(self, target):
        '''
        Выставляет кораблю место для перемещения.
        '''
        if my_math.dist(self.x_y, target) < self.speed:
            self.fly_to = target
            return True
        return False

    def move(self):
        '''
        Перемещает корабль в точку, которую надо задать через set_target.
        '''
        self.x_y = self.fly_to

    def add_visible_to(self, value):
        '''
        Делает корабль видимым для игрока value.
        '''
        self.visible_to.append(value)

    def heal_self(self):
        '''
        Лечит корабль, если это возможно.
        '''
        self.hp += self.heal
        if self.hp > 100:
            self.hp = 100

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
        "Корабль летит в: {}".format(str(self.fly_to)) + "\n"
        string = string + \
        "Хозяин корабля: игрок номер {}".format(str(self.master)) + "\n"
        string = string + \
        "Корабль находится в системе {}".format(systems[self.system].getName()) + "\n"
        string = string + \
        "Корабль видят игроки под номерами: {}".format(str(self.visible_to)) + "\n"
        return string

    def cache(self):
        '''
        Кеширует корабль. Необходимо для реализации сохранений.
        '''
        string = ""
        string = string + self.name + "\n"
        string = string + str(self.hp) + "\n"
        string = string + str(self.x_y) + "\n"
        string = string + str(self.fly_to) + "\n"
        string = string + str(self.master) + "\n"
        string = string + str(self.system) + "\n"
        string = string + str(len(self.visible_to)) + "\n"
        for i in self.visible_to:
            string = string + str(i) + "\n"
        return string
    #Геттеры и сеттеры (сгенерированы автоматически)
    def get_cost(self):
        '''Геттер поля cost'''
        return self.cost
    def set_cost(self, value):
        '''Сеттер поля cost'''
        self.cost = value
    def get_heal(self):
        '''Геттер поля heal'''
        return self.heal
    def set_heal(self, value):
        '''Сеттер поля heal'''
        self.heal = value
    def get_xy(self):
        '''Геттер поля x_y'''
        return self.x_y
    def set_xy(self, value):
        '''Сеттер поля x_y'''
        self.x_y = value
    def get_system(self):
        '''Геттер поля system'''
        return self.system
    def set_system(self, value):
        '''Сеттер поля system'''
        self.system = value
    def get_fly_to(self):
        '''Геттер поля fly_to'''
        return self.fly_to
    def set_fly_to(self, value):
        '''Сеттер поля fly_to'''
        self.fly_to = value
    def get_hp(self):
        '''Геттер поля hp'''
        return self.hp
    def set_hp(self, value):
        '''Сеттер поля hp'''
        self.hp = value
    def get_damage(self):
        '''Геттер поля damage'''
        return self.damage
    def set_damage(self, value):
        '''Сеттер поля damage'''
        self.damage = value
    def get_defence(self):
        '''Геттер поля defence'''
        return self.defence
    def set_defence(self, value):
        '''Сеттер поля defence'''
        self.defence = value
    def get_img(self):
        '''Геттер поля img'''
        return self.img
    def set_img(self, value):
        '''Сеттер поля img'''
        self.img = value
    def get_speed(self):
        '''Геттер поля speed'''
        return self.speed
    def set_speed(self, value):
        '''Сеттер поля speed'''
        self.speed = value
    def get_name(self):
        '''Геттер поля name'''
        return self.name
    def set_name(self, value):
        '''Сеттер поля name'''
        self.name = value
    def get_visible_to(self):
        '''Геттер поля visible_to'''
        return self.visible_to
    def set_visible_to(self, value):
        '''Сеттер поля visible_to'''
        self.visible_to = value
    def get_master(self):
        '''Геттер поля master'''
        return self.master
    def set_master(self, value):
        '''Сеттер поля master'''
        self.master = value


def read_ship(fin):
    '''
    Считывает корабль, который был захеширован через Ship.cache(), из файла..
    '''
    ship = Ship()
    ship.set_name(rdf(fin))
    hp = int(rdf(fin))
    x_y = rdf(fin).replace(")", "").replace("(", "").split(", ")
    fly_to = rdf(fin).replace(")", "").replace("(", "").split(", ")
    master = int(rdf(fin))
    system = int(rdf(fin))
    nummer = int(rdf(fin))
    for i in range(nummer):
        ship.add_visible_to(int(rdf(fin)))
    ship.set_hp(hp)
    ship.set_xy(my_math.Coords(int(x_y[0]), int(x_y[1])))
    ship.set_target(my_math.Coords(int(fly_to[0]), int(fly_to[1])))
    ship.set_master(master)
    ship.set_system(system)
    return ship
