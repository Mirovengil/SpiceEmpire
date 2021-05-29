'''
Вторые пять тестов.
'''

import unittest
import my_math
import dns_realization

class DistTest(unittest.TestCase):
    '''
    Демонстрирует, что dist(point1, point2) действует, как надо.
    '''
    def test_dist(self):
        '''
        Демонстрирует, что dist(point1, point2) действует, как надо.
        '''
        a = my_math.Coords(0, 0)
        b = my_math.Coords(1, 1)
        self.assertEqual(my_math.dist(a, b), 2 ** 0.5)
        b.x = -1
        self.assertEqual(my_math.dist(a, b), 2 ** 0.5)
        b.y = -1
        self.assertEqual(my_math.dist(a, b), 2 ** 0.5)
        b.x = 1
        self.assertEqual(my_math.dist(a, b), 2 ** 0.5)

class DNSTest(unittest.TestCase):
    '''
    Демонстрирует, что система СНМ работает, как надо.
    Elem не нуждается в тестировании, так как, де факто, является структурой
    без методов.
    '''
    def test_new_dns(self):
        '''
        Проверяет, что СНМ создаётся корректно.
        '''
        dns = dns_realization.DNS(3)
        #Проверка, что всё три элемента не соединены.
        self.assertNotEqual(dns.get_parent(0), dns.get_parent(1))
        self.assertNotEqual(dns.get_parent(1), dns.get_parent(2))
        self.assertNotEqual(dns.get_parent(2), dns.get_parent(0))

    def test_get_parent(self):
        '''
        Проверяет, что родитель элемента ищется корректно.
        '''
        dns = dns_realization.DNS(3)
        #Изначально корнем каждого элемента является он сам.
        self.assertEqual(dns.get_parent(0), 0)
        self.assertEqual(dns.get_parent(1), 1)
        self.assertEqual(dns.get_parent(2), 2)
        #После объединения первых двух элементов, корнем должна стать нулёвой.
        dns.unite(0, 1)
        self.assertEqual(dns.get_parent(0), 0)
        self.assertEqual(dns.get_parent(1), 0)
        #После объединения всех элементов, они должны иметь общий корень.
        dns.unite(0, 2)
        self.assertEqual(dns.get_parent(0), dns.get_parent(1))
        self.assertEqual(dns.get_parent(1), dns.get_parent(2))
        self.assertEqual(dns.get_parent(2), dns.get_parent(0))

    def test_unite_elems(self):
        '''
        Проверяет, что два элемента корректно соединяются между собой.
        '''
        dns = dns_realization.DNS(3)
        dns.unite(1, 2)
        #Проверка, что всё соединены только элементы 1 и 2.
        self.assertNotEqual(dns.get_parent(0), dns.get_parent(1))
        self.assertEqual(dns.get_parent(1), dns.get_parent(2))
        self.assertNotEqual(dns.get_parent(2), dns.get_parent(0))

    def test_size_logistiv(self):
        '''
        Проверяет, что всегда меньшее объединение элементов крепится к большему,
        а не наоборот.
        '''
        dns = dns_realization.DNS(5)
        # 0, 1, 2, 3, 4
        dns.unite(0, 1)
        # 0 <- 1, 2, 3, 4
        dns.unite(1, 2)
        # 2 -> 0 <- 1, 3, 4
        dns.unite(3, 4)
        # 2 -> 0 <- 1, 3 <- 4
        #Так как объединение элементов 2 -> 0 <- 1 состоит из трёх элементов, то
        #3 <- 4 должно к нему прикрепиться, а не наоборот.
        bigger_parent = dns.get_parent(2)
        dns.unite(3, 2)
        #          3
        #          |
        #         V
        # 2 -> 0 <- 1
        #         ^
        #         |
        #         4
        self.assertEqual(dns.get_parent(0), bigger_parent)
        self.assertEqual(dns.get_parent(1), bigger_parent)
        self.assertEqual(dns.get_parent(2), bigger_parent)
        self.assertEqual(dns.get_parent(3), bigger_parent)
        self.assertEqual(dns.get_parent(4), bigger_parent)
