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
import class_ship

TITLE_CMD = 0
CMD = 1
SIZE = 30

#Если кто не понял, речь идёт о боевой карте. Внизу используются две пары:
# (градус; координаты_перемещения)
# (градус; иллюстрация_перемещения)
#Их связь происходит через градус, так как обе пары размещены во множествах.

MY_PAIR_DEGREE = 0
MY_PAIR_COORD = 1
MY_PAIR_IMG = 1

#Типа, тащемта, ASCII-графений.
INTRO_IMG = my_math.rdf_all('./ASCII/Intro.txt')
PLANET_IMG = my_math.rdf_all('./ASCII/Planet.txt')
STAR_IMG = my_math.rdf_all("./ASCII/Star.txt")
SHIP_IMG = my_math.rdf_all("./ASCII/Ship.txt")
BATTLE_IMG = my_math.rdf_all("./ASCII/BattleSymbol.txt")
FINAL_IMG = my_math.rdf_all("./ASCII/FinishOfBattle.txt")
GMAIL = "Mirovengil@gmail.com"

MOVE_ILLUSTRATION_IMG = {
    60 : my_math.rdf_all("./ASCII/MoveIllustrationImg1.txt"),
    0: my_math.rdf_all("./ASCII/MoveIllustrationImg2.txt"),
    -60: my_math.rdf_all("./ASCII/MoveIllustrationImg3.txt"),
    -120: my_math.rdf_all("./ASCII/MoveIllustrationImg4.txt"),
    180: my_math.rdf_all("./ASCII/MoveIllustrationImg5.txt"),
    120: my_math.rdf_all("./ASCII/MoveIllustrationImg6.txt"),
}

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
        self.scouted_fleet = None
        self.using_shop_of_ships = None
        #Оный необходимо хранить, чтобы его не требовалось передавать между
        #методами покупки и удаления как параметр.

    @staticmethod
    def read_number(text):
        '''
        Считывает с клавиатуры номер чего-либо и приводит его к
        индексации.
        '''
        value = input(text)
        if value == "":
            return None
        return int(value) - 1

    @staticmethod
    def read_boolean(text):
        '''
        Считывает с клавиатуры вопрос, на который надо ответить, с припиской "(Yes/No)" и
        возвращает ответ в типе Boolean.
        '''
        value = input(text + " (Yes or No): ")
        value = value.lower()
        if len(value) < 1 or (value[0] != 'y' and value[0] != 'n'):
            return ASCIIInteface.read_boolean(text)
        return (value[0] == 'y')

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
        if not self.game is None and not self.game.battle_is_on:
            print('Ход №' + str(self.game.turn))
            print('Хотит игрок №' + str(self.game.player))
            print('Лимитов: ' + str(self.game.limits[self.game.player]))
        print('-' * SIZE)
        for i in enumerate(cmd):
            print(i[0] + 1, '. ', i[1][TITLE_CMD], sep='')
        cmd_complete = ASCIIInteface.read_number('ВВОД: ')
        if not isinstance(cmd_complete, int):
            self.print_cmd(cmd)
        if cmd_complete < 0 or cmd_complete >= len(cmd):
            self.print_cmd(cmd)
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
        if self.game.battle_is_on:
            self.draw_battle_map()
        if self.game.check_to_finish():
            self.draw_win(self.game.get_winner())
        print('Звёзды:')
        for i in enumerate(self.game.stars):
            print(i[0] + 1, '. ', (i[1].name if self.game.player in i[1].can_be_seen else 'СКРЫТО!'), sep='')
        mass = [
            ('Главное меню', ASCIIInteface.start),
            ('Просмотр звезды', ASCIIInteface.show_one_star),
            ('Просмотр флотов', ASCIIInteface.show_fleets),
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
        #Все перемещения корабля в итоге приведут к этой функции --> здесь удобно сделать
        #проверку на начало битвы (при необходимости -- переход в соответствующее меню).
        if self.game.battle_is_on:
            self.draw_battle_map()
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
                print(str(cnt) + '. ' + i.name + ' игрока №' + str(i.master))
                cnt += 1
        mass = [
            ('Главное меню', ASCIIInteface.start),
            ('Просмотр планеты', ASCIIInteface.show_planet),
            ('Просмотр корабля', ASCIIInteface.show_ship),
            ('Назад, к звёздам', ASCIIInteface.show_stars),
            ('Завершить ход', ASCIIInteface.end_turn)
        ]
        self.print_cmd(mass)

    def draw_battle_map(self):
        '''
        Отрисовывает карту, где происходит сражение.
        '''
        ASCIIInteface.cls()
        self.game.try_to_finish_battle()
        if not self.game.battle_is_on:
            print('Победил игрок №' + str(self.game.battle_map) + '!')
            ASCIIInteface.wait()
            self.show_stars()
        print(BATTLE_IMG)
        print('Идёт сражение')
        print(self.game.battle_map.str())
        print('Ходит игрок №' + str(self.game.battle_map.now_player()))
        print('Ваши корабли:')
        for ship in enumerate(self.game.battle_map.usable_ships()):
            if ship[1].is_live():
                print(str(ship[0] + 1) + ". " + ship[1].name + ' (' + str(ship[1].hp) + "HP)")
        self.scouted_ship =\
        self.game.battle_index_from_usable_to_real(ASCIIInteface.read_number('Выберите корабль: '))
        self.draw_battle_ship()

    def restore_card(self):
        '''
        Восстанавливает одну карточку кораблю и возвращает интерфейс в режим просмотра
        поля боя.
        Ход игрока, естественно, заканчивается.
        '''
        self.game.ships[self.scouted_ship].restore_card()
        self.game.battle_map.next_turn()
        self.draw_battle_map()

    def draw_battle_ship(self):
        '''
        Выводит данные (для сражения) о том корабле, который сейчас рассматривается (если
        включён режим сражения).
        '''
        ASCIIInteface.cls()
        print(self.game.battle_map.str(self.scouted_ship))
        print(self.game.battle_map.ship_info(self.scouted_ship))
        self.print_cmd([
            ('Просмотр карточки', ASCIIInteface.show_card),
            ('Использовать карточку', ASCIIInteface.use_card),
            ('Восстановить карточку', ASCIIInteface.restore_card),
            ('Назад к карте битвы', ASCIIInteface.draw_battle_map),
        ])

    def now_ship(self):
        '''
        Отрисовывает тот корабль, который рассматривали последним.
        '''
        ASCIIInteface.cls()
        print(SHIP_IMG)
        print(self.game.ships[self.scouted_ship].str(self.game.stars))
        print(self.game.stars[self.scouted_star].to_matrix(\
        self.game.ships[self.scouted_ship].x_y))
        self.print_ships_cards_list()
        mass = [
            ('Главное меню', ASCIIInteface.start),
            ('Назад к звезде', ASCIIInteface.now_star),
            ('Перемещение корабля', ASCIIInteface.move_ship_on_map)
        ]
        if self.game.ships[self.scouted_ship].on_side(self.game):
            mass.append(('Перемещение в другую систему', ASCIIInteface.change_system_for_ship))
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
        x = x if not x is None else self.game.ships[self.scouted_ship].x_y.x
        y = y if not y is None else self.game.ships[self.scouted_ship].x_y.y
        self.game.move_ship_on_global_map(self.scouted_ship, my_math.Coords(x, y))
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
        print('Дальность атаки:')
        print(self.game.show_attack_distance(self.scouted_ship, card))
        mass = [
            ('Главное меню', ASCIIInteface.start),
        ]
        if not self.game.battle_is_on:
            mass.append(('Назад к кораблю', ASCIIInteface.now_ship))
        else:
            mass.append(('Назад к кораблю', ASCIIInteface.draw_battle_map))
        self.print_cmd(mass)

    def show_ship(self):
        '''
        Отрисовывает корабль.
        '''
        self.scouted_ship = ASCIIInteface.read_number('Номер корабля: ')
        cnt = 0
        for i in enumerate(self.game.ships):
            if i[1].system == self.scouted_star:
                if cnt == self.scouted_ship:
                    self.scouted_ship = i[0]
                    break
                cnt += 1
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
        self.is_available = False
        self.print_cmd([
            ('Атака ({} ед.)'.format(card.dmg), ASCIIInteface.attack),
            ('Движение ({} ед.)'.format(card.mov), ASCIIInteface.move)
        ])

    def attack(self):
        '''
        Выбирает вражеский корабль и атакует.
        '''
        ASCIIInteface.cls()
        mass = [] #Массив кораблей в системе для удобного обращения.
        cnt = 1
        for ship in self.game.ships:
            if ship.system == self.scouted_star and\
            ship.master != self.game.ships[self.scouted_ship].master and ship in self.game.battle_map.ships:
                if ship.is_live():
                    mass.append(ship)
                    print(str(cnt) + '. ' + ship.name + ' игрока №' +\
                    str(ship.master) + ' (' + str(ship.hp) + ' HP)')
                    cnt += 1
        ship = ASCIIInteface.read_number('Выберите корабль: ')
        self.try_to_defeat(mass[ship])
        self.game.try_to_attack(self.scouted_ship, self.scouted_card, mass[ship])
        self.game.battle_map.next_turn()
        self.draw_battle_map()

    def move(self):
        '''
        Выдаёт кораблю единицы для перемещения по боевой карте и предлагает
        осуществить оное.
        '''
        ASCIIInteface.cls()
        self.game.start_ships_moving(self.scouted_ship, self.scouted_card)
        while self.game.ship_can_move_on_battle_map(self.scouted_ship):
            print('Карта:')
            ASCIIInteface.cls()
            print(self.game.battle_map.str(self.scouted_ship))
            degrees = ASCIIInteface.get_hecses_directory(self.game.battle_map, self.scouted_ship)
            place = self.game.battle_map.generate_near(\
            self.game.battle_map.ships[self.scouted_ship].battle_x_y)
            self.game.move_ship_on_battle_map(self.scouted_ship, place[degrees])
        self.game.battle_map.next_turn()
        self.draw_battle_map()

    def get_hecses_directory(battle_map, ship):
        '''
        Выводит иллюстрации для направлений движения на боевой карте.
        '''
        ASCIIInteface.cls()
        print(battle_map.str(ship))
        directories = battle_map.generate_near(battle_map.ships[ship].battle_x_y)
        places = [key for key, value in directories.items()]
        for place in enumerate(places):
            print(str(place[0] + 1) + ".\n" + MOVE_ILLUSTRATION_IMG[place[1]])
        place = ASCIIInteface.read_number('Выберите направление для перемещения: ')
        return places[place]
        ASCIIInteface.wait()

    def try_to_defeat(self, ship):
        '''
        Предлагает игроку, на корабль ship : Ship которого нападают, защититься.
        '''
        print('Игрок №' + str(self.game.battle_map.player_waits_now())\
        +', игрок №' + str(self.game.battle_map.player_turns_now()) + " напал на ваш корабль!")
        mass = ship.card_store.cards
        print('Выберите карту, чтобы защититься (просто ENTER, если не хотите)')
        for card in enumerate(mass):
            print(str(card[0] + 1) + ". " + card[1].tit + ' (' + str(card[1].dfc) + 'ед. )')
        card = ASCIIInteface.read_number('ВВОД: ')
        if card is None:
            return None
        ship.use(card, 'defence', None)

    def end_turn(self):
        '''
        Переводит игру на следующий ход.
        '''
        ASCIIInteface.cls()
        self.game.next_turn()
        print('Хотит игрок №' + str(self.game.player))
        ASCIIInteface.wait()
        ASCIIInteface.cls()
        if self.game.profit != 0:
            self.try_to_buy_ships()
        self.show_stars()

    def change_system_for_ship(self):
        '''
        Перемещает корабль в другую систему.
        '''
        for i in enumerate(self.game.stars[self.scouted_star].neighbours):
            print (str(i[0] + 1) + '. ' + self.game.stars[class_star.Star.get_neighbour(i[1])].name)
        new_star = ASCIIInteface.read_number('В какую систему-соседа вы хотите переместиться: ')
        new_star = self.game.star_index_to_normal(new_star, self.scouted_star)
        self.game.move_ship_to_system(self.scouted_ship, new_star)
        self.scouted_star = self.game.get_ships_star(self.scouted_ship)
        self.now_star()
        
    def print_ships_cards_list(self):
        '''
        Выводит карточки корабля без подробного описания.
        Вынесено в отдельную функцию, чтобы избежать повторов в коде.
        '''
        print('Карточки:')
        for ship in enumerate(self.game.ships[self.scouted_ship].card_store.cards):
            print(str(ship[0] + 1) + ". " + ship[1].tit)

    def draw_win(self, winner_index):
        '''
        Поздравляет игрока winner_index : int с победой, желает ему счастья,
        добра и далее по списку.
        '''
        print(FINAL_IMG)
        print('Поздравляем игрока №' + str(winner_index) + ' с блестящей и бесповоротной'\
        + ' победой, которую он добыл в самом трудном противостоянии в истории!')
        print('Также надеемся, что вам понравилась игра. Если так, то вы можете'\
        + ' поблагодарить её разработчиков денежкой по почтовому адресу ' + GMAIL)
        print('Чтобы перейти в главное меню, нажмите любую клавишу.')
        self.game = None
        ASCIIInteface.wait()
        self.start()

    def try_to_buy_ships(self):
        '''
        Предлагает составить список кораблей для покупки (при возможности).
        '''
        print('Вы -- игрок №' + str(self.game.player))
        self.using_shop_of_ships =\
        class_ship.ShipsShop(self.game.profit, self.game.get_limits_of_now_player(),\
        self.game.player)
        print('У вас есть столько очков для покупки: ' +\
        str(self.using_shop_of_ships.get_available_points()) + "$")
        if not ASCIIInteface.read_boolean('Вы хотите купить корабли (если нет, очки сгорят)?'):
            self.show_stars()
        #Так как функция show_stars гарантирует, что возврата в этот цикл не будет,
        #то его бесконечность вполне оправдана.
        while True:
            ASCIIInteface.cls()
            print('Вы уже заказали корабли:')
            print(self.using_shop_of_ships)
            print('У вас есть столько очков для покупки: ' +\
            str(self.using_shop_of_ships.get_available_points()) + "$")
            self.print_cmd([
                ('Заказать корабль', ASCIIInteface.buy_new_ship),
                ('Отменить заказ корабля', ASCIIInteface.delete_booked_ship),
                ('Купить и выйти', ASCIIInteface.buy_ship_and_to_stars),
                ('Выйти', ASCIIInteface.show_stars),
            ])

    def buy_new_ship(self):
        '''
        Выводит список кораблей, считывает номер покупаемого, добавляет корабль в
        список покупок.
        '''
        ASCIIInteface.cls()
        print('Доступные корабли:')
        for ship in enumerate(self.using_shop_of_ships.get_available_ships()):
            print(str(ship[0] + 1) + ". " + ship[1]['ship'] + ": " + str(ship[1]['cost']) + "$;" )
        buing_ship = ASCIIInteface.read_number('ВВОД: ')
        ASCIIInteface.cls()
        print('Доступные планеты:')
        for planet in enumerate(self.game.get_players_planets()):
            planet_object = class_ship.ShipsShop.get_planet_by_pair(planet[1], self.game)
            print(str(planet[0] + 1) + '. ' + planet_object.name + " " + str(planet_object.coordinates))
        planet = ASCIIInteface.read_number('ВВОД: ')
        system = self.game.get_players_planets()[planet]['system']
        planet = self.game.get_players_planet_by_id(planet)
        ship = self.using_shop_of_ships.get_available_ships()[buing_ship]['ship']
        self.using_shop_of_ships.add_ship_to_list(ship, system, planet)
        ASCIIInteface.cls()
        print('Корабль добавлен в список покупок!')
        ASCIIInteface.wait()


    def delete_booked_ship(self):
        '''
        Выводит список кораблей, предлагает удалить корабль из списка покупок.
        '''
        ASCIIInteface.cls()
        print('Ваши корабли:')
        print(self.using_shop_of_ships)
        delete_index = ASCIIInteface.read_number('ВВОД: ')
        self.using_shop_of_ships.remove_ship_from_list(delete_index)
        ASCIIInteface.cls()
        print('Корабль успешно удалён!')
        ASCIIInteface.cls()

    def buy_ship_and_to_stars(self):
        '''
        Покупает все выбранные корабли, выставляет их на карту и переходит на звёзду.
        '''
        self.game.add_ships(self.using_shop_of_ships.buy_ships())
        self.show_stars()

    def show_fleets(self):
        '''
        Выводит на экран список флотов, их координаты и кол-во кораблей внутри них.
        '''
        ASCIIInteface.cls()
        print('Ваши флоты:')
        fleets = self.game.get_fleets_of_player()
        for fleet in enumerate(self.game.get_fleets_of_player()):
            print(str(fleet[0] + 1) + ". Флот из " + str(fleet[1].size()) + " ед. " + str(fleet[1].x_y))
        self.print_cmd([
            ('Перейти к местоположению флота', ASCIIInteface.open_fleet_place),
            ('Просмотреть флот', ASCIIInteface.open_fleet),
            ('Назад к карте', ASCIIInteface.show_stars)
        ])

    def open_fleet_place(self):
        '''
        Считывает номер флота и переносит интерфейс на обзор
        той системы, где флот, собственно, находится. 
        '''
        fleet_number = ASCIIInteface.read_number('Номер флота: ')
        self.scouted_fleet = fleet_number
        self.show_one_fleet_place()

    def show_one_fleet_place(self):
        '''
        Переносит интерфейс на ту систему, где находится self.scouted_fleet : int.
        '''
        fleet_system = self.game.get_fleets_of_player()[self.scouted_fleet].system
        self.scouted_star = fleet_system
        self.now_star()

    def open_fleet(self):
        '''
        Выводит содержимое флота
        '''
        self.scouted_fleet = ASCIIInteface.read_number('Номер флота: ')
        ASCIIInteface.cls()
        fleet = self.game.get_fleets_of_player()[self.scouted_fleet]
        print('Флот находится в координате ' + str(fleet.x_y))
        print('Корабли флота:')
        for ship in enumerate(fleet.ships):
            print(str(ship[0] + 1) + ". " + ship[1].name)
        mass = [
            ('Перейти к местоположению флота', ASCIIInteface.show_one_fleet_place),
            ('Вывести корабль из флота', ASCIIInteface.remove_ship_from_fleet),
            ('Соединить с другим флотом', ASCIIInteface.merge_two_fleets),
            ('Переместить флот', ASCIIInteface.move_fleet),
            ('Назад к карте', ASCIIInteface.show_stars)
        ]
        if self.game.fleet_is_on_side(self.scouted_fleet):
            mass.append(('Перемещение в другую систему', ASCIIInteface.change_system_for_fleet))
        self.print_cmd(mass)

    def merge_two_fleets(self):
        '''
        Объединяет два флота в один.
        Считывает номер второго флота.
        '''
        ASCIIInteface.cls()
        print('Ваши флоты:')
        for fleet in enumerate(self.game.get_fleets_of_player()):
            print(str(fleet[0] + 1) + ". Флот из " + str(fleet[1].size()) + " ед. " + str(fleet[1] .x_y))
        other_fleet_index = ASCIIInteface.read_number('Номер второго флота: ')
        if other_fleet_index == self.scouted_fleet:
            ASCIIInteface.cls()
            print('Флот нельзя объединять с самим собой!')
            ASCIIInteface.wait()
            self.merge_two_fleets()
        self.game.merge_players_fleets(self.scouted_fleet, other_fleet_index)
        self.show_fleets()

    def remove_ship_from_fleet(self):
        '''
        Удаляет корабль из рассматриваемого флота.
        Запрашивает номер корабля.
        '''
        ship_index = ASCIIInteface.read_number('Номер удаляемого корабля: ')
        self.game.remove_ship_from_fleet(self.scouted_fleet, ship_index)
        self.show_fleets()

    def move_fleet(self):
        '''
        Выбирает клетку и перемещает флот на глобальной карте.
        На это расходуются единицы перемещения.
        '''
        ASCIIInteface.cls()
        print('Карта:')
        print(self.game.stars[self.game.fleets[self.scouted_fleet].system].to_matrix(\
        self.game.fleets[self.scouted_fleet].x_y))
        print('Вы отмечены как @:')
        x = ASCIIInteface.read_number('Введите х клетки: ')
        y = ASCIIInteface.read_number('Введите y клетки: ')
        x = x if not x is None else self.game.fleets[self.scouted_fleet].x_y.x
        y = y if not y is None else self.game.fleets[self.scouted_fleet].x_y.y
        self.game.move_fleet(self.scouted_fleet, my_math.Coords(x, y))
        self.scouted_star = self.game.get_fleets_of_player()[self.scouted_fleet].system
        self.now_star()

    def change_system_for_fleet(self):
        '''
        Если флот находится на краю системы, то он может её поменять на соседнюю.
        Считывает индекс другой системы и совершает перемещение в неё.
        '''
        print('Системы, куда вы можете переместиться:')
        self.scouted_star = self.game.fleets[self.scouted_fleet].system
        for i in enumerate(self.game.stars[self.scouted_star].neighbours):
            print(str(i[0] + 1) + ". " + self.game.stars[class_star.Star.get_neighbour(i[1])].name)
        new_star = ASCIIInteface.read_number('В какую систему-соседа вы хотите переместиться: ')
        self.game.move_fleet_to_system(self.scouted_fleet,\
        class_star.Star.get_neighbour(self.game.stars[self.scouted_star].neighbours[new_star]))
        self.scouted_star = self.game.get_fleets_star(self.scouted_fleet)
        self.now_star()
        

if __name__ == "__main__":
    TEST_INTERFACE = ASCIIInteface()
    TEST_INTERFACE.start()
