'''
В этом модуле размещены класс и функции для работы с планетами.
'''

from random import randint

from my_math import rdf
import my_math

LIMITS = [
    ('Богатая', 15),
    ('Средняя', 10),
    ('Бедная', 5)
]

class Planet:
    '''
    Класс планеты.
    name : string -- название планеты;
    coordinates : Coords -- координаты планеты на планетарной карте;
    description : string -- текстоое описание планеты, которое видит
    игрок;
    image : string --  имя изображения, соответствующего планете;
    master : int -- номер игрока, которому принадлежит планета;
    нейтральные планеты имеют хозяина NEITRAL;
    limits : int -- кол-во лимитов, которые планета приносит империи.
    '''

    LIM_SIZE = 1
    LIM_NAME = 0
    NEITRAL = -1
    types = ['lave', 'ice', 'earth', 'desert', 'water', 'rock', 'air']
    def __init__(self, name, coordinates):
        self.limits = None
        self.name = name
        self.coordinates = coordinates
        self.type = None
        self.image = None
        self.master = Planet.NEITRAL
        self.description = '''Какой-то дурачок создал планету общего
         вида. Ошибка в коде, извиняйте-с.'''
        '''Возможно,
        вы имеете счастье наблюдать планету-затычку, которая
        изображает звезду. Сделано это для того, чтобы обеспечить
        отсутствие планет на определённом расстоянии от того места,
        где в графическом интерфейсе будет изображаться звездa.'''

    def __str__(self):
        string = ""
        string = string + 'Название планеты: ' + self.get_name()\
        + "\n"
        string = string + 'Стратегический тип планеты: ' +\
        self.type + "\n"
        string = string + 'Вместимость: ' + self.limits[Planet.LIM_NAME] + "\n"
        string = string + 'Описание планеты: ' +\
        self.get_description() + "\n"
        string = string + 'Координаты в системе: ' +\
        str(self.get_coordinates()) + "\n"
        string = string + 'Изображение: ' +\
        self.get_image() + "\n"
        string = string + "Хозяин планеты: " +\
        ("никто" if self.is_neitral() else str(self.get_master()))\
        + "\n"
        return string

    def is_neitral(self):
        '''
        Возвращает True, если у планеты нет владельца.
        '''
        return self.master == Planet.NEITRAL

    def cache(self):
        '''
        Кеширует планету. Это необходимо для реализации сохранений.
        '''
        string = ""
        string = string + str(self.type) + "\n"
        string = string + self.name + "\n"
        string = string + str(self.coordinates.get_x()) + "\n"
        string = string + str(self.coordinates.get_y()) + "\n"
        string = string + self.image + "\n"
        string = string + str(self.master) + "\n"
        string = string + str(self.limits[Planet.LIM_SIZE]) + "\n"
        return string

    #Геттеры и сеттеры (сгенерированы автоматически)
    def get_name(self):
        '''Геттер поля name'''
        return self.name
    def set_name(self, value):
        '''Сеттер поля name'''
        self.name = value
    def get_coordinates(self):
        '''Геттер поля coordinates'''
        return self.coordinates
    def set_coordinates(self, value):
        '''Сеттер поля coordinates'''
        self.coordinates = value
    def get_type(self):
        '''Геттер поля type'''
        return self.type
    def set_type(self, value):
        '''Сеттер поля type'''
        self.type = value
    def get_image(self):
        '''Геттер поля image'''
        return self.image
    def set_image(self, value):
        '''Сеттер поля image'''
        self.image = value
    def get_master(self):
        '''Геттер поля master'''
        return self.master
    def set_master(self, value):
        '''Сеттер поля master'''
        self.master = value
    def get_description(self):
        '''Геттер поля description'''
        return self.description
    def set_description(self, value):
        '''Сеттер поля description'''
        self.description = value

    @staticmethod
    def load_description(fin):
        '''
        Считывает из файла описание планеты.
        '''
        fin = './data/descr/' + fin + '_description.txt'
        fin = open(fin, 'r')
        descr = ""
        for i in fin:
            descr = descr  + i
        fin.close()
        return descr

    @staticmethod
    def read_planet(fin):
        '''
        Считывает из файла закешированную при помощи Planet.cache() планету.
        '''
        typeplanet = str(rdf(fin))
        name = str(rdf(fin))
        x = int(rdf(fin))
        y = int(rdf(fin))
        coordinates = my_math.Coords(x, y)
        rez = Planet(name, coordinates)
        image = str(rdf(fin))
        master = int(rdf(fin))
        rez.set_image(image)
        rez.set_master(master)
        rez.set_type(typeplanet)
        description = Planet.load_description(rez.get_type())
        rez.set_description(description)
        limits_size = int(rdf(fin))
        for i in LIMITS:
            if i[Planet.LIM_SIZE] == limits_size:
                rez.limits = i
                break
        return rez

    @staticmethod
    def new_planet(name, coords):
        '''
        Создаёт случайную планету и возвращает её.
        '''
        planet = Planet(name, coords)
        planet.set_type(Planet.types[randint(0, len(Planet.types) - 1)])
        planet.set_image('/img/planets' + planet.get_type() + '.png')
        planet.set_description(Planet.load_description(planet.get_type()))
        planet.limits = LIMITS[randint(0, len(LIMITS) - 1)]
        return planet
