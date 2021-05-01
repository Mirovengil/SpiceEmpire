'''
Сий чудо-модуль содержит авторскую реализацию типа данных СНМ (Система
Непересекающихся множеств), простую, как угол дома, и надёжную, как
кувалда. С ней можно вытворять следующие вещи:
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
        '''
        nummer : int -- кол-во элементов в создаваемой СНМ;
        '''
        self.mass = []
        for i in range(nummer):
            self.mass.append([i, 1])

    def unite(self, i_1, i_2):
        '''
        i_1 : int и i_2 : int -- номера объединяемых элементов;
        '''
        i_1 = self.get_parent(i_1)
        i_2 = self.get_parent(i_2)
        if self.mass[i_2][SIZ] > self.mass[i_1][SIZ]:
            i_2, i_1 = i_1, i_2
        self.mass[i_2][PAR] = i_1
        self.mass[i_1][SIZ] += self.mass[i_2][SIZ]

    def get_parent(self, i):
        '''
        i : int -- номер элемента, корень которого надо получить;
        '''
        if self.mass[i][PAR] == i:
            return i
        par = self.get_parent(self.mass[i][PAR])
        self.mass[i][PAR] = par
        return par

'''
Важно: если читающему это что-то скажет, то здесь использована
оптимизация через логистику по размеру.
'''
