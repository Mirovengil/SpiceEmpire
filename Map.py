from classStar import Star
from classPlanet import Planet

class gameMap:
    exist = False
    
    def __init__(self):
        if gameMap.exist:
            raise ValueError('Игровая карта может существовать только в едином экземпляре!!11 АУФ!11')
        self.stars = None
        self.shiphs = None
        self.sizex = None
        self.sizey = None
        gameMap.exist = True
    
    def setSize(self, sizex, sizey):
        self.sizex = sizex
        self.sizey = sizey
        if self.stars != None:
            for i in range(len(self.stars)):
                self.stars[i].setSize(sizex, sizey)
    
    def setStars(self, stars):
        self.stars = stars
        if self.sizex != None:
            for i in range(len(self.stars)):
                self.stars[i].setSize(sizex, sizey)
                
    def setPlanets(self, planets):
        if self.stars == None:
            raise ValueError("Сперва задайте звёзды, к которым будут прикрепляться планеты!1")
        for i in range(len(planets)):
            self.stars[i].setPlanets(planets[i])
    
    def setShips(self, ships):
        self.ships = ships
    
    def __str__(self):
        string = ""
        for i in self.stars:
           string = string + i.str(self.stars)
        return string

    def cache(self):
        string = ""
        string = string + str(self.sizex) + "\n"
        string = string + str(self.sizey) + "\n"
        string = string + str(len(self.stars)) + "\n"
        for i in self.stars:
            string = string + i.cache()
        return string
