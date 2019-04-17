"""
author: Simon HEPPNER
website: simon.heppner.at  
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
download: https://github.com/spheppner/mountainShooter
"""
import pygame
import random
import os


def randomize_color(color, delta=50):
    d=random.randint(-delta, delta)
    color = color + d
    color = min(255,color)
    color = max(0, color)
    return color

def make_text(msg="pygame is cool", fontcolor=(255, 0, 255), fontsize=42, font=None):
    """returns pygame surface with text. You still need to blit the surface."""
    myfont = pygame.font.SysFont(font, fontsize)
    mytext = myfont.render(msg, True, fontcolor)
    mytext = mytext.convert_alpha()
    return mytext

def write(background, text="bla", pos=None, color=(0,0,0),
          fontsize=None, center=False, x=None, y=None):
        """write text on pygame surface. pos is a 2d Vector """
        if pos is None and (x is None or y is None):
            print("Error with write function: no pos argument given and also no x and y:", pos, x, y)
            return
        if pos is not None:
            # pos has higher priority than x or y
            x = pos.x
            y = -pos.y
        if fontsize is None:
            fontsize = 24
        font = pygame.font.SysFont('mono', fontsize, bold=True)
        fw, fh = font.size(text)
        surface = font.render(text, True, color)
        if center: # center text around x,y
            background.blit(surface, (x-fw//2, y-fh//2))
        else:      # topleft corner is x,y
            background.blit(surface, (x,y))

def elastic_collision(sprite1, sprite2):
        """elasitc collision between 2 VectorSprites (calculated as disc's).
           The function alters the dx and dy movement vectors of both sprites.
           The sprites need the property .mass, .radius, pos.x pos.y, move.x, move.y
           by Leonard Michlmayr"""
        if sprite1.static and sprite2.static:
            return 
        dirx = sprite1.pos.x - sprite2.pos.x
        diry = sprite1.pos.y - sprite2.pos.y
        sumofmasses = sprite1.mass + sprite2.mass
        sx = (sprite1.move.x * sprite1.mass + sprite2.move.x * sprite2.mass) / sumofmasses
        sy = (sprite1.move.y * sprite1.mass + sprite2.move.y * sprite2.mass) / sumofmasses
        bdxs = sprite2.move.x - sx
        bdys = sprite2.move.y - sy
        cbdxs = sprite1.move.x - sx
        cbdys = sprite1.move.y - sy
        distancesquare = dirx * dirx + diry * diry
        if distancesquare == 0:
            dirx = random.randint(0,11) - 5.5
            diry = random.randint(0,11) - 5.5
            distancesquare = dirx * dirx + diry * diry
        dp = (bdxs * dirx + bdys * diry) # scalar product
        dp /= distancesquare # divide by distance * distance.
        cdp = (cbdxs * dirx + cbdys * diry)
        cdp /= distancesquare
        if dp > 0:
            if not sprite2.static:
                sprite2.move.x -= 2 * dirx * dp
                sprite2.move.y -= 2 * diry * dp
            if not sprite1.static:
                sprite1.move.x -= 2 * dirx * cdp
                sprite1.move.y -= 2 * diry * cdp


class VectorSprite(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0
    numbers = {} # { number, Sprite }

    def __init__(self, **kwargs):
        self._default_parameters(**kwargs)
        self._overwrite_parameters()
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        self.number = VectorSprite.number # unique number for each sprite
        VectorSprite.number += 1
        VectorSprite.numbers[self.number] = self
        self.create_image()
        self.distance_traveled = 0 # in pixel
        self.rect.center = (-300,-300) # avoid blinking image in topleft corner
        if self.angle != 0:
            self.set_angle(self.angle)
        self.tail = [] 

    def _overwrite_parameters(self):
        """change parameters before create_image is called""" 
        pass

    def _default_parameters(self, **kwargs):    
        """get unlimited named arguments and turn them into attributes
           default values for missing keywords"""

        for key, arg in kwargs.items():
            setattr(self, key, arg)
        if "layer" not in kwargs:
            self._layer = 4
        else:
            self._layer = self.layer
        if "static" not in kwargs:
            self.static = False
        if "pos" not in kwargs:
            self.pos = pygame.math.Vector2(random.randint(0, Viewer.width),-50)
        if "move" not in kwargs:
            self.move = pygame.math.Vector2(0,0)
        if "fontsize" not in kwargs:
            self.fontsize = 22
        if "friction" not in kwargs:
            self.friction = 1.0 # no friction
        if "radius" not in kwargs:
            self.radius = 5
        if "width" not in kwargs:
            self.width = self.radius * 2
        if "height" not in kwargs:
            self.height = self.radius * 2
        
        if "hitpoints" not in kwargs:
            self.hitpoints = 100
        self.hitpointsfull = self.hitpoints # makes a copy
        if "mass" not in kwargs:
            self.mass = 10
        if "damage" not in kwargs:
            self.damage = 10
        if "bounce_on_edge" not in kwargs:
            self.bounce_on_edge = False
        if "kill_on_edge" not in kwargs:
            self.kill_on_edge = False
        if "angle" not in kwargs:
            self.angle = 0 # facing right?
        if "max_age" not in kwargs:
            self.max_age = None
        if "max_distance" not in kwargs:
            self.max_distance = None
        if "picture" not in kwargs:
            self.picture = None
        if "bossnumber" not in kwargs:
            self.bossnumber = None
        if "kill_with_boss" not in kwargs:
            self.kill_with_boss = False
        if "sticky_with_boss" not in kwargs:
            self.sticky_with_boss = False
        if "mass" not in kwargs:
            self.mass = 15
        if "upkey" not in kwargs:
            self.upkey = None
        if "downkey" not in kwargs:
            self.downkey = None
        if "rightkey" not in kwargs:
            self.rightkey = None
        if "leftkey" not in kwargs:
            self.leftkey = None
        if "speed" not in kwargs:
            self.speed = None
        if "age" not in kwargs:
            self.age = 0 # age in seconds
        if "warp_on_edge" not in kwargs:
            self.warp_on_edge = False
        if "gravity" not in kwargs:
            self.gravity = None
        if "survive_north" not in kwargs:
            self.survive_north = False
        if "survive_south" not in kwargs:
            self.survive_south = False
        if "survive_west" not in kwargs:
            self.survive_west = False
        if "survive_east" not in kwargs:
            self.survive_east = False
        if "speed" not in kwargs:
            self.speed = 0
        if "color" not in kwargs:
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

    def kill(self):
        if self.number in self.numbers:
           del VectorSprite.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)

    def create_image(self):
        if self.picture is not None:
            self.image = self.picture.copy()
        else:
            self.image = pygame.Surface((self.width,self.height))
            self.image.fill((self.color))
        self.image = self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect= self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height

    def rotate(self, by_degree):
        """rotates a sprite and changes it's angle by by_degree"""
        self.angle += by_degree
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def set_angle(self, degree):
        """rotates a sprite and changes it's angle to degree"""
        self.angle = degree
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        # ----- kill because... ------
        if self.hitpoints <= 0:
            self.kill()
        if self.max_age is not None and self.age > self.max_age:
            self.kill()
        if self.max_distance is not None and self.distance_traveled > self.max_distance:
            self.kill()
        # ---- movement with/without boss ----
        if self.bossnumber is not None:
            if self.kill_with_boss:
                if self.bossnumber not in VectorSprite.numbers:
                    self.kill()
            if self.sticky_with_boss and self.bossnumber in VectorSprite.numbers:
                boss = VectorSprite.numbers[self.bossnumber]
                self.pos = pygame.math.Vector2(boss.pos.x, boss.pos.y)
                self.set_angle(boss.angle)
        self.pos += self.move * seconds
        self.move *= self.friction 
        self.distance_traveled += self.move.length() * seconds
        self.age += seconds
        self.wallbounce()
        self.rect.center = ( round(self.pos.x, 0), -round(self.pos.y, 0) )

    def wallbounce(self):
        # ---- bounce / kill on screen edge ----
        # ------- left edge ----
        if self.pos.x < 0:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = 0
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = Viewer.width 
        # -------- upper edge -----
        if self.pos.y  > 0:
            if self.kill_on_edge and not self.survive_north:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = 0
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = -Viewer.height
        # -------- right edge -----                
        if self.pos.x  > Viewer.width:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = Viewer.width
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = 0
        # --------- lower edge ------------
        if self.pos.y   < -Viewer.height:
            if self.kill_on_edge:
                self.hitpoints = 0
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = -Viewer.height
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = 0




class Mouse(VectorSprite):
    
    #def __init__(self, radius = 50, color=(255,0,0), control="mouse" ):
    #    """create a (black) surface and paint a blue Mouse on it"""
    def _overwrite_parameters(self):
        self._layer=10
        #pygame.sprite.Sprite.__init__(self,self.groups)
        self.radius = 50
        self.color = (255,0,0)
        self.r = self.color[0]
        self.g = self.color[1]
        self.b = self.color[2]
        
        #self.control = control # "mouse" "keyboard1" "keyboard2"
        #self.pushed = False

    def create_image(self, out_of_range = False):
        #print("oor:", out_of_range)
        self.image = pygame.surface.Surface((self.radius*0.5, self.radius*0.5))
        delta1 = 12.5
        delta2 = 25
        w = self.radius*0.5 / 100.0
        h = self.radius*0.5 / 100.0
        # pointing down / up
        for y in (0,2,4):
            print("y,w,h", y, w, h)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (35*w,0+y),(50*w,15*h+y),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (50*w,15*h+y),(65*w,0+y),2)
    
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (35*w,100*h-y),(50*w,85*h-y),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (50*w,85*h-y),(65*w,100*h-y),2)
        # pointing right / left                 
        for x in (0,2,4):
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (0+x,35*h),(15*w+x,50*h),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (15*w+x,50*h),(0+x,65*h),2)
            
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (100*w-x,35*h),(85*w-x,50*h),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (85*w-x,50*h),(100*w-x,65*h),2)
        
        if out_of_range:
            pygame.draw.line(self.image, (200,0,0), (0,0), (int(self.radius*0.5), int(self.radius*0.5)), 1)
            pygame.draw.line(self.image, (200,0,0), (int(self.radius*0.5),0), (0, int(self.radius*0.5)), 1)
            
        
        self.image.set_colorkey((0,0,0))
        self.rect=self.image.get_rect()
        #self.rect.center = self.x, self.y

    def update(self, seconds):
        VectorSprite.update(self, seconds)
        #if self.control == "mouse":
        self.pos.x, self.pos.y = pygame.mouse.get_pos()[0], -pygame.mouse.get_pos()[1]
        

