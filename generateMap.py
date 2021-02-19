from random import randint
import OstTree
import mymath
from classPlanet import Planet
from classStar import Star

CNS = 0; PLN = 1
XCR = 0; YCR = 1

COLORS = [
'magmatic',
'waterfull',
'green',
'desert',
'Earth',
'gase',
'rock'
]

def okxy(planets, x, y, mind):
    for i in planets:
        if mymath.dist(x, y, i.coordinates[XCR], i.coordinates[YCR]) < mind:
            return False
    return True
    
    
def getNames(place):
    stdin = open(place, 'r')
    Names = [i.replace('\n', '') for i in stdin]
    return (Names, len(Names))


def generateConstellation(Names, n, minl, maxl, namesNumber):
    graph = []
    for i in range(n):
        star = []
        numm = randint(0, namesNumber - 1)
        name = Names[numm]
        Names[numm], Names[namesNumber - 1] = Names[namesNumber - 1], Names[numm]
        namesNumber -= 1
        graph.append(Star(name, 0, []))
    Ways = []
    for i in range(n):
        for j in range(n):
            Ways.append((randint(minl, maxl), i, j))
    Ways = OstTree.buildOstTree(n, Ways)
    for i in range(n):
        graph[i].neighbours = Ways[i]
    return graph
    

def generatePlanets(Names, n, minp, maxp, namesNumber, size, mind):
    graphs = []
    for i in range(n):
        planets = []
        for j in range(randint(minp, maxp)):
            x, y = randint(0, size - 1), randint(0, size - 1)
            while not okxy(planets, x, y, mind):
                x, y = randint(0, size - 1), randint(0, size - 1)
            numm = randint(0, namesNumber - 1)
            name = Names[numm]
            Names[numm], Names[namesNumber - 1] = Names[namesNumber - 1], Names[numm]
            namesNumber -= 1
            typ = COLORS[randint(0, len(COLORS) - 1)]
            planets.append(Planet(name, typ, (x, y)))
        graphs.append(planets)
    return graphs
        
def generateMap(n, minp, maxp, minl, maxl, size, mind):
    Names, namesNumber = getNames('StarsNames.txt')
    Map = []
    graph = generateConstellation(Names, n, minl, maxl, namesNumber)
    Map.append(graph)
    Names, namesNumber = getNames('PlanetsNames.txt')
    planets = generatePlanets(Names, n, minp, maxp, namesNumber, size, mind)
    Map.append(planets)
    for i in range(n):
        Map[CNS][i].planetsNumber = len(Map[PLN][i])
    return Map
    
def printSystems(systems, size):
    cnt = 0
    for i in systems[CNS]:
        print('-------------------------------------------------------')
        print('Название звезды:', i.name)
        print('Кол-во планет:', i.planetsNumber)
        print('Соседи:')
        for j in i.neighbours:
            print('    >', systems[CNS][j[1]].name, '  (', j[0], 'ПА', ')')
        view = []
        print('Планеты:')
        for j in systems[PLN][cnt]:
            print('      > Название планеты:', j.name)
            print('           Тип планеты:', j.typ)
            print('           Координаты в системе:', j.coordinates)
            view.append(j.coordinates)
            print()
        cnt += 1
        print('Внешний вид:')
        for j in range(size):
            print('           ', end = '')
            for k in range(size):
                if (j, k) in view:
                    print('*', end = ' ')
                else:
                    print('_', end = ' ')
            print()
    print('-------------------------------------------------------')

if __name__ == "__main__":
    n = 7        #кол-во систем на карте
    minp = 5     #минимальное кол-во планет в системе
    maxp = 10    #максимальное кол-во планет в системе
    minl = 1     #минимальная длина пути между двумя системами
    maxl = 4     #максимальная длина пути между двумя системами
    size = 15    #размер системы по xy (x == y)
    mind = 3     #минимальное расстояние между двумя планетами (считается по Пифагору)
    #изменять можно, на своё усмотрение; нюансы: n < 324, потому что названий для звёзд пока всего 324 (можешь добавить своих);
    #работает за O(n * n) -> не стоит делать n большим, чем sqrt(10^6): питон, всё же, ме-е-едленный;
    #n * maxp < 196 (названий для планет не хватит);
    systems = generateMap(n, minp, maxp, minl, maxl, size, mind)
    printSystems(systems, size)

