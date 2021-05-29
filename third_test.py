'''
Третьи пять тестов.
'''

import unittest
import my_math
from class_planet import Planet
from class_ship import Ship
from class_card import Card

class TestSaves (unittest.TestCase):
    '''
    Проверяет, что при считывании/сохранении объекта (работа ведётся с
    временным файлом) не происходит потери или искажения данных.
    '''
    def test_planet(self):
        '''
        Проверяет, что планета считывается из файла корректно.
        '''
        planet = Planet.new_planet('test', my_math.Coords(1, 2))
        f = open('log.txt', 'w')
        print(planet.cache(), file=f)
        f.close()
        f = open('log.txt', 'r')
        readed_planet = Planet.read_planet(f)
        f.close()
        self.assertEqual(planet.limits, readed_planet.limits)
        self.assertEqual(planet.name, readed_planet.name)
        self.assertEqual(planet.coordinates, readed_planet.coordinates)
        self.assertEqual(planet.type, readed_planet.type)
        self.assertEqual(planet.image, readed_planet.image)
        self.assertEqual(planet.master, readed_planet.master)
        self.assertEqual(planet.description, readed_planet.description)
        self.assertEqual(planet.adi.will_be_occupied, readed_planet.adi.will_be_occupied)
        self.assertEqual(planet.adi.will_be_occupied_by, readed_planet.adi.will_be_occupied_by)

    def test_card(self):
        '''
        Проверяет, что карточка считывается из файла корректно.
        '''
        card = Card('test_attack')
        f = open('log.txt', 'w')
        print(card.cache(), file=f)
        f.close()
        f = open('log.txt', 'r')
        readed_card = Card.load(f)
        f.close()
        self.assertEqual(card.inf, readed_card.inf)
        self.assertEqual(card.dmg, readed_card.dmg)
        self.assertEqual(card.dfc, readed_card.dfc)
        self.assertEqual(card.mov, readed_card.mov)
        self.assertEqual(card.pri, readed_card.pri)
        self.assertEqual(card.tit, readed_card.tit)
        self.assertEqual(card.usb, readed_card.usb)
        self.assertEqual(card.dst, readed_card.dst)
        
    def test_ship(self):
        '''
        Проверяет, что корабль считывается из файла корректно.
        '''
        ship = Ship.new_ship('test')
        ship.master = -1
        ship.x_y = my_math.Coords(-1, 12)
        ship.system = 1533
        f = open('log.txt', 'w')
        print(ship.cache(), file=f)
        f.close()
        f = open('log.txt', 'r')
        readed_ship = Ship.read_ship(f)
        self.speed = None
        self.limit = None
        self.fleet = None
        f.close()
        self.assertEqual(ship.x_y, readed_ship.x_y)
        self.assertEqual(ship.system, readed_ship.system)
        self.assertEqual(ship.img, readed_ship.img)
        self.assertEqual(ship.name, readed_ship.name)
        self.assertEqual(ship.master, readed_ship.master)
        self.assertEqual(ship.img, readed_ship.img)
        #То, что card_store считываются корректно, уже проверено.
        
