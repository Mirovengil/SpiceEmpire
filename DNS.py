#Структура данных "Система Непересекающихся Множеств"

SIZ = 1; PAR = 0
class DNS:
    def __init__(self, n):
        self.mass = []
        for i in range(n):
            self.mass.append([i, 1])
    
    def unite(self, i1, i2):
        i1 = self.get_parent(i1)
        i2 = self.get_parent(i2)
        if self.mass[i2][SIZ] > self.mass[i1][SIZ]:
            i2, i1 = i1, i2
        self.mass[i2][PAR] = i1
        self.mass[i1][SIZ] += self.mass[i2][SIZ]
        
    def get_parent(self, i):
        if self.mass[i][PAR] == i:
            return i
        par = self.get_parent(self.mass[i][PAR])
        self.mass[i][PAR] = par
        return par

