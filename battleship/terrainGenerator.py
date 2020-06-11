import random

def getNeighbours(x, y, terrain):
    neighbours = []
    
    return neighbours

def generateTerrain(tiles_x=20, tiles_y=20):
    terrain = []

    h = 60
    # ----- 1st run -----
    # Basis-Höhe setzen
    for y in range(tiles_y):
        line = []
        for x in range(tiles_x):
            height = h
            line.append(height)
        terrain.append(line)
        
    # ----- 2nd run -----
    # Zufälliges Höhen-Verändern der Felder
    for y in range(tiles_y):
        for x in range(tiles_x):
            old = terrain[y][x]
            new = old + random.gauss(-90, -100)
            new = min(255, new)
            new = max(0, new)
            terrain[y][x] = round(new)
            
    # ----- 3rd run -----
    # Landmasse rundherum
    for y in range(tiles_y):
        for x in range(tiles_x):
            for (posy,posx) in ((1,0),(1,1),(0,1),(1, tiles_x-1),(1, tiles_x-2),(0, tiles_x-2),(tiles_y-2,tiles_x-1),(tiles_y-2,tiles_x-2),(tiles_y-1,tiles_x-2),(tiles_y-2,0),(tiles_y-2,1),(tiles_y-1,1)):
                if y == posy and x == posx:
                    terrain[y][x] = 110
            for (posy,posx) in ((0,0),(0, tiles_x-1),(tiles_y-1,tiles_x-1),(tiles_y-1,0)):
                if y == posy and x == posx:
                    terrain[y][x] = 130
    
    # ----- 4th run -----
    # Vermischen der Höhen
    for y in range(tiles_y):
        for x in range(tiles_x):
            summe = 0
            for (dx,dy) in ((-1,-1), (-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)):
                 try:
                     value = terrain[y+dy][x+dx]
                 except:
                     value = 0
                 summe += value
                 #summe += terrain[y+dy][x+dx]
            wert = summe / 9
            terrain[y][x] = round(wert)
                    
    with open("terrain.txt", "w") as terrain_file:
        print("Writing file...")
        for y in terrain:
            for x in y:
                terrain_file.write(str(x) + ",")
            terrain_file.write("\n")
            
    print("Finished!")
        

if __name__ == "__main__":
    generateTerrain(50,50)
