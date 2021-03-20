from random import randint
import OstTree
import mymath
from classPlanet import newPlanet
from classStar import Star
from Map import gameMap
from Map import readMap
XCR = 0; YCR = 1

def okxy(planets, x, y, mind):
    for i in planets:
        if mymath.dist(x, y, i.getCoordinates()[XCR], i.getCoordinates()[YCR]) < mind:
            return False
    return True
    
    
def getNames(place):
    stdin = open(place, 'r')
    Names = [i.replace('\n', '') for i in stdin]
    stdin.close()
    return (Names, len(Names))


def generateConstellation(Names, n, minl, maxl, namesNumber):
    graph = []
    for i in range(n): #Здесь создаётся звезда
        star = []
        numm = randint(0, namesNumber - 1)
        name = Names[numm]
        Names[numm], Names[namesNumber - 1] = Names[namesNumber - 1], Names[numm]
        namesNumber -= 1
        graph.append(Star(name, []))
    Ways = []
    for i in range(n):
        for j in range(n):
            Ways.append((randint(minl, maxl), i, j))
    Ways = OstTree.buildOstTree(n, Ways)
    for i in range(n):
        graph[i].neighbours = Ways[i]
    return graph
    

def generatePlanets(Names, n, minp, maxp, namesNumber, sizex, sizey, mind):
    graphs = []
    for i in range(n):
        planets = []
        for j in range(randint(minp, maxp)): #Здесь создаётся планета
            x, y = randint(0, sizex - 1), randint(0, sizey - 1)
            while not okxy(planets, x, y, mind):
                x, y = randint(0, sizex - 1), randint(0, sizey - 1)
            numm = randint(0, namesNumber - 1)
            name = Names[numm]
            Names[numm], Names[namesNumber - 1] = Names[namesNumber - 1], Names[numm]
            namesNumber -= 1
            planets.append(newPlanet(name, (x, y)))
        graphs.append(planets)
    return graphs
        
def generateMap(n, minp, maxp, minl, maxl, sizex, sizey, mind):
    Names, namesNumber = getNames('./data/StarsNames.txt')
    Map = gameMap()
    graph = generateConstellation(Names, n, minl, maxl, namesNumber)
    Map.setStars(graph)
    Names, namesNumber = getNames('./data/PlanetsNames.txt')
    planets = generatePlanets(Names, n, minp, maxp, namesNumber, sizex, sizey, mind)
    Map.setPlanets(planets)
    Map.setPlanets(planets)
    Map.setSize(sizex, sizey)
    return Map

if __name__ == "__main__":
    n = 10        #кол-во систем на карте
    minp = 5     #минимальное кол-во планет в системе
    maxp = 10    #максимальное кол-во планет в системе
    minl = 1     #минимальная длина пути между двумя системами
    maxl = 4     #максимальная длина пути между двумя системами
    sizex = 20    #размер системы по x
    sizey = 10    #размер системы по у
    mind = 3     #минимальное расстояние между двумя планетами (считается по Пифагору)
    #изменять можно, на своё усмотрение; нюансы: n < 324, потому что названий для звёзд пока всего 324 (можешь добавить своих);
    #работает за O(n * n) -> не стоит делать n большим, чем sqrt(10^6): питон, всё же, ме-е-едленный;
    #n * maxp < 196 (названий для планет не хватит);
    
    
    #Map = generateMap(n, minp, maxp, minl, maxl, sizex, sizey, mind)
    Map = readMap("log.txt")
    print('Читабельный вывод карты (для людей):')
    print(Map)
    print('\n\n')
    #f = open('log.txt', 'w')
    #print(Map.cache(), file = f)
    #f.close()
    

'''
Задокументировать

Planet
def getSteelHas(self,value):
    self.steelHas = value
def getFoodHas(self, value):
    self.foodHas = value
def getMoneyHas(self, value):
    self.moneyHas = value
def setImage(self, image):
    self.image = image

def readPlanet(f):
    
mymath

def rdf(f):
    return f.readline().replace("\n", "")
    
def readMap(name):

def readStar(f):
'''
