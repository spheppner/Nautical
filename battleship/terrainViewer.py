import pygame
import random

class Viewer:
    width = 1280
    height = 1024
    grid_size = ()
    viewport = [0,0,50,50]

    def __init__(self, width, height, mapname="terrain.txt", player_number=3):
        Viewer.width = width
        Viewer.height = height
        self.player_number = player_number
        with open(mapname, "r") as terrain_file:
            lines = terrain_file.readlines()
        self.terrain = []
        for line in lines:
            self.terrain.append(line.split(",")[:-1])
        self.startpoints = []
        with open("startpoints.txt", "r") as startpoints_file:
            line = startpoints_file.read().split(",")[:-1]
        print(line)
        xlist = []
        ylist = []
        for i, element in enumerate(line):
            if i % 2 == 0:
                xlist.append(int(element))
            else:
                ylist.append(int(element))
        self.startpoints = list(zip(xlist, ylist))
        print(self.startpoints)

        self.waterheight = 0
        self.harbours = []
        self.colorMap = []
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
        Viewer.grid_size = [10, 10]
        Viewer.viewport = [0,0,len(self.terrain[0]), len(self.terrain)]
        self.radar_grid_size = [6, 6]
        self.panel_width = Viewer.width - (len(self.terrain[0]) * Viewer.grid_size[0])
        self.panel = pygame.Surface((self.panel_width, Viewer.height))
        self.makeTerrainMap()
        self.draw_panel()

    def draw_panel(self):
        dx = self.panel_width-(self.radar_grid_size[0]*len(self.terrain[0]))
        self.panel.fill((255,165,0))
        self.panel.blit(self.paintMap(self.radar_grid_size), (dx,0))
        c = random.randint(128,255)
        pygame.draw.rect(self.panel, (c,c,c), (Viewer.viewport[0]*self.radar_grid_size[0]+dx,
                                               Viewer.viewport[1]*self.radar_grid_size[1],
                                               (Viewer.viewport[2]-Viewer.viewport[0])*self.radar_grid_size[0],
                                               (Viewer.viewport[3]-Viewer.viewport[1])*self.radar_grid_size[1]), 3)

    def makeTerrainMap(self):
        """paint map into self.background"""
        self.harbours = []
        self.colorMap = self.terrain.copy()
        for y, line in enumerate(self.terrain):
            for x, tile in enumerate(line):
                h = int(self.terrain[y][x])
                if h == self.waterheight:
                    c = (0, 0, 255)
                elif h < self.waterheight:
                    c = (0, 0, 255 - int(abs(h)))
                else:
                    c = (h,255-min(255,h*2.5) if h<65 else h,h)
                for startpoint in self.startpoints:
                    if y == startpoint[0] and x == startpoint[1]:
                        c = (255, 0, 0)  # all harbours are hostile
                        self.harbours.append((x, y))
                self.colorMap[y][x] = c

    def paintMap(self, grid_size):
        """Return Pygame surface with map"""
        mapSurface = pygame.Surface((grid_size[0]*len(self.terrain[0]), grid_size[1]*len(self.terrain[0])))
        for y, line in enumerate(self.colorMap):
            for x, c in enumerate(line):
                pygame.draw.rect(mapSurface, c, (x * grid_size[0],
                                                      y * grid_size[1],
                                                      grid_size[0], grid_size[1]))
        # make friendly harbour green instead hostile-red
        pygame.draw.rect(mapSurface, (255, 0, 255),
                         (self.harbours[self.player_number][0] * grid_size[0],
                          self.harbours[self.player_number][1] * grid_size[1],
                          grid_size[0], grid_size[1]))
        return mapSurface

    def pixel_to_grid(self, pixelxy):
        x, y = pixelxy
        return (x // self.grid_size[0], y // self.grid_size[1])

    def redraw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.paintMap(self.grid_size), (0-Viewer.viewport[0]*self.grid_size[0],
                                                         0-Viewer.viewport[1]*self.grid_size[1]))
        self.draw_panel()
        self.screen.blit(self.panel, (Viewer.width - self.panel_width, 0))

    def run(self):
        running = True
        pygame.mouse.set_visible(True)
        oldleft, oldmiddle, oldright = False, False, False
        #self.viewTerrain()
        self.redraw()
        while running:
            (x, y) = self.pixel_to_grid(pygame.mouse.get_pos())
            text = "You are player #{}. Cursor in cell x:{} y:{} | FPS: {:.2f}".format(
                self.player_number, x, y, self.clock.get_fps())

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
                    elif event.key == pygame.K_1:
                        self.grid_size[0] += 1
                        self.grid_size[1] += 1
                        maptilesx = (Viewer.width - self.panel_width) // self.grid_size[0]
                        maptilesy = (Viewer.height - 0) // self.grid_size[1]
                        Viewer.viewport[2] = maptilesx
                        Viewer.viewport[3] = maptilesy
                        #self.redraw()
                    elif event.key == pygame.K_2:
                        self.grid_size[0] -= 1
                        self.grid_size[1] -= 1
                        maptilesx = (Viewer.width - self.panel_width) // self.grid_size[0]
                        maptilesy = (Viewer.height - 0) // self.grid_size[1]
                        Viewer.viewport[2] = maptilesx
                        Viewer.viewport[3] = maptilesy
                        #self.redraw()
                    elif event.key == pygame.K_3:
                        self.radar_grid_size[0] += 1
                        self.radar_grid_size[1] += 1
                        #self.redraw()
                    elif event.key == pygame.K_4:
                        self.radar_grid_size[0] -= 1
                        self.radar_grid_size[1] -= 1
                        #self.redraw()
                    elif event.key == pygame.K_KP8:
                        Viewer.viewport[1] -= 1
                        Viewer.viewport[3] -= 1
                    elif event.key == pygame.K_KP2:
                        Viewer.viewport[1] += 1
                        Viewer.viewport[3] += 1
                    elif event.key == pygame.K_KP4:
                        Viewer.viewport[0] -= 1
                        Viewer.viewport[2] -= 1
                    elif event.key == pygame.K_KP6:
                        Viewer.viewport[0] += 1
                        Viewer.viewport[2] += 1

            #screen.blit(background, (0, 0))
            self.redraw()
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Viewer(1680, 1000)



