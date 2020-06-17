import pygame

def viewTerrain(terrain, screen, waterheight):
    
    for y, line in enumerate(terrain):
        for x, tile in enumerate(line):
            h = int(terrain[y][x])
            
            if h <= waterheight:
                c = (0,0,int(h/waterheight*255))
            else:
                c = (h, h, h)
            if h == 0:
                c = (0,255,0)
            #if h < 15:
            #    c = (50, 50, 200)
            #elif h < 25:
            #    c = (25, 125, 225)
            #elif h < 40:
            #    c = (25, 125, 225)
            #elif h < 50:
            #    c = (175, 175, 175)
            #elif h < 75:
            #    c = (150, 150, 150)
            #elif h < 100:
            #    c = (125, 125, 125)
            #elif h < 125:
            #    c = (100, 100, 100)
            
            pygame.draw.rect(screen, c, (x*10, y*10,10,10))

if __name__ == "__main__":
    
    #terrainGenerator.generateTerrain(50,50)
    
    with open("terrain.txt", "r") as terrain_file:
        lines = terrain_file.readlines()
    terrain = []
    for line in lines:
        terrain.append(line.split(",")[:-1])
    
    pygame.init()
    screen = pygame.display.set_mode((1280, 800), pygame.DOUBLEBUF)
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((255,255,255)) # fill background white
    
    viewTerrain(terrain,background, 40)
    
    clock = pygame.time.Clock()
    fps = 60
    playtime = 0.0
    
    running = True
    pygame.mouse.set_visible(True)
    oldleft, oldmiddle, oldright  = False, False, False
    screen.blit(background, (0, 0))
    while running:
        
        milliseconds = clock.tick(fps) #
        seconds = milliseconds / 1000
        playtime += seconds

        # -------- events ------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # ------- pressed and released key ------
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
        #screen.blit(background, (0, 0))
        pygame.display.flip()
