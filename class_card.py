'''
Модуль содержит всё необходимое для реализации работы карточек действий
кораблей.
'''

import copy

from my_math import rdf

class Card:
    '''
    Класс карточки-действия для корабля.
    Поля:
        inf : string -- файл с данными карточки;
        dmg : float -- урон, который позволяет наносить карточка;
        dfc : float -- урон, который позволяет поглотить карточка;
        mov : float -- перемещение, которое позволяет совершить
            карточка;
        pri : int -- приоритет восстановления карточки;
        tit : string -- название карточки;
        usb : bool -- можно ли использовать карточку;
    '''

    def __init__(self, fin):
        '''
        fin -- название карточки.
        '''
        fin = open('./data/cards/' + fin + ".txt")
        self.inf = fin
        self.dmg = float(rdf(fin))
        self.dfc = float(rdf(fin))
        self.mov = float(rdf(fin))
        self.pri = int(rdf(fin))
        self.tit = str(rdf(fin))
        self.usb = True
        fin.close()

    def get_img(self):
        '''
        Возвращает название картинки, где хранится обложка карточки.
        '''
        return './img/cards/' + self.inf + '.png'

    def __str__(self):
        '''
        Можно применять для логгирования, например, тащемта.
        '''
        string = ""
        string = string + "Карточка: " + self.tit + "\n"
        string = string + "Обложка карточки: " + self.get_img() + "\n"
        string = string + "Урон: " + str(self.dmg) + "\n"
        string = string + "Защита: " + str(self.dfc) + "\n"
        string = string + "Перемещение: " + str(self.mov) + "\n"
        string = string + "Приоритет: " + str(self.pri) + "\n"
        string = string + "Готова к использованию" + str(self.usb) + "\n"
        return string

    def cache(self):
        '''
        Функция необходима для реализации сохранения карточки.
        '''
        string = ""
        string = string + self.inf + "\n"
        string = string + str(int(self.usb)) + "\n"
        return string

    @staticmethod
    def load(fin):
        '''
        Считывает карточку из открытого файла fin.
        '''
        inf = rdf(fin)
        card = Card(inf)
        card.usb = bool(int(rdf(fin)))
        return card

class CardStore:
    '''
    Класс хранилища карточек, доступных кораблю. Де-факто, это структура
    данных, похожая на стек, но со своими фишечками.
    Поля:
        cards : [Card] -- массив карточек, доступных корабля.
    '''
    cards_nummer = 3
    @staticmethod
    def comparator(first, second):
        '''
        Компаратор для корректной сортировки хранилища карточек.
        '''
        if first.usb != second.second:
            return first.pri > second.pri
        return first.usb > second.usb

    def __init__(self, fin=None):
        '''
        fin -- название корабля, для которого генерируются карточки.
        '''
        self.cards = []
        if not fin is None:
            self.cards.append(Card(fin + '_movement'))
            self.cards.append(Card(fin + '_attack'))
            self.cards.append(Card(fin + '_defence'))

    def refresh(self):
        '''
        Сортирует карточки в следующем приоритете
        '''
        self.cards.sort(cmp=lambda first,\
            second: CardStore.comparator(first, second))

    def use(self, index):
        '''
        Использует карточку и возвращает её.
        '''
        if index < 0 or index >= len(self.cards):
            raise ValueError('Карточки с таким номером не существует!11')
        if not self.cards[index].usb:
            raise ValueError('Эта карточка ещё не восстановилась!11')
        self.cards[index].usb = False
        to_return = copy.copy(self.cards[index])
        self.refresh()
        return to_return

    def __str__(self):
        '''
        Можно применять для логгирования, например, тащемта.
        '''
        string = ""
        string = string + "Карточки корабля:\n"
        for i in self.cards:
            string = string + str(i) + "\n"
        return string

    def cache(self):
        '''
        Функция необходима для реализации сохранения карточек корабля.
        '''
        string = ""
        for i in self.cards:
            string = string + i.cache() + "\n"
        return string

    @staticmethod
    def load(fin):
        '''
        Считывает карточки корабля из открытого файла fin.
        '''
        card_store = CardStore()
        for i in range(CardStore.cards_nummer):
            card_store.cards.append(Card.load(fin))
        return card_store
