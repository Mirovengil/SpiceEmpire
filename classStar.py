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
    
    def getName(self):
        return self.name
    
    def getNeighbours(self):
        return self.neighbours
    
    def setPlanets(self, planets):
        self.planets = planets
    
    def planetsNumber(self):
        return len(self.planets)
    
    def __str__(self):
        pass
