'''
Первые пять модульных тестов.
'''
import unittest
import my_math

class CoordsTest(unittest.TestCase):
    '''
    Демонстрирует, что класс Coords функционирует, как надо.
    '''
    def test_getting_and_setting(self):
        '''
        Проверяет, что поля класса Coords функционируют, как надо.
        '''
        test_coords = my_math.Coords(-5, 5)
        #Проверка конструкторов.
        self.assertEqual(test_coords.x, -5)
        self.assertEqual(test_coords.y, 5)
        #Проверка геттеров.
        self.assertEqual(test_coords.get_x(), -5)
        self.assertEqual(test_coords.get_y(), 5)
        #Проверка сеттеров.
        test_coords.set_x(-6)
        test_coords.set_y(6)
        self.assertEqual(test_coords.x, -6)
        self.assertEqual(test_coords.y, 6)

    def test_str_operator(self):
        '''
        Проверяет, что класс Coords корректно приводится к строке.
        '''
        test_coords = my_math.Coords(-5, 5)
        self.assertEqual(str(test_coords), '(-5, 5)')

    def test_equal_operator(self):
        '''
        Проверяет, что класс Coords имеет корректно перегруженный оператор сравнения.
        '''
        test_coords_1 = my_math.Coords(-5, 5)
        test_coords_2 = my_math.Coords(5, 5)
        self.assertEqual(test_coords_1 == test_coords_2, False)
        test_coords_2.x = -5
        self.assertEqual(test_coords_1 == test_coords_2, True)

    def test_to_pair(self):
        '''
        Проверяет, что класс Coords корректно приводится к кортежу из двух элементов.
        '''
        test_coords = my_math.Coords(-5, 5)
        self.assertEqual(test_coords.to_pair(), (-5, 5))

    def test_from_pair(self):
        '''
        Проверяет, что объект класса Coords можно корректно получить из кортежа
        из двух элементов.
        '''
        test_coords = my_math.Coords.from_pair((5, -5))
        self.assertEqual(my_math.Coords(5, -5), test_coords)
