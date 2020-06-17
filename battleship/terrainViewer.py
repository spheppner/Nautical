import pygame

def viewTerrain(terrain, screen, waterheight, player_number):
    harbours = []
    for y, line in enumerate(terrain):
        for x, tile in enumerate(line):
            h = int(terrain[y][x])
            
            if h <= waterheight:
                c = (0,0,int(h/waterheight*255))
            else:
                c = (h, h, h)
            if h == 0:
                c = (255,0,0) # all harbours are hostile
                harbours.append((y,x))
            pygame.draw.rect(screen, c, (x*10, y*10,10,10))
    # make friendly harbour green instead hostile-red
    pygame.draw.rect(screen, (0,255,0),
        (harbours[player_number][1]*10,harbours[player_number][0]*10,10,10))

def viewer(mapname="terrain.txt", player_number=3):
    with open(mapname, "r") as terrain_file:
        lines = terrain_file.readlines()
    terrain = []
    for line in lines:
        terrain.append(line.split(",")[:-1])

    pygame.init()
    screen = pygame.display.set_mode((1280, 800), pygame.DOUBLEBUF)
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((255, 255, 255))  # fill background white

    viewTerrain(terrain, background, 40, player_number)

    clock = pygame.time.Clock()
    fps = 60
    playtime = 0.0

    running = True
    pygame.mouse.set_visible(True)
    oldleft, oldmiddle, oldright = False, False, False
    screen.blit(background, (0, 0))
    while running:
        pygame.display.set_caption("you are player # {}".format(player_number))
        milliseconds = clock.tick(fps)  #
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

        # screen.blit(background, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    viewer()
    

    
