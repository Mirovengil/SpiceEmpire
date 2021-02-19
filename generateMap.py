from random import randint
import OstTree

CNS = 0; PLN = 1
NAM = 0; NPL = 1; WYS = 2
PLC = 0; LEN = 1
CLR = 1; COR = 2; 
XCR = 0; YCR = 1

def getStarsNames(place):
    stdin = open(place, 'r')
    Names = [i.replace('\n', '') for i in stdin]
    return (Names, len(Names))

def generateConstellation(Names, n, minl, maxl, namesNumber):
    graph = []
    for i in range(n):
        star = []
        numm = randint(0, namesNumber)
        star.append(Names[numm])
        Names[numm], Names[namesNumber - 1] = Names[namesNumber - 1], Names[numm]
        namesNumber -= 1
        star.append(0)
        star.append([])
        graph.append(star)
    Ways = []
    for i in range(n):
        for j in range(n):
            Ways.append((randint(minl, maxl), i, j))
    Ways = OstTree.buildOstTree(n, Ways)
    for i in range(n):
        graph[i][WYS] = Ways[i]
    return graph
    
def generateMap(n, minp, maxp, minl, maxl):
    Names, namesNumber = getStarsNames('StarsNames.txt')
    Map = []
    graph = generateConstellation(Names, n, minl, maxl, namesNumber)
    Map.append(graph)
    return Map
    
def printSystems(systems):
    #Пока только систем, планеты не выводятся:
    for i in systems[CNS]:
        print('Название звезды:', i[NAM])
        print('Кол-во планет:', i[NPL])
        print('Соседи:')
        for j in i[WYS]:
            print('    >', systems[CNS][j[1]][NAM], '  (', j[0], 'ПА', ')')


if __name__ == "__main__":
    n = 7       #кол-во систем на карте
    minp = 5     #минимальное кол-во планет в системе
    maxp = 10    #максимальное кол-во планет в системе
    minl = 1     #минимальная длина пути между двумя системами
    maxl = 4    #максимальная длина пути между двумя системами
    #изменять можно, на своё усмотрение; нюансы: n < 324, потому что названий для звёзд пока всего 324 (можешь добавить своих);
    #работает за O(n * n) -> не стоит делать n большим, чем sqrt(10^6): питон, всё же, ме-е-едленный;
    systems = generateMap(n, minp, maxp, minl, maxl)
    printSystems(systems)

