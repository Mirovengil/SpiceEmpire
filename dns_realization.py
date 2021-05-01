'''
Структура данных "Система Непересекающихся Множеств"
'''

SIZ = 1
PAR = 0

class Elem:
    '''
    Один элемент СНМ.
    '''
    def __init__(self, parent, size):
        self.parent = parent
        self.size = size
    #Геттеры и сеттеры (сгенерированы автоматически)
    def get_parent(self):
        '''Геттер поля parent'''
        return self.parent
    def set_parent(self, value):
        '''Сеттер поля parent'''
        self.parent = value
    def get_size(self):
        '''Геттер поля size'''
        return self.size
    def set_size(self, value):
        '''Сеттер поля size'''
        self.size = value


class DNS:
    '''
    СНМ, авторская реализация. Не велосипедная!
    '''

    def __init__(self, nummer):
        self.mass = []
        for i in range(nummer):
            self.mass.append([i, 1])

    def unite(self, i_1, i_2):
        '''
        Объединить два элемента СНМ.
        '''
        i_1 = self.get_parent(i_1)
        i_2 = self.get_parent(i_2)
        if self.mass[i_2][SIZ] > self.mass[i_1][SIZ]:
            i_2, i_1 = i_1, i_2
        self.mass[i_2][PAR] = i_1
        self.mass[i_1][SIZ] += self.mass[i_2][SIZ]

    def get_parent(self, i):
        '''
        Узнать корень вершины СНМ.
        '''
        if self.mass[i][PAR] == i:
            return i
        par = self.get_parent(self.mass[i][PAR])
        self.mass[i][PAR] = par
        return par