class Flytext(VectorSprite):
    
    def _overwrite_parameters(self):
        self._layer = 7  # order of sprite layers (before / behind other sprites)
        self.r, self.g, self.b = self.color
        
    def create_image(self):
        self.image = make_text(self.text, (self.r, self.g, self.b), self.fontsize)  # font 22
        self.rect = self.image.get_rect()
        

class Spark(VectorSprite):
    
    def _overwrite_parameters(self):
        self._layer = 9
        self.kill_on_edge = True
        
    def create_image(self):
        r,g,b = self.color
        r = randomize_color(r,50)
        g = randomize_color(g,50)
        b = randomize_color(b,50)
        self.image = pygame.Surface((10,10))
        pygame.draw.line(self.image, (r,g,b), 
                         (10,5), (5,5), 3)
        pygame.draw.line(self.image, (r,g,b),
                          (5,5), (2,5), 1)
        self.image.set_colorkey((0,0,0))
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()            

class Player(VectorSprite):
    
    def _overwrite_parameters(self):
        self._layer = 50
        self.range1 = 250
        self.energy = 0
        self.max_energy = 10
        
    def create_image(self):
        self.image = pygame.Surface((10,10))
        pygame.draw.rect(self.image, (0, 255, 0), (2, 2, 6, 6))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()

