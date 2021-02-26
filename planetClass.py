XCR = 0; YCR = 1
from random import randint

def loadDescription(File):
    std = open(File, 'r')
    descr = ""
    for i in std:
        descr = descr  + i
    std.close()
    return descr

class Planet:
    maxBuildsNumber = 5
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates
        self.steel = None
        self.food = None
        self.money = None
        self.description = 'Какой-то дурачок создал планету общего вида. Ошибка в коде, извиняйте-с.'
        self.port = []
        self.defence = []
        self.fun = []
        self.farm = []
        self.main = [] 
    #Геттеры
    def getSteel(self):
        return self.steel
    def getFood(self):
        return self.food
    def getMoney(self): 
        return self.money
    def getDescription(self):
        return self.description
    def getPort(self):
        return self.port
    def getDefence(self):
        return self.defence
    def getFun(self):
        return self.fun
    def getFarm(self):
        return self.farm
    def getMain(self):
        return self.main
    def getBuildsLen(self):
        summ = 0
        summ += len(self.getPort())
        summ += len(self.getDefence())
        summ += len(self.getFun())
        summ += len(self.getFarm())
        summ += len(self.getMain())
        return summ
    #Добавление построек
    def addPort(self, port):
        if self.getBuildsLen() < Planet.maxBuildsNumber:
            self.port.append(port)
            return True
        return False
    def addDefence(self, defence):
        if self.getBuildsLen() < Planet.maxBuildsNumber:
            self.defence.append(defence)
            return True
        return False
    def addFun(self, fun):
        if self.getBuildsLen() < Planet.maxBuildsNumber:
            self.fun.append(fun)
            return True
        return False
    def addFarm(self, farm):
        if self.getBuildsLen() < Planet.maxBuildsNumber:
            self.farm.append(farm)
            return True
        return False
    def addMain(self, main):
        if self.getBuildsLen() < Planet.maxBuildsNumber:
            self.main.append(main)
            return True
        return False


class Lave(Planet):
    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)
        self.steel = 1
        self.food = 0
        self.money = 1
        self.description = loadDescription('./data/LaveDescription.txt')
    def addFarm(self, farm):
        return False
    def addFun(self, fun):
        return False


class Ice(Planet):
    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)
        self.steel = 0.5
        self.food = 0
        self.money = 1
        self.description = loadDescription('./data/IceDescription.txt')
    def addFarm(self, farm):
        return False
    def addFun(self, fun):
        return False
    
    
class Air(Planet):
    maxDefenceNumber = 1
    maxPortNumber = 1
    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)
        self.steel = 0
        self.food = 0
        self.money = 2
        self.description = loadDescription('./data/AirDescription.txt')
    def addFun(self, fun):
        return False
    def addFarm(self, farm):
        return False
    def addMain(self, main):
        return False
    def addPort(self, port):
        if self.getBuildsLen() < Air.maxPortNumber:
            self.port.append(port)
            return True
        return False
    def addDefence(self, defence):
        if self.getBuildsLen() < Air.maxDefenceNumber:
            self.defence.append(defence)
            return True
        return False
        
        
class Rock(Planet):
    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)
        self.steel = 2
        self.food = 0.5
        self.money = 1
        self.description = loadDescription('./data/RockDescription.txt')
    def addFun(self, fun):
        return False
    
class Water(Planet):
    maxPortNumber = 1
    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)
        self.steel = 0.5
        self.food = 1
        self.money = 1
        self.description = loadDescription('./data/WaterDescription.txt')
    def addPort(self, port):
        if self.getBuildsLen() < Water.maxPortNumber:
            self.port.append(port)
            return True
        return False    
    
class Desert(Planet):
    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)
        self.steel = 1
        self.food = 0.5
        self.money = 1
        self.description = loadDescription('./data/DesertDescription.txt')
    
    
class Earth(Planet):
    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)
        self.steel = 1
        self.food = 1
        self.money = 1
        self.description = loadDescription('./data/EarthDescription.txt')

def newPlanet(name, coordinates):
    types = [Lave, Water, Ice, Desert, Earth, Air, Rock]
    return types[randint(0, len(types) - 1)](name, coordinates)
