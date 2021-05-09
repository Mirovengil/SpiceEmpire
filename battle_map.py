'''
В этом классе реализовано поле битвы кораблей и некоторые функции, с ним связанные.
'''

import my_math

class BattleMap:
    '''
    Класс карты для проведения сражений кораблей.
    Для ориентирования на ней используются battle_x_y : Coords.
    Поле имеет размеры size_x на size_y ГЕКСОВ.
    Следовательно, из клетки (x, y) можно переместиться в:
        > (x - 1; y);
        > (x + 1; y);
        > (x; y - 1);
        > (x; y + 1);
        > (x - 1; y - 1);
        > (x - 1; y + 1);
    '''
    def __init__(self, ships=None, size_x=10, size_y=10):
        self.size_x = size_x
        self.size_y = size_y
        self.ships = ships
        #Корабли также надобно расставить по полюшку ратному по следующему принципу:
        #сверху вниз, у левого края поля -- один игрок, а сверху вниз, у правого края поля --
        #второй.
        #Утверждается, что при такой механике, какая реализована в игре, в сражении не может
        #участвовать большее количество игроков, чем двое.
        left_player = self.ships[0].master
        last_y_on_left_side = 0
        last_y_on_right_side = 0
        ship = 0
        while ship < len(self.ships):
            if self.ships[ship].master == left_player:
                self.ships[ship].battle_x_y.x = 0
                self.ships[ship].battle_x_y.y = last_y_on_left_side
                last_y_on_left_side += 1
            else:
                self.ships[ship].battle_x_y.x = self.size_x - 1
                self.ships[ship].battle_x_y.y = last_y_on_right_side
                last_y_on_right_side += 1
            self.ships[ship].battle_mode_on()
            ship += 1

    def to_str():
        '''
        Преобразовывает поле битвы в строку (использовать для отладки или логгирования).
        '''
        if self.size_x is None or self.size_y is None or self.ships is None:
            raise ValueError('Карта не инициализирована!1')
        mass = [['.' for x in range(self.size_x)] for y in range(self.size_y)]
        for ship in self.ships:
            mass[ship.battle_x_y.y][ship.battle_x_y.x] = str(ship.master)
        string = ''
        for y in range(self.size_x):
            for x in range(self.size_y):
                string = string + (mass[y][x] + ' ' if y % 2 == 0 else ' ' + mass[y][x])
        return string

    def generate_near(self, coords):
        '''
        Возвращает координаты клеток, на которые можно переместиться из coords : Coords при
        условии гексагональности оных клеток.
        '''
        x = coords.x
        y = coords.y
        near = [
            my_math.Coords(x - 1, y), 
            my_math.Coords(x + 1, y),
            my_math.Coords(x, y - 1),
            my_math.Coords(x, y + 1),
            my_math.Coords(x - 1, y - 1),
            my_math.Coords(x - 1, y + 1),
        ]
        true_near = [] #Не включает клетки, которые не могут существовать.
        for i in near:
            if self.ok_xy(i):
                true_near.append(i)
        return true_near

    def ok_xy(self, coords):
        '''
        Проверяет, удовлетворяют ли координаты данному полю (могут ли они на
        нём существовать).
        '''
        x = coords.x
        y = coords.y
        ok_x = x >= 0 and x < self.size_x
        ok_y = y >= 0 and y < self.size_y
        return ok_x and ok_y

    def is_finished(self):
        '''
        Возвращает индекс игрока-победителя, либо -1, если бой ещё не закончился.
        '''
        ship = 0
        while ship < len(self.ships):
            if self.ships[ship].master != self.ships[ship + 1].master and self.ships[ship].is_live() and\
            self.ships[ship + 1].is_live():
                return -1
            ship += 1
        return self.ships[0].master
