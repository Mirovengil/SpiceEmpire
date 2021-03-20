from mymath import rdf
from classPlanet import readPlanet

class Star: 
    @staticmethod
    def getNeighbour(way):
        return way[1]
        
    @staticmethod
    def getWayLen(way):
        return way[0]
        
    def __init__(self, name, neighbours):
        self.name = name
        self.neighbours = neighbours
        self.planets = None
        self.sizex = 0
        self.sizey = 0
    
    def setSize(self, sizex, sizey):
        self.sizex = sizex
        self.sizey = sizey

    def getName(self):
        return self.name
    
    def getNeighbours(self):
        return self.neighbours
    
    def setPlanets(self, planets):
        self.planets = planets
    
    def planetsNumber(self):
        return len(self.planets)
    
    def str(self, other):
        string = ""
        temp_coords = []
        string = string + "-------------------------------------------------------" + "\n"
        string = string + 'Название звезды: ' + str(self.name) + "\n"
        string = string + 'Кол-во планет: ' + str(self.planetsNumber()) + "\n"
        string = string + 'Соседи: ' + "\n"
        for j in self.getNeighbours():
            string = string + '    > ' + other[Star.getNeighbour(j)].getName() + ' (' + str(Star.getWayLen(j)) +  'ПА' +  ')' + "\n"
        string = string + "\n"
        string = string + 'Планеты: ' + "\n"
        for j in self.planets:
            string = string + str(j)
            temp_coords.append(j.getCoordinates())
        string = string + "Положение планет: " + "\n"
        for y in range(self.sizey):
            for x in range(self.sizex):
                if (x, y) in temp_coords:
                    string = string + " *"
                else:
                    string = string + " _"
            string = string + "\n"
        string = string + '-------------------------------------------------------' + "\n"
        return string
    
    def cache(self):
        string = ""
        string = string + self.name + "\n"
        string = string + str(len(self.neighbours)) + "\n"
        for i in self.neighbours:
            string = string + str(i[0]) + "\n"
            string = string + str(i[1]) + "\n"
        string = string + str(len(self.planets)) + "\n"
        for i in self.planets:
            string = string + i.cache()
        return string


def readStar(f):
    name = str(rdf(f))
    n = int(rdf(f))
    neighbours = []
    for i in range(n):
        wayLen = int(rdf(f))
        wayTarget = int(rdf(f))
        neighbours.append((wayLen, wayTarget))
    n = int(rdf(f))
    planets = [readPlanet(f) for i in range(n)]
    rez = Star(name, neighbours)
    rez.setPlanets(planets)
    return rez
    
