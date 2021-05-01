'''
В этом модуле размещены класс и функции для работы с планетами.
'''

from random import randint

from my_math import rdf
import my_math

def load_description(fin):
    '''
    Считывает из файла описание планеты.
    '''
    std = open(fin, 'r')
    descr = ""
    for i in std:
        descr = descr  + i
    std.close()
    return descr

class Planet:
    '''
    Класс планеты.
    '''
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates
        self.type = None
        self.image = None
        self.master = -1
        self.description = '''Какой-то дурачок создал планету общего
         вида. Ошибка в коде, извиняйте-с.'''
        '''Возможно,
        вы имеете счастье наблюдать планету-затычку, которая
        изображает звезду. Сделано это для того, чтобы обеспечить
        отсутствие планет на определённом расстоянии от того места,
        где в графическом интерфейсе будет изображаться звездa.'''

    def __str__(self):
        string = ""
        string = string + '      > Название планеты: ' + self.get_name()\
        + "\n"
        string = string + '           Стратегический тип планеты: ' +\
        self.type + "\n"
        string = string + '           Описание планеты: ' +\
        self.get_description() + "\n"
        string = string + '           Координаты в системе: ' +\
        str(self.get_coordinates()) + "\n"
        string = string + '           Изображение: ' +\
        self.get_image() + "\n"
        string = string + "           Хозяин планеты: " +\
        "никто" if self.get_master() == -1 else str(self.get_master())\
        + "\n"
        return string

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

def read_planet(fin):
    '''Считывает из файла закешированную при помощи Planet.cache() планету.'''
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
    return rez
