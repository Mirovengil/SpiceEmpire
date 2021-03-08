from classStar import Star
from planetClass import Planet

class gameMap:
    exist = False
    
    def __init__(self):
        if gameMap.exist:
            raise ValueError('Игровая карта может существовать только в едином экземпляре!!11 АУФ!11')
        self.stars = None
        self.shiphs = None
        gameMap.exist = True
    
    def setStars(self, stars):
        self.stars = stars
        
    def setPlanets(self, planets):
        if stars == None:
            raise ValueError("Сперва задайте звёзды, к которым будут прикрепляться планеты!1")
        for i in range(len(planets)):
            self.stars[i].setPlanets(planets[i])
    
    def setShips(self, ships):
        self.ships = ships
    
    def __str__(self):
        string = ""
        for i in self.stars:
            string = string + "-------------------------------------------------------" + "\n"
            string = string + 'Название звезды: ' + str(i.name) + "\n"
            string = string + 'Кол-во планет: ' + str(i.planetsNumber()) + "\n"
            string = string + 'Соседи: ' + "\n"
            for j in i.neighbours:
                string = string + '    >' + Star.getNeighbour(j).getName() + ' (' + str(Star.getWayLen(j)) +  'ПА' +  ')' + "\n"
            string = string + 'Планеты: ' + "\n"
            for j in i.planets:
                string = string + '      > Название планеты: ' + j.getName() + "\n"
                string = string + '           Стратегический тип планеты: ' + j.getType() + "\n"
                string = string + '           Описание планеты: ' + j.getDescription() + "\n"
                string = string + '           Координаты в системе: ' + j.getCoordinates() + "\n"
                string = string + '           Изображение: ' + j.getImage() + "\n"
                string = string + '           Скорость добычи стали у одного завода: ' + int(j.getSteel() * 100) + '%' + "\n"
                string = string + '           Скорость добычи еды у одной фермы: ' + int(j.getFood() * 100) + '%' + "\n"
                string = string + '           Скорость получения денег у одного порта: ' + int(j.getMoney() * 100) + '%' + "\n"
            string = string + '-------------------------------------------------------' + "\n"
        
