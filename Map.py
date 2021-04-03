from classStar import Star
from classPlanet import Planet
from mymath import rdf
from classShip import readShip

class gameMap:
    def __init__(self):
        self.stars = []
        self.ships = []
        self.sizex = None
        self.sizey = None
    
    def setSize(self, sizex, sizey):
        self.sizex = sizex
        self.sizey = sizey
        if self.stars != None:
            for i in range(len(self.stars)):
                self.stars[i].setSize(self.sizex, self.sizey)
    
    def setStars(self, stars):
        self.stars = stars
        if self.sizex != None:
            for i in range(len(self.stars)):
                self.stars[i].setSize(self.sizex, self.sizey)
                
    def setPlanets(self, planets):
        if self.stars == None:
            raise ValueError("Сперва задайте звёзды, к которым будут прикрепляться планеты!1")
        for i in range(len(planets)):
            self.stars[i].setPlanets(planets[i])
    
    def setShips(self, ships):
        self.ships = ships
    
    def addShip(self, ship):
        self.ships.append(ship)
    
    def __str__(self):
        string = "Звёзды\n\n"
        for i in self.stars:
           string = string + i.str(self.stars)
        string = string + 'Корабли\n'
        for i in self.ships:
            string = string + i.str(self.stars)
        return string

    def next_turn(self):
        for i in range(len(self.ships)):
            if self.ships[i].get_xy() == self.ships[i].get_fly_to():
                self.ships[i].heal_self()
            self.ships[i].move()
        

    def cache(self):
        string = ""
        string = string + str(self.sizex) + "\n"
        string = string + str(self.sizey) + "\n"
        string = string + str(len(self.stars)) + "\n"
        for i in self.stars:
            string = string + i.cache()
        string = string + str(len(self.ships)) + "\n"
        for i in self.ships:
            string = string + i.cache()
        return string

    @staticmethod
    def readMap(name):
        Map = gameMap()
        f = open(name, 'r')
        sizex = int(rdf(f))
        sizey = int(rdf(f))
        n = int(rdf(f))
        rez = gameMap()
        rez.setSize(sizex, sizey)
        rez.setStars([Star.readStar(f) for i in range(n)])
        n = int(rdf(f))
        rez.setShips([readShip(f) for i in range(n)])
        f.close()
        return rez    
    