class Fadenkreuz(VectorSprite):
    def _overwrite_parameters(self):
        self._layer = 50
        
    def create_image(self):
        self.image = pygame.Surface((10,10))
        pygame.draw.line(self.image, (255, 0, 0), (5,0), (5, 10))
        pygame.draw.line(self.image, (255, 0, 0), (0,5), (10, 5))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()
        

class Explosion():
    """emits a lot of sparks, for Explosion or Player engine"""
    def __init__(self, posvector, minangle=0, maxangle=360, maxlifetime=3,
                 minspeed=5, maxspeed=150, red=255, red_delta=0, 
                 green=225, green_delta=25, blue=0, blue_delta=0,
                 minsparks=5, maxsparks=20):
        for s in range(random.randint(minsparks,maxsparks)):
            v = pygame.math.Vector2(1,0) # vector aiming right (0°)
            a = random.randint(minangle,maxangle)
            v.rotate_ip(a)
            speed = random.randint(minspeed, maxspeed)
            duration = random.random() * maxlifetime # in seconds
            red   = randomize_color(red, red_delta)
            green = randomize_color(green, green_delta)
            blue  = randomize_color(blue, blue_delta)
            Spark(pos=pygame.math.Vector2(posvector.x, posvector.y),
                  angle= a, move=v*speed, max_age = duration, 
                  color=(red,green,blue), kill_on_edge = True)


