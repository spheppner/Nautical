"""game.py  the main battleship game (textmode)
is expecting a file (csv file with numbers for height (0-255))
"""

class Game:
    world = []  # list of list
    width = 0
    height = 0

    def __init__(self, mapfile="map001.csv"):
        with open(mapfile) as f:
            lines = f.readlines()
        for line in lines:
            Game.world.append(line.split(",")[:-1])
        Game.width = len(Game.world[0])
        Game.height = len(Game.world)

        print("----- game world {} x {}".format(Game.width, Game.height))
        for line in Game.world:
            print(line)

if __name__ == "__main__":
    g = Game()