'''
Модуль содержит реализацию ASCII-интерфейса для игры в SpiceEmpire.
Пока основное предназначение -- проведение тестов.
Однако есть вероятность, что он, по причине безделия большей части
команды, станет основным.
Или, тащемта, например, будет выдвинут под девизом "пойдёт на любой
кофеварке!".
'''

import generate_map
import class_map
import class_star
import my_math
import class_planet 
import random
TITLE_CMD = 0
CMD = 1
SIZE = 30


#Типа, ASCII-графений.
INTRO_IMG = my_math.rdf_all('./ASCII/Intro.txt')
PLANET_IMG = my_math.rdf_all('./ASCII/Planet.txt')
STAR_IMG = my_math.rdf_all("./ASCII/Star.txt")
SHIP_IMG = my_math.rdf_all("./ASCII/Ship.txt")

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
        self.scouted_card = None

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
        input()

    @staticmethod
    def cls():
        '''
        Очищает консоль.
        '''
        print("\033c", end="")

    def print_cmd(self, cmd):
        '''
        Выводит список команд, считывает ввод и выполняет выбранную
        команду.
        '''
        print('-' * SIZE)
        if not self.game is None:
            print('Ход №' + str(self.game.turn))
            print('Хотит игрок №' + str(self.game.player))
            print('Лимитов: ' + str(self.game.limits[self.game.player]))
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
        random.seed()
        ASCIIInteface.cls()
        print(INTRO_IMG)
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
        ASCIIInteface.cls()
        self.show_stars()

    def show_stars(self):
        '''
        Отрисовывает все звёзды и предлагает перейти к одной из них.
        '''
        ASCIIInteface.cls()
        print('Звёзды:')
        for i in enumerate(self.game.stars):
            print(i[0] + 1, '. ', (i[1].name if self.game.player in i[1].can_be_seen else 'СКРЫТО!'), sep='')
        mass = [
            ('Главное меню', ASCIIInteface.start),
            ('Просмотр звезды', ASCIIInteface.show_one_star),
            ('Завершить ход', ASCIIInteface.end_turn)
        ]
        self.print_cmd(mass)

    def show_one_star(self):
        '''
        Отрисовывает все планеты системы, её корабли и предлагает перейти
        к чему-то из этого.
        '''
        star = ASCIIInteface.read_number('Номер звезды: ')
        if not self.game.player in self.game.stars[star].can_be_seen:
            raise ValueError('Вы не можете рассматривать систему, где нет ваших кораблей!')
        self.scouted_star = star
        self.now_star()

    def now_star(self):
        '''
        Отрисовывает ту звезду, которую рассматривали последней.
        '''
        ASCIIInteface.cls()
        print('Звезда: ' + self.game.stars[self.scouted_star].name)
        print(STAR_IMG)
        print('Соседи:')
        for i in enumerate(self.game.stars[self.scouted_star].neighbours):
            print(str(i[0] + 1) + '. ' +\
                self.game.stars[class_star.Star.get_neighbour(i[1])].name +\
                '(' + str(class_star.Star.get_way_len(i[1])) + ' ПА)')
        print('Планеты:')
        for i in enumerate(self.game.stars[self.scouted_star].planets):
            print(i[0] + 1, ': ', i[1].name, sep='')
        print(self.game.stars[self.scouted_star].to_matrix())
        print('Корабли:')
        cnt = 1
        for i in self.game.ships:
            if i.system == self.scouted_star:
                print(str(cnt) + '. ' + i.name + ' игрока №' +\
                str(i.master) + ' (' + str(i.hp) + ' HP)' +\
                (' -- ЗАЩИЩАЕТСЯ' if i.dfc > 0 else ''))
                cnt += 1
        mass = [
            ('Главное меню', ASCIIInteface.start),
            ('Просмотр планеты', ASCIIInteface.show_planet),
            ('Просмотр корабля', ASCIIInteface.show_ship),
            ('Назад, к звёздам', ASCIIInteface.show_stars),
            ('Завершить ход', ASCIIInteface.end_turn)
        ]
        self.print_cmd(mass)

    def now_ship(self):
        '''
        Отрисовывает тот корабль, который рассматривали последним.
        '''
        ASCIIInteface.cls()
        print(SHIP_IMG)
        print(self.game.ships[self.scouted_ship].str(self.game.stars))
        print(self.game.stars[self.scouted_star].to_matrix(\
        self.game.ships[self.scouted_ship].x_y))
        print('Карточки:')
        for i in enumerate(self.game.ships[self.scouted_ship].card_store.cards):
            print(str(i[0] + 1) + ". " + i[1].tit)
        mass = [
            ('Главное меню', ASCIIInteface.start),
            ('Назад к звезде', ASCIIInteface.now_star),
            ('Просмотр карточки', ASCIIInteface.show_card),
            ('Перемещение корабля', ASCIIInteface.move_ship_on_map)
            #('Использование карточки', ASCIIInteface.use_card)#Карточки не используются вне боя(
        ]
        self.print_cmd(mass)

    def move_ship_on_map(self):
        '''
        Выбирает клетку и перемещает корабль на глобальной карте.
        На это расходуются единицы перемещения.
        '''
        ASCIIInteface.cls()
        print('Карта:')
        print(self.game.stars[self.scouted_star].to_matrix(\
        self.game.ships[self.scouted_ship].x_y))
        print('Вы отмечены как @:')
        x = ASCIIInteface.read_number('Введите х клетки: ')
        y = ASCIIInteface.read_number('Введите y клетки: ')
        self.game.ships[self.scouted_ship].move_on_global_map(my_math.Coords(x, y))
        self.now_star()

    def show_planet(self):
        '''
        Отрисовывает планету.
        '''
        planet = ASCIIInteface.read_number('Номер планеты: ')
        ASCIIInteface.cls()
        print(PLANET_IMG)
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
        ASCIIInteface.cls()
        print(self.game.ships[self.scouted_ship].card_store.cards[card])
        mass = [
            ('Главное меню', ASCIIInteface.start),
            ('Назад к кораблю', ASCIIInteface.now_ship),
            #('Использовать карточку', ASCIIInteface.use_now_card)
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
        ASCIIInteface.cls()
        print('Игра успешно сохранена.')
        file_to_save = open('./log.txt', 'w')
        print(self.game.cache(), file=file_to_save)
        file_to_save.close()

    def use_card(self):
        '''
        Выбирает карточку и использует её.
        '''
        self.scouted_card = ASCIIInteface.read_number('Номер карточки: ')
        self.use_now_card()

    def use_now_card(self):
        '''
        Использует карточку, которая была выбрана или рассматривается.
        '''
        ASCIIInteface.cls()
        print('Выберите действие: ')
        card = self.game.ships[self.scouted_ship].card_store.cards[\
        self.scouted_card]
        self.print_cmd([
            ('Атака ({} ед.)'.format(card.dmg), ASCIIInteface.attack),
            ('Защита ({} ед.)'.format(card.dfc), ASCIIInteface.defence),
            ('Движение ({} ед.)'.format(card.mov), ASCIIInteface.move)
        ])

    def attack(self):
        '''
        Выбирает вражеский корабль и атакует.
        '''
        ASCIIInteface.cls()
        mass = [] #Массив кораблей в системе для удобного обращения.
        cnt = 1
        for i in self.game.ships:
            if i.system == self.scouted_star and\
            i.master != self.game.ships[self.scouted_ship].master:
                mass.append(i)
                print(str(cnt) + '. ' + i.name + ' игрока №' +\
                str(i.master) + ' (' + str(i.hp) + ' HP)')
                cnt += 1
        ship = ASCIIInteface.read_number('Выберите корабль: ')
        self.game.ships[self.scouted_ship].use(self.scouted_card, 'attack',\
        mass[ship])
        self.now_star()

    def defence(self):
        '''
        Увеличивает защиту корабля.
        '''
        self.game.ships[self.scouted_ship].use(self.scouted_card, 'defence', None)
        self.now_star()

    def move(self):
        '''
        Выбирает клетку и перемещает корабль.
        '''
        ASCIIInteface.cls()
        print('Карта:')
        print(self.game.stars[self.scouted_star].to_matrix(\
        self.game.ships[self.scouted_ship].x_y))
        print('Вы отмечены как @:')
        x = ASCIIInteface.read_number('Введите х клетки: ')
        y = ASCIIInteface.read_number('Введите y клетки: ')
        self.game.ships[self.scouted_ship].use(self.scouted_card,\
        'move', my_math.Coords(x, y))
        self.now_star()

    def end_turn(self):
        '''
        Переводит игру на следующий ход.
        '''
        ASCIIInteface.cls()
        self.game.next_turn()
        print('Хотит игрок №' + str(self.game.player))
        ASCIIInteface.wait()
        ASCIIInteface.cls()
        self.show_stars()

if __name__ == "__main__":
    TEST_INTERFACE = ASCIIInteface()
    TEST_INTERFACE.start()
