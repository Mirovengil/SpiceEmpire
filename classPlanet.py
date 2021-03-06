XCR = 0; YCR = 1
from random import randint

class Types:
    lave = 0
    air = 1
    ice = 2
    earth = 3
    desert = 4
    rock = 5
    water = 6

def loadDescription(File):
    std = open(File, 'r')
    descr = ""
    for i in std:
        descr = descr  + i
    std.close()
    return descr

descr = dict()
descr['lave'] = loadDescription('./data/LaveDescription.txt')
descr['ice'] = loadDescription('./data/IceDescription.txt')
descr['rock'] = loadDescription('./data/RockDescription.txt')
descr['water'] = loadDescription('./data/WaterDescription.txt')
descr['air'] = loadDescription('./data/AirDescription.txt')
descr['desert'] = loadDescription('./data/DesertDescription.txt')
descr['earth'] = loadDescription('./data/EarthDescription.txt')

class Planet:
    maxBuildsNumber = 5
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates
        self.steel = None
        self.food = None
        self.money = None
        self.type = None
        self.description = 'Какой-то дурачок создал планету общего вида. Ошибка в коде, извиняйте-с.'
        self.builds = []
    #Геттеры
    def getType(self):
        return self.type
    def getName(self):
        return self.name
    def getCoordinates(self):
        return self.coordinates
    def getSteel(self):
        return self.steel
    def getFood(self):
        return self.food
    def getMoney(self): 
        return self.money
    def getDescription(self):
        return self.description
    def getPort(self):
        port = []
        for i in self.builds:
            if i.type == "port":
                port.append(i)
        return port
    def getDefence(self):
        port = []
        for i in self.builds:
            if i.type == "defence":
                port.append(i)
        return port
    def getFun(self):
        port = []
        for i in self.builds:
            if i.type == "fun":
                port.append(i)
        return port
    def getFarm(self):
        port = []
        for i in self.builds:
            if i.type == "farm":
                port.append(i)
        return port
    def getMain(self):
        port = []
        for i in self.builds:
            if i.type == "main":
                port.append(i)
        return port
    def getBuildsLen(self):
        return len(self.builds)
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
        self.description = descr['lave']
        self.type = Types.lave
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
        self.type = Types.ice
        self.description = descr['ice']
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
        self.type = Types.air
        self.description = descr['air']
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
        self.type = Types.rock
        self.money = 1
        self.description = descr['rock']
    def addFun(self, fun):
        return False
    
class Water(Planet):
    maxPortNumber = 1
    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)
        self.steel = 0.5
        self.food = 1
        self.money = 1
        self.type = Types.water
        self.description = descr['water']
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
        self.type = Types.desert
        self.description = descr['desert']
           
    
class Earth(Planet):
    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)
        self.steel = 1
        self.food = 1
        self.money = 1
        self.type = Types.earth
        self.description = descr['earth']

def newPlanet(name, coordinates):
    types = [Lave, Water, Ice, Desert, Earth, Air, Rock]
    return types[randint(0, len(types) - 1)](name, coordinates)
