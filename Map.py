from classStar import Star
from classPlanet import Planet

class gameMap:
    exist = False
    
    def __init__(self):
        if gameMap.exist:
            raise ValueError('Игровая карта может существовать только в едином экземпляре!!11 АУФ!11')
        self.stars = None
        self.shiphs = None
        self.sizex = 0
        self.sizey = 0
        gameMap.exist = True
    
    def setSize(self, sizex, sizey):
        self.sizex = sizex
        self.sizey = sizey
    
    def setStars(self, stars):
        self.stars = stars
        
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
            temp_coords = []
            string = string + "-------------------------------------------------------" + "\n"
            string = string + 'Название звезды: ' + str(i.name) + "\n"
            string = string + 'Кол-во планет: ' + str(i.planetsNumber()) + "\n"
            string = string + 'Соседи: ' + "\n"
            for j in i.getNeighbours():
                string = string + '    >' + self.stars[Star.getNeighbour(j)].getName() + ' (' + str(Star.getWayLen(j)) +  'ПА' +  ')' + "\n"
            string = string + "\n"
            string = string + 'Планеты: ' + "\n"
            for j in i.planets:
                string = string + '      > Название планеты: ' + j.getName() + "\n"
                string = string + '           Стратегический тип планеты: ' + Planet.typeToStr(j.getType()) + "\n"
                string = string + '           Описание планеты: ' + j.getDescription() + "\n"
                string = string + '           Координаты в системе: ' + str(j.getCoordinates()) + "\n"
                string = string + '           Изображение: ' + j.getImage() + "\n"
                string = string + '           Скорость добычи стали у одного завода: ' + str(int(j.getSteel() * 100)) + '%' + "\n"
                string = string + '           Скорость добычи еды у одной фермы: ' + str(int(j.getFood() * 100)) + '%' + "\n"
                string = string + '           Скорость получения денег у одного порта: ' + str(int(j.getMoney() * 100)) + '%' + "\n"
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
