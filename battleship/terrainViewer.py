import pygame

class Viewer:
    width=1280
    height=1024
    grid_size = ()

    def __init__(self, width, height, mapname="terrain.txt", player_number=3):
        Viewer.width = width
        Viewer.height = height
        self.player_number = player_number
        with open(mapname, "r") as terrain_file:
            lines = terrain_file.readlines()
        self.terrain = []
        for line in lines:
            self.terrain.append(line.split(",")[:-1])
        self.waterheight = 0
        self.harbours = []
        self.setup()
        self.run()

    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height),
                                              pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((255, 255, 255))  # fill background white
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.playtime = 0.0
        Viewer.grid_size = (10,10)

    def viewTerrain(self):
        """paint map into self.background"""
        for y, line in enumerate(self.terrain):
            for x, tile in enumerate(line):
                h = int(self.terrain[y][x])
                if h == self.waterheight:
                    c = (0,0,255)
                elif h < self.waterheight:
                    c = (0, 0, 255-int(abs(h)))            
                elif h < 50: # 0-50
                    c = (0+h, 200+h, 0+h)
                elif h < 100: # 50-100
                    c = (h, 150, h)
                elif h < 150: # 100-150
                    c = (50+h, 255, 0)
                elif h < 200: # 150-200
                    c = (50+h, 255, 0)
                elif h < 250: # 200-250
                    c = (h,h,h)
                     
                if h == 0:
                    c = (255, 0, 0)  # all harbours are hostile
                    self.harbours.append((x, y))
                pygame.draw.rect(self.background, c, (x * self.grid_size[0],
                                             y * self.grid_size[1],
                                             self.grid_size[0], self.grid_size[1]))
        # make friendly harbour green instead hostile-red
        pygame.draw.rect(self.background, (0, 255, 0),
                         (self.harbours[self.player_number][0] * self.grid_size[0],
                          self.harbours[self.player_number][1] * self.grid_size[1],
                          self.grid_size[0], self.grid_size[1]))

    def pixel_to_grid(self, pixelxy):
        x, y = pixelxy
        return (x // self.grid_size[0], y // self.grid_size[1])

    def run(self):
        running = True
        pygame.mouse.set_visible(True)
        oldleft, oldmiddle, oldright = False, False, False
        self.viewTerrain()
        self.screen.blit(self.background, (0, 0))

        while running:
            (x,y) = self.pixel_to_grid(pygame.mouse.get_pos())
            text = "you are player # {}. cursor at cell x:{} y:{}".format(
                self.player_number,x,y )
            pygame.display.set_caption(text)
            milliseconds = self.clock.tick(self.fps)  #
            seconds = milliseconds / 1000
            self.playtime += seconds

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
    Viewer(1280,1024)
    

    
