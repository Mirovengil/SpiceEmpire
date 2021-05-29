'''
Третьи пять тестов.
'''

import unittest
import my_math
from class_planet import Planet
from class_ship import Ship

class TestSaves (unittest.TestCase):
    '''
    Проверяет, что при считывании/сохранении объекта (работа ведётся с
    временным файлом) не происходит потери или искажения данных.
    '''
    def test_planet(self):
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
        
        
