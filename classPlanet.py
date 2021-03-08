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

img = dict()
img['lave'] = ('lave_img_1.png', 'lave_img_2.png', 'lave_img_3.png', 'lave_img_4.png')
img['ice'] = ('ice_img_1.png', 'ice_img_2.png', 'ice_img_3.png', 'ice_img_4.png')
img['air'] = ('air_img_1.png', 'air_img_2.png', 'air_img_3.png', 'air_img_4.png')
img['water'] = ('water_img_1.png', 'water_img_2.png', 'water_img_3.png', 'water_img_4.png')
img['rock'] = ('rock_img_1.png', 'rock_img_2.png', 'rock_img_3.png', 'rock_img_4.png')
img['desert'] = ('desert_img_1.png', 'desert_img_2.png', 'desert_img_3.png', 'desert_img_4.png')
img['earth'] = ('earth_img_1.png', 'earth_img_2.png', 'earth_img_3.png', 'earth_img_4.png')

class Planet:

    @staticmethod
    def typeToStr(planetType):
        if planetType == Types.air:
            return "Газовая"
        if planetType == Types.desert:
            return "Пустынная"
        if planetType == Types.rock:
            return "Скалистая"
        if planetType == Types.lave:
            return "Лавовая"
        if planetType == Types.water:
            return "Водяная"
        if planetType == Types.ice:
            return "Ледяная"
        if planetType == Types.earth:
            return "Земного типа"
        return "ЧТО ЗА ХРЕНЬ ВЫ ПЕРЕДАЛИ В ПАРАМЕТРЫ!? ПЕРЕДАЙТЕ, пожалуйста, СУЩЕСТВУЮЩИЙ ТИП ПЛАНЕТЫ!"
    
    maxBuildsNumber = 5
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates
        self.steel = None
        self.food = None
        self.money = None
        self.type = None
        self.image = None
        self.steelHas = 0
        self.foodHas = 0
        self.moneyHas = 0
        self.description = 'Какой-то дурачок создал планету общего вида. Ошибка в коде, извиняйте-с.' #Возможно,
        #вы имеете счастье наблюдать планету-затычку, которая изображает звезду. Сделано это для того, чтобы обеспечить
        #отсутствие планет на определённом расстоянии от того места, где в графическом интерфейсе будет изображаться звезда.
        self.builds = []
    #Геттеры
    def getSteelHas(self):
        return self.steelHas
    def getFoodHas(self):
        return self.foodHas
    def getMoneyHas(self):
        return self.moneyHas
    def addSteel(self, value):
        self.steelHas += value
    def addFood(self, value):
        self.foodHas += value
    def addMoney(self, value):
        self.moneyHas += value
    def getImage(self):
        return self.image
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

    def __str__(self):
        string = ""
        string = string + '      > Название планеты: ' + self.getName() + "\n"
        string = string + '           Стратегический тип планеты: ' + Planet.typeToStr(self.getType()) + "\n"
        string = string + '           Описание планеты: ' + self.getDescription() + "\n"
        string = string + '           Координаты в системе: ' + str(self.getCoordinates()) + "\n"
        string = string + '           Изображение: ' + self.getImage() + "\n"
        string = string + '           Скорость добычи стали у одного завода: ' + str(int(self.getSteel() * 100)) + '%' + "\n"
        string = string + '           Скорость добычи еды у одной фермы: ' + str(int(self.getFood() * 100)) + '%' + "\n"
        string = string + '           Скорость получения денег у одного порта: ' + str(int(self.getMoney() * 100)) + '%' + "\n"
        return string
        
class Lave(Planet):
    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)
        self.steel = 1
        self.food = 0
        self.money = 1
        self.description = descr['lave']
        self.type = Types.lave
        self.image = img['lave'][randint(0, len(img['lave']) - 1)]
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
        self.image = img['ice'][randint(0, len(img['ice']) - 1)]
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
        self.image = img['air'][randint(0, len(img['air']) - 1)]
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
        self.image = img['rock'][randint(0, len(img['rock']) - 1)]
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
        self.image = img['water'][randint(0, len(img['water']) - 1)]
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
        self.image = img['desert'][randint(0, len(img['desert']) - 1)]
        
    
class Earth(Planet):
    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)
        self.steel = 1
        self.food = 1
        self.money = 1
        self.type = Types.earth
        self.description = descr['earth']
        self.image = img['earth'][randint(0, len(img['earth']) - 1)]

def newPlanet(name, coordinates):
    types = [Lave, Water, Ice, Desert, Earth, Air, Rock]
    return types[randint(0, len(types) - 1)](name, coordinates)
