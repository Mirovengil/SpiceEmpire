'''
Третьи пять тестов.
'''

import unittest
import my_math
from class_planet import Planet
from class_ship import Ship
from class_card import Card
from class_card import CardStore
from class_map import GameMap

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

    def test_card_store(self):
        '''
        Проверяет, что card_store считывается из файла корректно.
        '''
        card_store = CardStore(fin='test')
        f = open('log.txt', 'w')
        print(card_store.cache(), file=f)
        f.close()
        f = open('log.txt', 'r')
        readed_card_store = CardStore.load(f)
        f.close()
        card = 0
        while card < len(card_store.cards):
            self.assertEqual(card_store.cards[card].inf, readed_card_store.cards[card].inf)
            self.assertEqual(card_store.cards[card].dmg, readed_card_store.cards[card].dmg)
            self.assertEqual(card_store.cards[card].dfc, readed_card_store.cards[card].dfc)
            self.assertEqual(card_store.cards[card].mov, readed_card_store.cards[card].mov)
            self.assertEqual(card_store.cards[card].pri, readed_card_store.cards[card].pri)
            self.assertEqual(card_store.cards[card].tit, readed_card_store.cards[card].tit)
            self.assertEqual(card_store.cards[card].usb, readed_card_store.cards[card].usb)
            self.assertEqual(card_store.cards[card].dst, readed_card_store.cards[card].dst)
            card += 1

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
        f.close()
        self.assertEqual(ship.x_y, readed_ship.x_y)
        self.assertEqual(ship.system, readed_ship.system)
        self.assertEqual(ship.img, readed_ship.img)
        self.assertEqual(ship.name, readed_ship.name)
        self.assertEqual(ship.master, readed_ship.master)
        self.assertEqual(ship.img, readed_ship.img)
        #То, что card_store считываются корректно, уже проверено.

    def test_map(self):
        '''
        Проверяет, что карта считывается из файла корректно.
        '''
        game_map = GameMap()
        game_map.size_x = 123
        game_map.size_y = 321
        game_map.number_of_players = 6666
        f = open('log.txt', 'w')
        print(game_map.cache(), file=f)
        f.close()
        readed_map = GameMap.read_map('log.txt')
        self.assertEqual(game_map.size_x, readed_map.size_x)
        self.assertEqual(game_map.size_y, readed_map.size_y)
        self.assertEqual(game_map.number_of_players, readed_map.number_of_players)
        self.assertEqual(game_map.player, readed_map.player)
        self.assertEqual(game_map.turn, readed_map.turn)
        self.assertEqual(game_map.battle_is_on, readed_map.battle_is_on)
        self.assertEqual(game_map.profit, readed_map.profit)
        
