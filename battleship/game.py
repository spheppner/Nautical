"""game.py  the main battleship game (textmode)
is expecting a file (csv file with numbers for height (0-255))
"""

class Ship:
    number = 0

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.number = Ship.number
        Ship.number += 1
        #---default values ----
        self.size = 1 #
        self.description = "dummy ship"
        self.evade_chance = 0.25
        self.speed = 40
        self.fuel = 2000
        self.radar_range = 100
        self.radar_towers = 1
        self.torpedo_range = 50
        self.torpedo_launcher = 3
        self.torpedos = 0
        self.can_dive = False
        self.mines = 0
        #self.scout_planes = 0
        self.big_guns = 0
        self.medium_guns = 0
        self.small_guns = 0
        self.armor_big = 0.0
        self.armor_medium = 0.0
        self.armor_small = 0.1
        self.waterbomb_launcher = 1
        self.waterbombs = 0
        self.ammo_big = 0
        self.ammo_medium = 0
        self.ammo_small = 0
        self.mine_detection_chance = 0.1

class Corvette(Ship):

    def __init__(self,x,y):
        super().__init__(x,y)
        self.description = "small military ship, submarine-hunter and convoy protector"
        self.waterbombs = 400
        self.waterbomb_launcher = 2
        self.radar_range = 100
        self.armor_medium = 0.1
        self.armor_small = 0.8
        self.evade_chance = 0.25
        self.size = 2
        self.small_guns = 2
        self.ammo_small = 500

class Frigate(Ship):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.description = "small patrol ship, allrounder"
        self.waterbombs = 400
        self.waterbomb_launcher = 2
        self.radar_range = 100
        self.armor_small = 0.9
        self.armor_medium = 0.15
        self.radar_towers = 1
        self.radar_range = 150
        self.waterbomb_launcher = 1
        self.waterbombs = 200
        self.torpedo_launcher = 2
        self.torpedos = 12

        self.evade_chance = 0.15
        self.size = 2
        self.small_guns = 4
        self.medium_guns = 2
        self.ammo_small = 1000
        self.ammo_medium = 200







class Game:

    world = []  # list of list
    width = 0
    height = 0
    fleets = []
    startpoints = []

    def __init__(self, mapfile="map001.csv", starpoints="map001_startpoints.csv"):
        with open(mapfile) as f:
            lines = f.readlines()
        for line in lines:
            textvalues = line.split(",")[:-1]
            intvalues = [int(x) for x in textvalues]
            Game.world.append(intvalues)
        Game.width = len(Game.world[0])
        Game.height = len(Game.world)

        with open(starpoints) as f:
            lines = f.readlines()
        for line in lines:
            x,y = line.split(",")
            x = int(x)
            y = int(y)
            Game.startpoints.append((x,y))

        print("----- game world {} x {}".format(Game.width, Game.height))
        for line in Game.world:
            print(line)
        print("-----startpoints----")
        print(Game.startpoints)

if __name__ == "__main__":
    g = Game()