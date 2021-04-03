import mymath
from mymath import rdf
class Ship:
    max_dist = {
        "fast" : 18**0.5 + 0.01,
        "medium" : 8**0.5 + 0.01, 
        "low" : 2**0.5 + 0.01    
    }
    
    def __init__(self):
        self.cost = None
        self.heal = None
        self.xy = mymath.Coords()
        self.system = None
        self.fly_to = mymath.Coords()
        self.hp = 100 #percents
        self.damage = None
        self.defence = None
        self.img = None
        self.speed = None
        self.name = None #name of ship's type
        self.visible_to = []
        self.master = None

    def set_target(self, target):
        if mymath.dist(self.xy, target) < self.speed:
            self.fly_to = target
            return True
        else:
            return False
            
    def move(self):
        self.xy = self.fly_to
    
    def add_visible_to(self, value):
        self.visible_to.append(value)
        
    def heal_self(self):
        self.hp += self.heal
        if self.hp > 100:
            self.hp = 100
    
    def is_live(self):
        return self.hp > 0
        
    def is_died(self):
        return not self.is_live()
    
    #Геттеры и сеттеры (сгенерированы автоматически)
    def get_master(self):
        return self.master
    def set_master(self, value):
        self.master = value
    def get_system(self):
        return self.system
    def set_system(self, value):
        self.system = value
    def get_xy(self):
        return self.xy
    def set_xy(self, value):
        self.xy = value
        if self.fly_to == mymath.Coords():
            self.fly_to = value
    def get_fly_to(self):
        return self.fly_to
    def get_hp(self):
        return self.hp
    def set_hp(self, value):
        self.hp = value
    def get_damage(self):
        return self.damage
    def set_damage(self, value):
        self.damage = value
    def get_defence(self):
        return self.defence
    def set_defence(self, value):
        self.defence = value
    def get_img(self):
        return self.img
    def set_img(self, value):
        self.img = value
    def get_speed(self):
        return self.speed
    def set_speed(self, value):
        self.speed = value
    def get_name(self):
        return self.name
    def set_name(self, value):
        self.name = value
    def get_visible_to(self):
        return self.visible_to
    def get_cost(self):
        return self.cost
    def set_cost(self, value):
        self.cost = value
    def get_heal(self):
        return self.heal
    def set_heal(self, value):
        self.heal = value

    def str(self, systems):
        string = ""
        string = string + "Тип корабля: {}".format(self.name) + "\n"
        string = string + 'HP: {}'.format(str(self.hp)) + "\n"
        string = string + "Координаты корабля: {}".format(str(self.xy)) + "\n"
        string = string + "Корабль летит в: {}".format(str(self.fly_to)) + "\n"
        string = string + "Хозяин корабля: игрок номер {}".format(str(self.master)) + "\n"
        string = string + "Корабль находится в системе {}".format(systems[self.system].getName()) + "\n"
        string = string + "Корабль видят игроки под номерами: {}".format(str(self.visible_to)) + "\n"        
        return string
        
    def cache(self):
        string = ""
        string = string + self.name + "\n"
        string = string + str(self.hp) + "\n"
        string = string + str(self.xy) + "\n"
        string = string + str(self.fly_to) + "\n"
        string = string + str(self.master) + "\n"
        string = string + str(self.system) + "\n"
        string = string + str(len(self.visible_to)) + "\n"        
        for i in self.visible_to:
            string = string + str(i) + "\n"  
        return string

class Ninja(Ship):
    def __init__(self):
        super().__init__()
        self.cost = 100
        self.heal = 0
        self.damage = 50
        self.defence = 0
        self.img = "img/ships/ninja.png"
        self.speed = Ship.max_dist['fast']
        self.name = 'Невидимка'

    def add_visible_to(self, value):
        return "Lolwhut?"
        
    def get_visible_to(self):
        return [self.master]

class Scout(Ship):
    def __init__(self):
        super().__init__()
        self.cost = 20
        self.heal = 5
        self.damage = 0
        self.defence = 0
        self.img = "img/ships/scout.png"
        self.speed = Ship.max_dist['fast']
        self.name = 'Разведчик'

name_to_class = {
    "Разведчик" : Scout,
    "Невидимка" : Ninja
}

def readShip(f):
    ship = name_to_class[rdf(f)]()
    hp = int(rdf(f))
    xy = rdf(f).replace(")", "").replace("(", "").split(", ")
    fly_to = rdf(f).replace(")", "").replace("(", "").split(", ")
    master = int(rdf(f))
    system = int(rdf(f))
    n = int(rdf(f))
    for i in range(n):
        ship.add_visible_to(int(rdf(f)))
    ship.set_hp(hp)
    ship.set_xy(mymath.Coords(int(xy[0]), int(xy[1])))
    ship.set_target(mymath.Coords(int(fly_to[0]), int(fly_to[1])))
    ship.set_master(master)
    ship.set_system(system)
    return ship
