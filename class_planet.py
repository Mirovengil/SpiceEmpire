'''
В этом модуле размещены класс и функции для работы с планетами.
'''

from random import randint

from my_math import rdf
import my_math

TURNS_TO_GET_PLANET = 3
LIMITS = [
    ('Богатая', 15),
    ('Средняя', 10),
    ('Бедная', 5)
]

class AdditionalInfo:
    '''
    Класс дополнительной информации о планете.
    На данный момент содержит:
        will_be_occupied : int -- кол-во ходов, через которое планета будет захвачена.
        will_be_occupied_by : int -- индекс игрока, который захватит планету по
        окончании вышеупомянутого срока.
    '''
    def __init__(self):
        self.will_be_occupied = TURNS_TO_GET_PLANET
        self.will_be_occupied_by = Planet.NEITRAL 
    
    def __str__(self):
        string = ""
        if self.will_be_occupied_by != Planet.NEITRAL:
            string = string + "Планету захватит через " + str(self.will_be_occupied)  +\
            " игрок №" + str(self.will_be_occupied_by) + "\n"
        return string
        
    def cache(self):
        '''
        Возвращает строку : str, которая содержит информацию об объекте класса.
        '''
        string = ""
        string = string + str(self.will_be_occupied) + "\n"
        string = string + str(self.will_be_occupied_by) + "\n"
        return string

    @staticmethod
    def read(fin):
        '''
        Считывает закешированное при помощи self.cache() из файла fin, который
        надо открыть заранее.
        '''
        rez = AdditionalInfo()
        rez.will_be_occupied = int(rdf(fin))
        rez.will_be_occupied_by = int(rdf(fin))
        return rez

    def new_master(self, master):
        '''
        Означает, что игрок под индексом master : int начал захват планеты.
        '''
        self.will_be_occupied = TURNS_TO_GET_PLANET
        self.will_be_occupied_by = master
        
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
    adi : AdditionalInfo -- дополнительная информация о планете (см. соответствующий класс).
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
        self.adi = AdditionalInfo()

    def try_to_get_master_out(self, ships):
        '''
        Принимает на вход массив всех кораблей, имеющихся в игре, ships : [Ship].
        Если корабль прекратил захват планеты, то информация о ней обновляется.
        '''
        has_ship_or_master = False
        for ship in ships:
            if ship.x_y == self.coordinates and ship.master != self.master:
                self.adi.new_master(ship.master)
                has_ship_or_master = True
        if not has_ship_or_master:
            self.adi.will_be_occupied_by = self.master

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
        string = string + self.adi.cache()
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
        #Проверка на то, что у планеты -- корректное кол-во лимитов.
        has_true_limits = False
        for i in LIMITS:
            if i[Planet.LIM_SIZE] == limits_size:
                rez.limits = i
                has_true_limits = True
                break
        if not has_true_limits:
            raise ValueError('''Вы либо повредили файлы с сохранениями, либо
            играете против читера! Некорректные размеры лимитов планеты!!11''')
        rez.adi = AdditionalInfo.read(fin)
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

    def refresh_master(self):
        '''
        Обновляет количество ходов, через которое будет захвачена данная планета.
        '''
        if self.adi.will_be_occupied_by ==  Planet.NEITRAL or\
        self.adi.will_be_occupied_by == self.master:
            return 0
        self.adi.will_be_occupied = max(self.adi.will_be_occupied - 1, 0)
        if self.adi.will_be_occupied == 0:
            self.master = self.adi.will_be_occupied_by
