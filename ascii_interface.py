'''
Модуль содержит реализацию ASCII-интерфейса для игры в SpiceEmpire.
Пока основное предназначение -- проведение тестов.
Однако есть вероятность, что он, по причине безделия большей части
команды, станет основным.
Или, тащемта, например, будет выдвинут под девизом "пойдёт на любой
кофеварке!".
'''

import os

import generate_map
import class_map
import class_star
import my_math

TITLE_CMD = 0
CMD = 1
SIZE = 30

class ASCIIInteface:
    '''
    Класс интерфейса. По причине того, что ASCII-графика несколько
    устарела (скажите это Dwarf Fortress, ага), он будет не
    сверхпродвинутым, а обеспечивающим основные игровые функции для
    красноглазиков в Gentoo.
    '''
    def __init__(self):
        self.game = None
        self.scouted_star = None
        self.scouted_ship = None

    @staticmethod
    def read_number(text):
        '''
        Считывает с клавиатуры номер чего-либо и приводит его к
        индексации.
        '''
        return int(input(text)) - 1

    @staticmethod
    def wait():
        '''
        Ждёт нажатия клавиши ENTER.
        '''
        ASCIIInteface.wait()

    def print_cmd(self, cmd):
        '''
        Выводит список команд, считывает ввод и выполняет выбранную
        команду.
        '''
        print('-' * SIZE)
        for i in enumerate(cmd):
            print(i[0] + 1, '. ', i[1][TITLE_CMD], sep='')
        cmd_complete = ASCIIInteface.read_number('ВВОД: ')
        cmd[cmd_complete][CMD](self)

    def new_game(self):
        '''
        Создаёт новую игру.
        '''
        option = generate_map.GeneratorOptions()
        self.game = generate_map.generate_map(option)
        print('Новая игра создана!')

    def load_game(self):
        '''
        Загружает игру. Пока что только из файла 'log.txt'.
        '''
        self.game = class_map.GameMap.read_map("log.txt")
        print('Игра успешно загружена!')

    def exit(self):
        '''
        Завершает выполнение программы.
        '''
        exit(0)

    def start(self):
        '''
        Главное меню игры.
        '''
        os.system('clear')
        mass = [
        ('Новая игра', ASCIIInteface.new_game),
        ('Загрузить игру', ASCIIInteface.load_game),
        ('Выйти из игры', ASCIIInteface.exit)
        ]
        if not self.game is None:
            mass.append(('Продолжить игру', ASCIIInteface.show_stars))
            mass.append(('Сохранить игру', ASCIIInteface.save_game))
        self.print_cmd(mass)
        ASCIIInteface.wait()
        os.system('clear')
        self.show_stars()

    def show_stars(self):
        '''
        Отрисовывает все звёзды и предлагает перейти к одной из них.
        '''
        os.system('clear')
        print('Звёзды:')
        for i in enumerate(self.game.stars):
            print(i[0] + 1, '. ', i[1].name, sep='')
        mass = [
        ('Главное меню', ASCIIInteface.start),
        ('Просмотр звезды', ASCIIInteface.show_one_star)
        ]
        self.print_cmd(mass)

    def show_one_star(self):
        '''
        Отрисовывает все планеты системы, её корабли и предлагает перейти
        к чему-то из этого.
        '''
        self.scouted_star = ASCIIInteface.read_number('Номер звезды: ')
        self.now_star()

    def now_star(self):
        '''
        Отрисовывает ту звезду, которую рассматривали последней.
        '''
        os.system('clear')
        print('Звезда: ' + self.game.stars[self.scouted_star].name)
        print('Соседи:')
        for i in enumerate(self.game.stars[self.scouted_star].neighbours):
            print(str(i[0] + 1) + '. ' +\
                self.game.stars[class_star.Star.get_neighbour(i[1])].name +\
                '(' + str(class_star.Star.get_way_len(i[1])) + ' ПА)')
        marked_coords = []
        print('Планеты:')
        for i in enumerate(self.game.stars[self.scouted_star].planets):
            print(i[0] + 1, ': ', i[1].name, sep='')
            marked_coords.append(i[1].coordinates)
        for y in range(self.game.stars[self.scouted_star].size_y):
            for x in range(self.game.stars[self.scouted_star].size_x):
                if my_math.Coords(x, y) in marked_coords:
                    print('*', end=' ')
                else:
                    print('-', end=' ')
            print()
        print('Корабли:')
        cnt = 1
        for i in self.game.ships:
            if i.system == self.scouted_star:
                print(str(cnt) + '. ' + i.name + ' игрока №' +\
                str(i.master) + ' (' + str(i.hp) + ' HP)')
                cnt += 1
        mass = [
        ('Главное меню', ASCIIInteface.start),
        ('Просмотр звезды', ASCIIInteface.show_one_star),
        ('Просмотр планеты', ASCIIInteface.show_planet),
        ('Просмотр корабля', ASCIIInteface.show_ship),
        ]
        self.print_cmd(mass)

    def now_ship(self):
        '''
        Отрисовывает тот корабль, который рассматривали последним.
        '''
        os.system('clear')
        print(self.game.ships[self.scouted_ship].str(self.game.stars))
        print('Карточки:')
        for i in enumerate(self.game.ships[self.scouted_ship].card_store.cards):
            print(str(i[0] + 1) + ". " + i[1].tit)
        mass = [
            ('Главное меню', ASCIIInteface.start),
            ('Назад к звезде', ASCIIInteface.now_star),
            ('Просмотр карточки', ASCIIInteface.show_card)
        ]
        self.print_cmd(mass)

    def show_planet(self):
        '''
        Отрисовывает планету.
        '''
        planet = ASCIIInteface.read_number('Номер планеты: ')
        os.system('clear')
        print(self.game.stars[self.scouted_star].planets[planet])
        mass = [
        ('Главное меню', ASCIIInteface.start),
        ('Назад к звезде', ASCIIInteface.now_star)
        ]
        self.print_cmd(mass)

    def show_card(self):
        '''
        Отрисовывает карту корабля
        '''
        card = ASCIIInteface.read_number('Номер карточки: ')
        os.system('clear')
        print(self.game.ships[self.scouted_ship].card_store.cards[card])
        mass = [
        ('Главное меню', ASCIIInteface.start),
        ('Назад к кораблю', ASCIIInteface.now_ship)
        ]
        self.print_cmd(mass)

    def show_ship(self):
        '''
        Отрисовывает корабль.
        '''
        self.scouted_ship = ASCIIInteface.read_number('Номер корабля: ')
        cnt = 0
        for i in enumerate(self.game.ships):
            cnt += (i[1].system == self.scouted_star)
            if cnt == self.scouted_ship:
                self.scouted_ship = i[0]
                break
        self.now_ship()

    def save_game(self):
        '''
        Сохраняет начатую игру в файл log.txt.
        '''
        print('Игра успешно сохранена.')
        file_to_save = open('./log.txt', 'w')
        print(self.game.cache(), file=file_to_save)
        file_to_save.close()
        ASCIIInteface.wait()
        ASCIIInteface.cls()
        

if __name__ == "__main__":
    TEST_INTERFACE = ASCIIInteface()
    TEST_INTERFACE.start()
