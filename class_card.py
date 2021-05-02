'''
Модуль содержит всё необходимое для реализации работы карточек действий
кораблей.
'''

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

    def load(self, fin):
        '''
        Считывает карточку из открытого файла fin.
        '''
        inf = rdf(fin)
        self.__init__(inf)
        self.usb = bool(int(rdf(fin)))
