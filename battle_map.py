'''
В этом классе реализовано поле битвы кораблей и некоторые функции, с ним связанные.
'''

MY_PAIR_DEGREE = 0
MY_PAIR_COORD = 1

import my_math
MARKER = '@'
NONE = '.'
ZONE_MARKER = '^'

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
        self.turn_left = True
        #Корабли также надобно расставить по полюшку ратному по следующему принципу:
        #сверху вниз, у левого края поля -- один игрок, а сверху вниз, у правого края поля --
        #второй.
        #Утверждается, что при такой механике, какая реализована в игре, в сражении не может
        #участвовать большее количество игроков, чем двое.
        self.left_player = self.ships[0].master
        last_y_on_left_side = 0
        last_y_on_right_side = 0
        ship = 0
        while ship < len(self.ships):
            self.ships[ship].battle_x_y = my_math.Coords()
            if self.ships[ship].master == self.left_player:
                self.ships[ship].battle_x_y.x = 0
                self.ships[ship].battle_x_y.y = last_y_on_left_side
                last_y_on_left_side += 1
            else:
                self.right_player = self.ships[ship].master
                self.ships[ship].battle_x_y.x = self.size_x - 1
                self.ships[ship].battle_x_y.y = last_y_on_right_side
                last_y_on_right_side += 1
            self.ships[ship].battle_mode_on()
            ship += 1

    def str(self, marked=None, marked_zone=-1):
        '''
        Преобразовывает поле битвы в строку (использовать для отладки или логгирования).
        marked : int -- индекс корабля, котовый выделится особым символом.
        marked_zone : int -- расстояние от клетки корабля, которое выделится особыми
        символами (можно использовать, чтобы показать диапазон атаки/движения).
        '''
        if self.size_x is None or self.size_y is None or self.ships is None:
            raise ValueError('Карта не инициализирована!1')
        mass = [[NONE for x in range(self.size_x)] for y in range(self.size_y)]
        for ship in self.ships:
            mass[ship.battle_x_y.y][ship.battle_x_y.x] = str(ship.master)
        if not marked is None:
            marked = self.ships[marked].battle_x_y
            mass[marked.y][marked.x] = MARKER
            if marked_zone > 0:
                marked_cells = self.get_possible(marked, marked_zone)
                for cell in marked_sells:
                    mass[cell.y][cell.x] = ZONE_MARKER
        string = ''
        for y in range(self.size_y):
            for x in range(self.size_x):
                string = string + (mass[y][x] + ' ' if y % 2 == 0 else ' ' + mass[y][x])
            string = string + "\n"
        return string

    def _get_near_coords_(self, coords):
        '''
        Возвращает множество, содержащее координаты клеток, смежных с
        coords : Coords, при условии, что всё происходит в гексагональном измерении.
        '''
        x_value = 0
        y_value = 1
        x = coords[x_value]
        y = coords[y_value]
        near = set()
        near.add(my_math.Coords(x - 1, y).to_pair())
        near.add(my_math.Coords(x + 1, y).to_pair())
       
        if y % 2 != 0:
            near.add(my_math.Coords(x, y - 1).to_pair())
            near.add(my_math.Coords(x, y + 1).to_pair())
            near.add(my_math.Coords(x + 1, y - 1).to_pair())
            near.add(my_math.Coords(x + 1, y + 1).to_pair())
        else:
            near.add(my_math.Coords(x - 1, y - 1).to_pair())
            near.add(my_math.Coords(x - 1, y + 1).to_pair())
            near.add(my_math.Coords(x, y - 1).to_pair())
            near.add(my_math.Coords(x, y + 1).to_pair())
        true_near = set() #Не включает клетки, которые не могут существовать.
        for value in near:
            if self.ok_xy(value):
                true_near.add(value)
        return true_near

    def generate_near(self, coords):
        '''
        Возвращает словарь, который имеет градус, на который необходимо переместиться,
        в качестве ключа, и координаты клетки, на которую можно переместиться из
        coords : Coords при условии гексагональности оных клеток, в качестве значения.
        '''
        x = coords.x
        y = coords.y
        near = {
            180: my_math.Coords(x - 1, y), 
            0: my_math.Coords(x + 1, y),
        }
        if y % 2 != 0:
            near[120] = my_math.Coords(x, y - 1)
            near[-120] = my_math.Coords(x, y + 1)
            near[60] = my_math.Coords(x + 1, y - 1)
            near[-60] = my_math.Coords(x + 1, y + 1)
        else:
            near[120] = my_math.Coords(x - 1, y - 1)
            near[-120] = my_math.Coords(x - 1, y + 1)
            near[60] = my_math.Coords(x, y - 1)
            near[-60] = my_math.Coords(x, y + 1)
        true_near = {} #Не включает клетки, которые не могут существовать.
        for key, value in near.items():
            if self.ok_xy(value):
                true_near[key] = value
        return true_near

    def ok_xy(self, coords):
        '''
        Проверяет, удовлетворяют ли координаты данному полю (могут ли они на
        нём существовать).
        '''
        if isinstance(coords, my_math.Coords): 
            x = coords.x
            y = coords.y
        else:
            x_value = 0
            y_value = 1
            x = coords[x_value]
            y = coords[y_value]
        ok_x = x >= 0 and x < self.size_x
        ok_y = y >= 0 and y < self.size_y
        return ok_x and ok_y

    def is_finished(self):
        '''
        Возвращает индекс игрока-победителя, либо -1, если бой ещё не закончился.
        '''
        ship = 0
        while ship < len(self.ships):
            if self.ships[ship].master != self.ships[ship + 1].master and\
            self.ships[ship].is_live() and self.ships[ship + 1].is_live():
                return -1
            ship += 1
        return self.ships[0].master

    def now_player(self):
        '''
        Возвращает номер (глобальный, не внутри битвы) игрока, которому принадлежит ход
        в битве на данный момент.
        '''
        if self.turn_left:
            return self.left_player
        return self.right_player

    def next_turn(self):
        '''
        Передаёт ход в битве следующему игроку в очереди.
        '''
        self.turn_left = not self.turn_left

    def usable_ships(self):
        '''
        Возвращает массив кораблей, которыми может воспользоваться игрок, что ходит.
        '''
        ships = []
        for ship in self.ships:
            if ship.master == self.player_turns_now() and ship.is_available:
                ships.append(ship)
        return ships

    def ship_info(self, ship_index):
        '''
        Возвращает данные корабля с индексом ship_index : int в виде описания
        (данные + словесные пояснения к ним).
        '''
        return self.ships[ship_index].battle_str()

    def player_turns_now(self):
        '''
        Возвращает номер игрока, которому сейчас принадлежит ход в битве.
        '''
        if  self.turn_left:
            return self.left_player
        return self.right_player

    def get_possible(self, place_from, len_of_way):
        '''
        Возвращает те клетки, которые находятся на расстоянии, не большем
        len_of_way : int, от клетки place_from : Coords.
        '''
        answer = set()
        answer.add(place_from.to_pair())
        length = len_of_way
        while length > 0:
            possible = set()
            for near in answer:
                print('near:', near)
                possible = possible | self._get_near_coords_(near)
            answer = answer | possible
            length -= 1
        ans = []
        for value in answer:
            ans.append(my_math.Coords.from_pair(value))
        return ans
