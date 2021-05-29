'''
Третьи пять тестов.
'''

import unittest
import my_math
from class_planet import Planet

class TestSaves (unittest.TestCase):
    '''
    Проверяет, что при считывании/сохранении объекта (работа ведётся с
    временным файлом) не происходит потери или искажения данных.
    '''
    def test_planet(self):
        planet = Planet('Ioann', my_math.Coords(1, 2))
        planet.limits = ('Средняя', 10)
        planet.type = 'lave'
        planet.image = 'image'
        planet.master = Planet.NEITRAL
        f = open('./log.txt', 'w')
        print(planet.cache(), file=f)
        f.close()
        f = open('./log.txt', 'r')
        readed_planet = Planet.read_planet(f)
        self.assertEqual(readed_planet.name, planet.name)
        self.assertEqual(readed_planet.coordinates, planet.coordinates)
        self.assertEqual(readed_planet.limits, planet.limits)
        self.assertEqual(readed_planet.image, planet.image)
        self.assertEqual(readed_planet.master, planet.master)
        self.assertEqual(readed_planet.adi.will_be_occupied_by, planet.adi.will_be_occupied_by)
        self.assertEqual(readed_planet.adi.will_be_occupied, planet.adi.will_be_occupied)
        f.close()
        
        
