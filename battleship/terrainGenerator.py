import random

def getDifferences(xlist):
    lenList = len(xlist)
    difference_list = []
    for _ in range(lenList):
        difference_list.append([])
    for num in xlist:
        for x in range(lenList):
            difference_list[xlist.index(num)].append((abs(num[0]-xlist[x][0]),abs(num[1]-xlist[x][1])))
    return difference_list
    
def generateStartpoints(terrain, waterheight, numPlayers):
    startpoints = []
    tiles_y = len(terrain)
    tiles_x = len(terrain[0])
    land = []
    for y in range(tiles_y):
        for x in range(tiles_x):
            if terrain[y][x] > waterheight:
                for (dx,dy) in ((-1,0),(0,-1),(0,1),(1,0)):
                    try:
                        if terrain[y+dy][x+dx] <= waterheight: 
                            land.append((y,x))
                            break
                    except:
                        pass
    for _ in range(numPlayers):
        startpoints.append(random.choice(land))
    
    #candidates = []
    for tile in land:
    #if True:
    #for _ in range(100):
        diffs = getDifferences(startpoints)
        for diff in diffs:
            for x in diff:
                if diff.index(x) != 0:
                    if x[0] < len(terrain)//(numPlayers) and x[1] < len(terrain)//(numPlayers):
                        #print(x)
                        startpoints.remove(startpoints[diffs.index(diff)])
                        startpoints.append(random.choice(land))
    return startpoints

def generateTerrain(tiles_x=20, tiles_y=20, waterheight=0):
    terrain = []
    
    h = -255
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
            new = old + random.gauss(waterheight, 75)
            new = min(255, new)
            new = max(-255, new)
            terrain[y][x] = round(new)
    
    # ----- 3rd run -----
    # Random Landmasses in the ocean (Volcanos)
    volcanos = []
    if tiles_y < 20 or tiles_x < 20:
        raise SystemError("Map-Size must be at least 20x20!")
    for y in range(10,tiles_y-10):
        for x in range(10,tiles_x-10):
            if random.random() < 0.025:
                terrain[y][x] = random.randint(-150,200)
                volcanos.append((y,x))
    
    # ----- 3rd run -----
    # Landmasse in den Ecken
    #for y in range(tiles_y):
    #    for x in range(tiles_x):
    #        for (posy,posx) in ((1,0),(1,1),(0,1),(1, tiles_x-1),(1, tiles_x-2),(0, tiles_x-2),(tiles_y-2,tiles_x-1),(tiles_y-2,tiles_x-2),(tiles_y-1,tiles_x-2),(tiles_y-2,0),(tiles_y-2,1),(tiles_y-1,1)):
    #            if y == posy and x == posx:
    #                terrain[y][x] = 110
    #        for (posy,posx) in ((0,0),(0, tiles_x-1),(tiles_y-1,tiles_x-1),(tiles_y-1,0)):
    #            if y == posy and x == posx:
    #                terrain[y][x] = 130
    
    # ----- 4th run -----
    # Landmasse am Rand
    #for y in range(tiles_y):
    #    for x in range(tiles_x):
    #        if y == 0:
    #            terrain[y][x] = 255
    #        if x == 0:
    #            terrain[y][x] = 255
    #        if x == tiles_x-1:
    #            terrain[y][x] = 255
    #        if y == tiles_y-1:
    #            terrain[y][x] = 255
    #        volcanos.append((y,x))
    
    # ----- 5th run -----
    # Vermischen der Höhen
    for _ in range(10):
        for y in range(tiles_y):
            for x in range(tiles_x):
                if (y,x) in volcanos:
                    continue
                summe = 0
                neighbours = []
                for (dx,dy) in ((-1,-1), (-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)):
                     try:
                         value = terrain[y+dy][x+dx]
                     except:
                         print("land out of index")
                         continue
                     neighbours.append(value)
                # ------ 
                ma = max(neighbours)
                med = sum(neighbours) / len(neighbours)
                if med < ma: 
                    diff = ma-med
                    new_diff = diff * 0.8
                    new = ma - new_diff
                    new = min(255, new)
                    new = max(-255, new)
                    terrain[y][x] = round(new)
                else:
                    #print("dies sollte nie vorkommen....")
                    #med = min(255, med)
                    #med = max(-255, med)
                    #terrain[y][x] = round(med)   
                    pass
                
                     
    land_counter = 0
    water_counter = 0
    for y in range(tiles_y):
        for x in range(tiles_x):
            if terrain[y][x] > 0:
                land_counter += 1
            else:
                water_counter += 1
    print(land_counter)
    print(water_counter)
    
    startpoints = generateStartpoints(terrain, 0, 4)
    # ----- 6th run -----
    # Setzen der Startpoints
    #for y in range(tiles_y):
    #    for x in range(tiles_x):
    #        for startpoint in startpoints:
    #            if y == startpoint[0] and x == startpoint[1]:
    #                terrain[y][x] = 0
    
    with open("startpoints.txt", "w") as startpoint_file:
        for startpoint in startpoints:
            startpoint_file.write(str(startpoint[0]) + "," + str(startpoint[1]) +",")
            
    with open("terrain.txt", "w") as terrain_file:
        print("Writing file...")
        for y in terrain:
            for x in y:
                terrain_file.write(str(x) + ",")
            terrain_file.write("\n")
            
    print("Finished!")
        

if __name__ == "__main__":
    generateTerrain(100,100,0)
