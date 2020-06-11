"""game.py  the main battleship game (textmode)
is expecting a file (csv file with numbers for height (0-255))
"""

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