class World():
    
    tiles_x = 121
    tiles_y = 90   
    
    
    def __init__(self):
        self.terrain = []
        h = 128
        #h2 = random.randint(180, 255)
        print("setting all to 128....")
        for y in range(self.tiles_y):
            line = []
            for x in range(self.tiles_x):
                height = h
                line.append(height)
            self.terrain.append(line)
        # ----- 2nd run -----
        for y in range(self.tiles_y):
            for x in range(self.tiles_x):
                old = self.terrain[y][x]
                new = old + random.gauss(0, 100)
                new = min(255, new)
                new = max(0, new)
                self.terrain[y][x] = new
        # ------ 3rd run ------
        # mittlewert von allen
        for y in range(self.tiles_y):
            
            for x in range(self.tiles_x):
                summe = 0
                for (dx,dy) in ((-1,-1), (-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)):
                     try:
                         value = self.terrain[y+dy][x+dx]
                     except:
                         value = 0
                     summe += value
                     #summe += self.terrain[y+dy][x+dx]
                wert = summe / 9
                self.terrain[y][x] = wert
        
   
            

        
    
    

class Viewer(object):
    width = 0
    height = 0
    images = {}
    sounds = {}
    menu =  {"main":            ["resume", "settings", "credits", "quit" ],
            #main
            "settings":        ["back", "video", "difficulty", "reset all values"],
            #settings
            "difficulty":      ["back", "powerups", "bosshealth", "playerhealth"],
            "video":           ["back", "resolution", "fullscreen"],
            #difficulty
            "bosshealth":      ["back", "1000", "2500", "5000", "10000"],
            "playerhealth":    ["back", "100", "250", "500", "1000"],
            "powerups":        ["back", "laser", "bonusrockets", "heal", "shield", "speed"],
            #powerups
            "bonusrockets":    ["back", "bonusrocketincrease", "bonusrocket duration"],
            "laser":           ["back", "laserdamage", "laser duration"],
            "heal":            ["back", "heal effectiveness"],
            "shield":          ["back", "bossrocket deflection", "shield duration"],
            "speed":           ["back", "speed increase", "speed duration"],
            #powerup effects
            "bonusrocketincrease": ["back", "1", "2", "3", "5", "10"],
            "bonusrocket duration": ["back", "10", "30", "60"],
            "laserdamage":     ["back", "3", "5", "10"],
            "laser duration": ["back", "10", "30", "60"],            
            "heal effectiveness": ["back", "50", "100", "250", "full health"],
            "bossrocket deflection": ["back", "true", "false"],
            "shield duration": ["back", "10", "30", "60"],
            "speed increase":  ["back", "3", "5", "10", "15"],
            "speed duration":  ["back", "10", "30", "60"],
            #video
            "resolution":      ["back", "720p", "1080p", "1440p", "4k"],
            "fullscreen":      ["back", "true", "false"]
            }
    
    
    #Viewer.menu["resolution"] = pygame.display.list_modes()
    history = ["main"]
    cursor = 0
    name = "main"
    fullscreen = False

    def __init__(self, width=640, height=400, fps=60):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.mixer.pre_init(44100,-16, 2, 2048)   
        pygame.init()
        Viewer.width = width    # make global readable
        Viewer.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0

        # -- menu --
        li = ["back"]
        for i in pygame.display.list_modes():
            # li is something like "(800, 600)"
            pair = str(i)
            comma = pair.find(",")
            x = pair[1:comma]
            y = pair[comma+2:-1]
            li.append(str(x)+"x"+str(y))
        Viewer.menu["resolution"] = li
        self.set_resolution()
        
        
        # ------ background images ------
        #self.backgroundfilenames = [] # every .jpg file in folder 'data'
        #try:
        #    for root, dirs, files in os.walk("data"):
        #        for file in files:
        #            if file[-4:] == ".jpg" or file[-5:] == ".jpeg":
        #                self.backgroundfilenames.append(file)
        #    random.shuffle(self.backgroundfilenames) # remix sort order
        #except:
        #    print("no folder 'data' or no jpg files in it")

        self.age = 0
        # ------ joysticks ----
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()
        self.prepare_sprites()
        self.loadbackground()
        self.load_sounds()
        self.world = World()
        #print(self.world)
        
        
    def load_sounds(self):
        #Viewer.sounds["click"]=  pygame.mixer.Sound(
        #         os.path.join("data", "panzersound1.wav"))
        return
    
    
    def set_resolution(self):
        if Viewer.fullscreen:
             self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF|pygame.FULLSCREEN)
        else:
             self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.loadbackground()
    
    
    def loadbackground(self):
        
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((255,0,255)) # fill background white
            
        self.background = pygame.transform.scale(self.background,
                          (Viewer.width,Viewer.height))
        self.background.convert()
        
    
    def paint_world(self):
        for y, line in enumerate(self.world.terrain):
            for x, tile in enumerate(line):
                h = self.world.terrain[y][x]
                #print("h = ", h)
                if h < 25:
                    c = (160, 160, 255)
                elif h < 50:
                    c = (185, 185, 255)
                elif h < 75:
                    c = (210, 210, 255)
                elif h < 100:
                    c = (255, 255, 255)
                elif h < 125:
                    c = (200, 200, 200)
                elif h < 150:
                    c = (175, 175, 175)
                elif h < 175:
                    c = (150, 150, 150)
                elif h < 200:
                    c = (125, 125, 125)
                elif h < 255:
                    c = (100, 100, 100)
                
                pygame.draw.rect(self.screen, c, (x*10, y*10,10,10))
                #if x == random.randint(1, 10) and y == random.randint(1, 10):
                #    p = pygame.math.Vector2(x*10, -y*10)
                #    self.player.pos = p
        
    
    def load_sprites(self):
            print("loading sprites from 'data' folder....")
            #Viewer.images["player1"]= pygame.image.load(
            #     os.path.join("data", "player1.png")).convert_alpha()
            
            # --- scalieren ---
            #for name in Viewer.images:
            #    if name == "bossrocket":
            #        Viewer.images[name] = pygame.transform.scale(
            #                        Viewer.images[name], (60, 60))
            
     
    def prepare_sprites(self):
        """painting on the surface and create sprites"""
        self.load_sprites()
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.flytextgroup = pygame.sprite.Group()
        self.playergroup = pygame.sprite.Group()
        self.mousegroup = pygame.sprite.Group()
        
        VectorSprite.groups = self.allgroup
        Flytext.groups = self.allgroup, self.flytextgroup
        Player.groups = self.allgroup, self.playergroup
        Fadenkreuz.groups = self.allgroup
        Mouse.groups = self.allgroup, self.mousegroup
        
        #self.player1 =  Player(imagename="player1", warp_on_edge=True, pos=pygame.math.Vector2(Viewer.width/2-100,-Viewer.height/2))
        #self.player2 =  Player(imagename="player2", angle=180,warp_on_edge=True, pos=pygame.math.Vector2(Viewer.width/2+100,-Viewer.height/2))
        tx = random.randint(0, 121)
        ty = random.randint(0,90)
        x=tx*10 + 5
        y=-ty*10 + 5
        print(x,y)
        self.player = Player(pos=pygame.math.Vector2(x=x,y=y))
        self.mouse1 = Mouse(control="mouse", color=(255,0,0))
   
    def menu_run(self):
        running = True
        pygame.mouse.set_visible(True)
        while running:
            
            #pygame.mixer.music.pause()
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1 # running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return -1 # running = False
                    if event.key == pygame.K_UP:
                        Viewer.cursor -= 1
                        Viewer.cursor = max(0, Viewer.cursor) # not < 0
                        #Viewer.menusound.play()
                    if event.key == pygame.K_DOWN:
                        Viewer.cursor += 1
                        Viewer.cursor = min(len(Viewer.menu[Viewer.name])-1,Viewer.cursor) # not > menu entries
                        #Viewer.menusound.play()
                    if event.key == pygame.K_RETURN:
                        text = Viewer.menu[Viewer.name][Viewer.cursor]
                        if text == "quit":
                            return -1
                            Viewer.menucommandsound.play()
                        elif text in Viewer.menu:
                            # changing to another menu
                            Viewer.history.append(text) 
                            Viewer.name = text
                            Viewer.cursor = 0
                            #Viewer.menuselectsound.play()
                        elif text == "resume":
                            return
                            #Viewer.menucommandsound.play()
                            #pygame.mixer.music.unpause()
                        elif text == "back":
                            Viewer.history = Viewer.history[:-1] # remove last entry
                            Viewer.cursor = 0
                            Viewer.name = Viewer.history[-1] # get last entry
                            #Viewer.menucommandsound.play()
                            # direct action
                        elif text == "credits":
                            credit_text = """'mountainShooter' by Simon HEPPNER\n---\nGithub: github.com/spheppner/mountainShooter\nWebsite: simon.heppner.at\n---\nprogrammed with Python3 and Pygame"""
                            print(credit_text)
                        if Viewer.name == "resolution":
                            # text is something like 800x600
                            t = text.find("x")
                            if t != -1:
                                x = int(text[:t])
                                y = int(text[t+1:])
                                Viewer.width = x
                                Viewer.height = y
                                self.set_resolution()
                                #Viewer.menucommandsound.play()
                                    
                        if Viewer.name == "fullscreen":
                            if text == "true":
                                #Viewer.menucommandsound.play()
                                Viewer.fullscreen = True
                                self.set_resolution()
                            elif text == "false":
                                #Viewer.menucommandsound.play()
                                Viewer.fullscreen = False
                                self.set_resolution()
                        
            # ------delete everything on screen-------
            self.screen.blit(self.background, (0, 0))
            
            
         
            # -------------- UPDATE all sprites -------             
            self.flytextgroup.update(seconds)

            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)

            # --- paint menu ----
            # ---- name of active menu and history ---
            write(self.screen, text="you are here:", x=200, y=50, color=(0,255,255))
            
            t = "main"
            for nr, i in enumerate(Viewer.history[1:]):
                #if nr > 0:
                t+=(" > ")
                t+=(i)
                #
            
            #t+=Viewer.name
            write(self.screen, text=t, x=200,y=70,color=(0,255,255))
            # --- menu items ---
            menu = Viewer.menu[Viewer.name]
            for y, item in enumerate(menu):
                write(self.screen, text=item, x=200, y=100+y*20, color=(255,255,255))
            # --- cursor ---
            write(self.screen, text="-->", x=100, y=100+ Viewer.cursor * 20, color=(255,255,255))
                        
            
           
                
            # -------- next frame -------------
            pygame.display.flip()
        #----------------------------------------------------- 
    def run(self):
        """The mainloop"""
        
        running = True
        self.menu_run()
        pygame.mouse.set_visible(True)
        oldleft, oldmiddle, oldright  = False, False, False
        while running:
            #pygame.display.set_caption("player1 hp: {} player2 hp: {}".format(
            #                     self.player1.hitpoints, self.player2.hitpoints))
            
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            self.player.energy += seconds * 0.5

            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_d:
                        if self.player.pos.x + 10 < Viewer.width - 215:
                            self.player.pos += pygame.math.Vector2(10,0)
                    elif event.key == pygame.K_a:
                        if self.player.pos.x - 10 > 0:
                            self.player.pos += pygame.math.Vector2(-10,0)
                    elif event.key == pygame.K_s:
                        if self.player.pos.y - 10 > -Viewer.height:
                            self.player.pos += pygame.math.Vector2(0,-10)
                    elif event.key == pygame.K_w:
                        if self.player.pos.y + 10 < 0:
                            self.player.pos += pygame.math.Vector2(0,10)
                    #elif event.key == pygame.K_LSHIFT:
            
            # =========== delete everything on screen ==============
            self.screen.blit(self.background, (0, 0))
                       
            
            self.paint_world()
            
            
            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            #if pressed_keys[pygame.K_LSHIFT]:
            
            #if pressed_keys[pygame.K_x]:
            #    print("hi")
            #    p = pygame.math.Vector2(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]*-1)
            #    Fadenkreuz(pos=p)
            # ------- movement keys for player1 -------
            
            #if pressed_keys[pygame.K_l]:
            #            self.player2.turn_right()
            
            # ------ mouse handler ------
            left,middle,right = pygame.mouse.get_pressed()
            oldleft, oldmiddle, oldright = left, middle, right
            if pygame.mouse.get_pressed()[0]:
                Explosion(posvector=pygame.math.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]*-1), maxlifetime = 1.5)
                # TODO: Shoot Rocket to mouse.get_pos
                
            # ------ joystick handler -------
            #for number, j in enumerate(self.joysticks):
            #    if number == 0:
            #        player = self.player1
            #    elif number ==1:
            #        player = self.player2
            #    else:
            #        continue 
             #   x = j.get_axis(0)
             #   y = j.get_axis(1)
                #if y > 0.5:
                #    player.move_backward()
                #if y < -0.5:
                #    player.move_forward()
                #if x > 0.5:
                #    player.turn_right()
                #if x < -0.5:
                #    player.turn_left()
                
              #  buttons = j.get_numbuttons()
              #  for b in range(buttons):
               #        pushed = j.get_button( b )
                #       if b == 0 and pushed:
                #           player.fire()
                #       if b == 4 and pushed:
                #           player.strafe_left()
                #       if b == 5 and pushed:
                #           player.strafe_right()                
                
              
         
            # paint the player
            
            #self.player.pos = pygame.math.Vector2(self.player.tx * 10, self.player.ty*10)
                       
            # write text below sprites
            write(self.screen, "FPS: {:8.3}".format(
                self.clock.get_fps() ), x=Viewer.width-200, y=10, color=(255,20,128))
            
            #kasterl für energy
            ey = self.player.energy / ( self.player.max_energy / 100)
            pygame.draw.rect(self.screen, (0, 255, 0), (Viewer.width-70, Viewer.height-35, 25, -int(ey*2)))
            pygame.draw.rect(self.screen, (133, 11, 133), (Viewer.width-70, Viewer.height-35, 25, -200), 10)
            #zwischenlinien beim energy-balken
            pygame.draw.line(self.screen, (111, 11, 111), (Viewer.width-70, Viewer.height-(35+(200/10)*1)), (Viewer.width-45, Viewer.height-(35+(200/10)*1)), 2)
            pygame.draw.line(self.screen, (111, 11, 111), (Viewer.width-70, Viewer.height-(35+(200/10)*2)), (Viewer.width-45, Viewer.height-(35+(200/10)*2)), 2)
            pygame.draw.line(self.screen, (111, 11, 111), (Viewer.width-70, Viewer.height-(35+(200/10)*3)), (Viewer.width-45, Viewer.height-(35+(200/10)*3)), 2)
            pygame.draw.line(self.screen, (111, 11, 111), (Viewer.width-70, Viewer.height-(35+(200/10)*4)), (Viewer.width-45, Viewer.height-(35+(200/10)*4)), 2)
            pygame.draw.line(self.screen, (111, 11, 111), (Viewer.width-70, Viewer.height-(35+(200/10)*5)), (Viewer.width-45, Viewer.height-(35+(200/10)*5)), 2)
            pygame.draw.line(self.screen, (111, 11, 111), (Viewer.width-70, Viewer.height-(35+(200/10)*6)), (Viewer.width-45, Viewer.height-(35+(200/10)*6)), 2)
            pygame.draw.line(self.screen, (111, 11, 111), (Viewer.width-70, Viewer.height-(35+(200/10)*7)), (Viewer.width-45, Viewer.height-(35+(200/10)*7)), 2)
            pygame.draw.line(self.screen, (111, 11, 111), (Viewer.width-70, Viewer.height-(35+(200/10)*8)), (Viewer.width-45, Viewer.height-(35+(200/10)*8)), 2)
            pygame.draw.line(self.screen, (111, 11, 111), (Viewer.width-70, Viewer.height-(35+(200/10)*9)), (Viewer.width-45, Viewer.height-(35+(200/10)*9)), 2)
                       
            # ----- collision detection between player and PowerUp---
            #for p in self.playergroup:
            #    crashgroup=pygame.sprite.spritecollide(p,
            #               self.powerupgroup, False, 
            #               pygame.sprite.collide_mask)
            #    for o in crashgroup:
            #            Explosion(o.pos, red=128, green=0, blue=128)
            #            o.kill()
            
                   
            # ================ UPDATE all sprites =====================
            self.allgroup.update(seconds)
            # ---------- paint range circle around player -------
            pygame.draw.circle(self.screen, (0,255,0), (int(self.player.pos.x), -int(self.player.pos.y)), self.player.range1, 3)
            
            # check --------: mouse out of range1 from player
            dist =   self.mouse1.pos - self.player.pos
            oldcenter = self.mouse1.rect.center
            print(dist.length())
            if dist.length() > self.player.range1:
                self.mouse1.create_image(out_of_range=True)
            else:
                self.mouse1.create_image(out_of_range=False)
            self.mouse1.rect.center = oldcenter
            # ----------- paint diameter of this circle through mouse ------
            # make dist with length radius
            try:
               dist.normalize_ip() # has no lenght 1
            except:
               dist = pygame.math.Vector2(1,0)
               dist.rotate(random.randint(0,360))
            dist *= self.player.range1
            pygame.draw.line(self.screen, (0,0,255), (int(self.player.pos.x), -int(self.player.pos.y)), (int(self.player.pos.x - dist.x), -int(self.player.pos.y - dist.y)), 1)
            pygame.draw.line(self.screen, (0,0,255), (int(self.player.pos.x), -int(self.player.pos.y)), (int(self.player.pos.x + dist.x), -int(self.player.pos.y + dist.y)), 1)
            
            
            if self.player.energy > self.player.max_energy:
                self.player.energy = self.player.max_energy
            
            
            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)

            
           
                
            # -------- next frame -------------
            pygame.display.flip()
        #-----------------------------------------------------
        pygame.mouse.set_visible(True)    
        pygame.quit()

if __name__ == '__main__':
    Viewer(1430,800).run()
