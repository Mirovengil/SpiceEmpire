class Ship_cmd:
    def __init__(self, ship):
        self.ship = ship
    
    def do(self):
        raise ValueError("АБСТРАКТНЫЙ МЕТОД, ЕТИЖИ-ПАССАТИЖИ!")

class Move(Ship_cmd):
    def do(self):
        pass

class Fix(Ship_cmd):
    def do(self):
        pass

class Move(Ship_cmd):
    def do(self):
        pass

class Ship:
    max_dist = {
    "fast" : 18**0.5,
    "medium" : 8**0.5, 
    "low" : 2**0.5    
    }
    
    def __init__(self):
        self.xy = (None, None)
        self.fly_to = (None, None)
        self.hp = 100 #percents
        self.damage = None
        self.defence = None
        self.special_cmd = [] #special abilityes of ship
        self.img = None
        self.speed = None
        self.name = None #name of ship's type
        self.visible_to = []

    #Геттеры и сеттеры (сгенерированы автоматически)
    def get_xy(self):
        return self.xy
    def set_xy(self, value):
        self.xy = value
    def get_fly_to(self):
        return self.fly_to
    def set_fly_to(self, value):
        self.fly_to = value
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
    def get_special_cmd(self):
        return self.special_cmd
    def set_special_cmd(self, value):
        self.special_cmd = value
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
    def set_visible_to(self, value):
        self.visible_to = value
