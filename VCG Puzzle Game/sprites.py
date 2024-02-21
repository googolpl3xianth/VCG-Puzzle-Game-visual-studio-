from PIL import Image
from PIL.ImageFilter import FIND_EDGES
import pygame as pg

pg.init()
screen = pg.display.set_mode((1,1))

def spriteSheet(image, imageWidth, imageHeight, numFrames, gameManager):
    frames = []
    i = 0 
    spriteImage = Image.open(image)
    temp = image
    for y in range(spriteImage.height // imageHeight):
      for x in range(spriteImage.width // imageWidth):
          temp = image
          i += 1
          if i > numFrames:
              y = (spriteImage.height // imageHeight) + 1
              x = (spriteImage.width // imageWidth) + 1
              break

          spriteImage = spriteImage.crop((x * imageWidth, y * imageHeight, x * imageWidth + imageWidth, y * imageHeight + imageHeight))
          temp = temp.replace(".png", str(i) + ".png")
          spriteImage.resize((int(gameManager.tileSize), int(gameManager.tileSize))).save(temp)
          frames.append(temp)
          spriteImage = Image.open(image)
    return frames

class GameManager:  ########## Game manager #########

  def __init__(self, WIDTH, HEIGHT, FPS, tileSize):
    self.Player = Player
    self.wall_group = pg.sprite.Group()
    self.box_group = pg.sprite.Group()
    self.colliding_box_group = pg.sprite.Group()
    self.shadow_group = pg.sprite.Group()
    self.door_group = pg.sprite.Group()
    self.guard_group = pg.sprite.Group()
    self.collect_group = pg.sprite.Group()
    self.text_group = pg.sprite.Group()
    self.switch_group = pg.sprite.Group()
    self.switchWall_group = pg.sprite.Group()
    self.kill_shadow = pg.sprite.Group()
    self.inventory = pg.sprite.Group()

    self.screenWidth = WIDTH
    self.screenHeight = HEIGHT
    self.tileSize = int(tileSize)
    self.FPS = FPS

    self.sceneIndex = 0

  def clearLevel(self):
    self.wall_group.empty()
    self.box_group.empty()
    self.colliding_box_group.empty()
    self.shadow_group.empty()
    self.door_group.empty()
    self.guard_group.empty()
    self.collect_group.empty()
    self.text_group.empty()
    self.switch_group.empty()
    self.switch_group.empty()
    self.switchWall_group.empty()
    self.kill_shadow.empty()

  def searchInv(self, name):
    for collectable in self.inventory:
      if collectable.name == name:
        return True
    return False

  def removeCollect(self, name):
    for collectable in self.inventory:
      if collectable.name == name:
        self.inventory.remove(collectable)

  def checkCollisions(self):
    collided_enemies = pg.sprite.spritecollide(self.Player, self.guard_group,
                                               False)
    collided_killShadow = pg.sprite.spritecollide(self.Player,
                                                  self.kill_shadow, False)
    if len(collided_enemies) > 0 or (len(collided_killShadow) > 0
                                     and self.Player.PShadow):
      self.Player.killed()

    collided_switchWalls = pg.sprite.spritecollide(self.Player,
                                                   self.switchWall_group,
                                                   False)

    for switchWall in collided_switchWalls:
      if switchWall.on:
        self.Player.rect.x = self.Player.preX
        self.Player.rect.y = self.Player.preY
        self.Player.windup = 1

    if self.Player.PShadow:  # player * shadow collision
      collided_shadows = pg.sprite.spritecollide(self.Player,
                                                 self.shadow_group, False)
      if len(collided_shadows) > 0:
        for shadow in collided_shadows:
          self.Player.collidingshadow = True
          self.Player.rect.x = self.Player.preX
          self.Player.rect.y = self.Player.preY
          self.Player.windup = 1
      else:
        self.Player.collidingshadow = False

    collided_walls = pg.sprite.spritecollide(self.Player, self.wall_group,
                                             False)
    collided_boxes = pg.sprite.spritecollide(self.Player, self.box_group,
                                             False)
    if len(collided_walls) > 0 or len(collided_boxes) > 0:
      self.Player.collidingreal = True
    elif len(collided_switchWalls) > 0:
      for wall in collided_switchWalls:
        if wall.on:
          self.Player.collidingreal = True
        else:
          self.Player.collidingreal = False
    else:
      self.Player.collidingreal = False

    for wall in collided_walls:
      if self.Player.PShadow == wall.shadow or not (self.Player.PShadow):
        self.Player.rect.x = self.Player.preX
        self.Player.rect.y = self.Player.preY
        self.Player.windup = 1

    for box in collided_boxes:
      if self.Player.PShadow == box.shadow or not (self.Player.PShadow):
        box.preX = box.rect.x  # moving a held box
        box.preY = box.rect.y
        box.rect.x += self.Player.rect.x - self.Player.preX
        box.rect.y += self.Player.rect.y - self.Player.preY

        self.colliding_box_group.add(box)
        self.box_group.remove(box)

    boxLoop = True
    while boxLoop:
      for box1 in self.colliding_box_group:
        box_box = pg.sprite.spritecollide(box1, self.box_group, False)
        for box2 in box_box:
          box2.preX = box2.rect.x  # moving a held box
          box2.preY = box2.rect.y
          box2.rect.x += self.Player.rect.x - self.Player.preX
          box2.rect.y += self.Player.rect.y - self.Player.preY

          self.colliding_box_group.add(box2)
          self.box_group.remove(box2)
        if len(box_box) <= 0:
          boxLoop = False
      if len(self.colliding_box_group) <= 0:
        break

    box_wall_col_group = pg.sprite.groupcollide(self.colliding_box_group,
                                                self.wall_group, False,
                                                False)  # box * wall collision
    if len(box_wall_col_group) > 0:
      for box in self.colliding_box_group:
        box.rect.x = box.preX
        box.rect.y = box.preY
      self.Player.rect.x = self.Player.preX
      self.Player.rect.y = self.Player.preY
      self.Player.windup = 1


    box_switchWall_col_group = pg.sprite.groupcollide(self.colliding_box_group,
                                                      self.switchWall_group,
                                                      False, False) # box * switchWall collision
    for box, switchWall in box_switchWall_col_group.items():
      if switchWall[0].on:
        box.rect.x = box.preX
        box.rect.y = box.preY
        self.Player.rect.x = self.Player.preX
        self.Player.rect.y = self.Player.preY
        self.Player.windup = 1

    for box in self.colliding_box_group:
      if box.rect.x < 0 or box.rect.x + box.rect.width > self.screenWidth or box.rect.y < 0 or box.rect.y + box.rect.height > self.screenHeight:
        box.rect.x = box.preX
        box.rect.y = box.preY
        self.Player.rect.x = self.Player.preX
        self.Player.rect.y = self.Player.preY

      self.box_group.add(box)
      self.colliding_box_group.remove(box)


    collided_doors = pg.sprite.spritecollide(self.Player, self.door_group,
                                             False) # player * door
    for door in self.door_group:
      door.isOpen = False
    for door in collided_doors:
      door.isOpen = True
      self.Player.rect.x = self.Player.preX
      self.Player.rect.y = self.Player.preY
      self.Player.windup = 1
      break


    for box in self.box_group:
        box_switch = pg.sprite.spritecollide(box, self.switch_group, False) # box * switch
        for switch in box_switch:
            if box not in switch.boxColliding:
                switch.switchValues()
                switch.boxColliding.append(box)
        for switch in self.switch_group:
            if len(box_switch) <= 0 and box in switch.boxColliding:
                switch.boxColliding.remove(box)


    collided_switch = pg.sprite.spritecollide(self.Player, self.switch_group,
                                              False) # player * switch
    for switch in collided_switch:
      if switch.playerColliding == False:
        switch.switchValues()
        switch.playerColliding = True

    for switch in self.switch_group:
      if switch not in collided_switch and switch.playerColliding == True:
        switch.playerColliding = False


    collided_collect = pg.sprite.spritecollide(self.Player, self.collect_group,
                                               False)
    for collect in collided_collect:
      collect.collected()

    collided_text = pg.sprite.spritecollide(self.Player, self.text_group,
                                            False)
    for text in self.text_group:
      text.colliding = False
    for text in collided_text:
      text.colliding = True


class Sprite(pg.sprite.Sprite):  ######### sprite #########

  def __init__(self,
               image,
               startx,
               starty,
               manager,
               text=False,
               grid=True,
               *groups):
    super().__init__(*groups)

    mentorImage = Image.open("sprites/NPCs/Mentor.png").crop((100, 80, 332, 590))
    mentorImage.resize((int(manager.tileSize), int(manager.tileSize) * 2)).save("sprites/NPCs/NMentor.png")

    if text:
      self.image = image
    else:
      self.image = pg.image.load(image).convert_alpha()
    self.rect = self.image.get_rect()

    if grid:
      self.rect.x = (startx + .5) * manager.tileSize - self.rect.width / 2
      self.rect.y = (starty + .5) * manager.tileSize - self.rect.height / 2
    else:
      self.rect.center = (startx, starty)

  def update(self):
    pass

  def draw(self, screen):
    screen.blit(self.image, self.rect)

  def animate(self):
    pass

  def addSelf(self, manager):
    pass


class Collider(Sprite):  ########## collider #############

  def __init__(self,
               image,
               startx,
               starty,
               manager,
               shadow=False,
               textImage=False,
               *groups):
    self.shadow = shadow
    super().__init__(image, startx, starty, manager, textImage, *groups)

  def addSelf(self, manager):
    if (self.shadow):
      manager.shadow_group.add(self)


class Collectable(Collider):  ####### Collectable #########

  def __init__(self, startx, starty, type, name, manager, *groups):
    if type == "key":
        keyImage = Image.open("sprites/Collectibles/key.png")
        keyImage.resize(
            (int(manager.tileSize),
             int(manager.tileSize))).save("sprites/Collectibles/newKey.png")
        image = "sprites/Collectibles/newKey.png"
        self.frames = ["sprites/Collectibles/newKey.png"]
    elif type == "coin":
        self.frames = spriteSheet("sprites/Collectibles/coin.png", 32, 32, 10, manager)
        image = self.frames[0]
    else:
      image = "sprites/Collectibles/newKey.png"

    self.clock = 0
    self.globalFPS = manager.FPS

    self.inInventor = False
    self.name = name
    super().__init__(image, startx, starty, manager, *groups)
    self.manager = manager

  def collected(self):
    self.manager.inventory.add(self)
    self.manager.collect_group.remove(self)
    self.inInventor = True

  def draw(self, screen):
    if (self.inInventor):
      pass
    else:
      screen.blit(self.image, self.rect)

  def addSelf(self, manager):
    manager.collect_group.add(self)


  def animate(self):
    FPS = 6

    numFrames = self.globalFPS / FPS
    if self.clock > self.globalFPS:
      self.clock = 0
    self.clock += 1

    self.image = pg.image.load(self.frames[int(
        (self.clock / numFrames)) % len(self.frames)]).convert_alpha()
    super().animate()


class Player(Collider):  ############ player ##############

  def __init__(self, startx, starty, manager, *groups):
    playerImage = Image.open("sprites/Player/Player.jpeg")
    playerImage.resize(
        (manager.tileSize * 4 // 5,
         manager.tileSize * 4 // 5)).save("sprites/Player/SPlayer.png")
    playerImage = Image.open("sprites/Player/SPlayer.png")
    playerImage.rotate(180, expand=True).save("sprites/Player/NPlayer.png")
    playerImage = Image.open("sprites/Player/SPlayer.png")
    playerImage.rotate(-90, expand=True).save("sprites/Player/WPlayer.png")
    playerImage = Image.open("sprites/Player/SPlayer.png")
    playerImage.rotate(90, expand=True).save("sprites/Player/EPlayer.png")

    shadowImage = Image.open("sprites/Player/SPlayer.png")
    shadowImage = shadowImage.filter(FIND_EDGES)
    shadowImage.putalpha(128)
    shadowImage.save("sprites/Player/SPShadow.png")
    shadowImage = Image.open("sprites/Player/SPShadow.png")
    shadowImage.rotate(180, expand=True).save("sprites/Player/NPShadow.png")
    shadowImage = Image.open("sprites/Player/SPShadow.png")
    shadowImage.rotate(90, expand=True).save("sprites/Player/EPShadow.png")
    shadowImage = Image.open("sprites/Player/SPShadow.png")
    shadowImage.rotate(-90, expand=True).save("sprites/Player/WPShadow.png")

    self.preX = startx
    self.preY = starty

    super().__init__("sprites/Player/SPlayer.png", startx, starty, manager,
                     *groups)
    self.collidingreal = False
    self.collidingshadow = False
    self.PShadow = False
    self.alive = True

    self.direction = "S"
    self.clock = 0
    self.globalFPS = manager.FPS

    # animation lists
    self.walkN = ["sprites/Player/NPlayer.png"]
    self.walkE = ["sprites/Player/EPlayer.png"]
    self.walkS = ["sprites/Player/SPlayer.png"]
    self.walkW = ["sprites/Player/WPlayer.png"]
    self.SWalkN = ["sprites/Player/NPShadow.png"]
    self.SWalkE = ["sprites/Player/EPShadow.png"]
    self.SWalkS = ["sprites/Player/SPShadow.png"]
    self.SWalkW = ["sprites/Player/WPShadow.png"]

    self.frames = self.walkS

    self.cooldown = 0
    self.windup = 0

    manager.Player = self
    self.manager = manager

  def update(self):
    self.preX = self.rect.x
    self.preY = self.rect.y
    keys = pg.key.get_pressed()

    if not (keys[pg.K_w]) and not (keys[pg.K_a]) and not (
        keys[pg.K_s]) and not (keys[pg.K_d]):
      self.cooldown = 0

    if self.cooldown <= 0:
      if keys[pg.K_a]:
        self.direction = "W"
        self.move(-self.manager.tileSize, 0)
        self.cooldown = self.manager.FPS
      elif keys[pg.K_d]:
        self.direction = "E"
        self.move(self.manager.tileSize, 0)
        self.cooldown = self.manager.FPS
      elif keys[pg.K_w]:
        self.direction = "N"
        self.move(0, -self.manager.tileSize)
        self.cooldown = self.manager.FPS
      elif keys[pg.K_s]:
        self.direction = "S"
        self.move(0, self.manager.tileSize)
        self.cooldown = self.manager.FPS

      if self.preX == self.rect.x and self.preY == self.rect.y:
        self.windup = 1
    else:
      self.cooldown -= self.windup
      self.windup += 2
      if self.windup > self.manager.FPS / 4:
        self.windup = self.manager.FPS / 4

    if keys[pg.K_LSHIFT] and not (self.collidingshadow):
      self.PShadow = True
    elif keys[pg.K_LSHIFT] is False and not (self.collidingreal):
      self.PShadow = False

    if self.PShadow:
      if self.direction == "N":
        self.frames = self.SWalkN
      elif self.direction == "E":
        self.frames = self.SWalkE
      elif self.direction == "S":
        self.frames = self.SWalkS
      elif self.direction == "W":
        self.frames = self.SWalkW
    else:
      if self.direction == "N":
        self.frames = self.walkN
      elif self.direction == "E":
        self.frames = self.walkE
      elif self.direction == "S":
        self.frames = self.walkS
      elif self.direction == "W":
        self.frames = self.walkW

  def move(self, x, y):
    self.rect.move_ip([x, y])

  def killed(self):
    self.alive = False

  def animate(self):
    FPS = 2

    numFrames = self.globalFPS / FPS
    if self.clock > self.globalFPS:
      self.clock = 0
    self.clock += 1

    self.image = pg.image.load(self.frames[int(
        (self.clock / numFrames)) % len(self.frames)]).convert_alpha()
    super().animate()


class text(Collider):  ################ text ###############

  def __init__(self, startx, starty, manager, text, rectColor=(0,255,255), textColor=(0,0,0), textSize=16, font='freesansbold.ttf', *groups):
    
    font = pg.font.Font(font, textSize)

    self.text = font.render(text, True, textColor)
    self.colliding = False

    self.rectColor = rectColor
    
    super().__init__(self.text, startx, starty, manager, False, True, *groups)

  def draw(self, screen):

    if self.colliding:
      screen.blit(self.text, self.rect)
    else:
      pg.draw.rect(screen, self.rectColor, self.rect, 3)

  def addSelf(self, manager):
    manager.text_group.add(self)


class Guard(Collider):  ############ guard ############

  def __init__(self,
               startx,
               starty,
               distance,
               speed,
               manager,
               hor=True,
               *groups):
    guardImage = Image.open("sprites/Enemies/Guard.png")
    guardImage.resize(
        (int(manager.tileSize),
         int(manager.tileSize))).save("sprites/Enemies/newGuardE.png")
    guardImage = Image.open("sprites/Enemies/newGuardE.png")
    guardImage.rotate(180, expand=True).save("sprites/Enemies/newGuardW.png")
    guardImage = Image.open("sprites/Enemies/newGuardE.png")
    guardImage.rotate(90, expand=True).save("sprites/Enemies/newGuardS.png")
    guardImage = Image.open("sprites/Enemies/newGuardE.png")
    guardImage.rotate(-90, expand=True).save("sprites/Enemies/newGuardN.png")

    if hor:
      guardImage = "sprites/Enemies/newGuardE.png"
      self.initial = startx * manager.tileSize
      self.final = (startx + distance) * manager.tileSize
    else:
      guardImage = "sprites/Enemies/newGuardS.png"
      self.initial = starty * manager.tileSize
      self.final = (starty + distance) * manager.tileSize

    self.hor = hor
    self.turn = False

    self.cooldown = 0
    self.windup = speed

    super().__init__(guardImage, startx, starty, manager, *groups)
    self.manager = manager

  def update(self):

    if self.cooldown <= 0:
      if self.hor:
        if not (self.turn):
          if self.rect.x < self.final:
            self.rect.x += self.manager.tileSize
          else:
            self.image = pg.image.load("sprites/Enemies/newGuardW.png").convert_alpha()
            self.turn = True
        else:
          if self.rect.x > self.initial:
            self.rect.x -= self.manager.tileSize
          else:
            self.image = pg.image.load("sprites/Enemies/newGuardE.png").convert_alpha()
            self.turn = False
      else:
        if not (self.turn):
          if self.rect.y < self.final:
            self.rect.y += self.manager.tileSize
          else:
            self.image = pg.image.load("sprites/Enemies/newGuardN.png").convert_alpha()
            self.turn = True
        else:
          if self.rect.y > self.initial:
            self.rect.y -= self.manager.tileSize
          else:
            self.image = pg.image.load("sprites/Enemies/newGuardS.png").convert_alpha()
            self.turn = False
      self.cooldown = 60
    else:
      self.cooldown -= self.windup

  def addSelf(self, manager):
    manager.guard_group.add(self)


class Box(Collider):  ############### box ################

  def __init__(self, startx, starty, manager, shadow, *groups):
    boxImage = Image.open("sprites/Boxes/box_moveable.png").crop(
        (90, 100, 400, 410))
    boxImage.resize(
        (manager.tileSize * 4 // 5,
         manager.tileSize * 4 // 5)).save("sprites/Boxes/NewBox.png")

    boxImage = Image.open("sprites/Boxes/box_unmoveable.png").crop(
        (90, 100, 400, 410))
    boxImage.resize(
        (manager.tileSize * 4 // 5,
         manager.tileSize * 4 // 5)).save("sprites/Boxes/NewSBox.png")

    if shadow:
      image = "sprites/Boxes/NewSBox.png"
    else:
      image = "sprites/Boxes/NewBox.png"

    self.shadow = shadow

    super().__init__(image, startx, starty, manager, shadow, *groups)

    self.preX = self.rect.x
    self.preY = self.rect.y

  def addSelf(self, manager):
    manager.box_group.add(self)
    if (self.shadow):
      manager.shadow_group.add(self)


class Switch(Collider):  ############ switch #############

  def __init__(self, startx, starty, manager, color, switchWalls, *groups):
    offImage = Image.open("sprites/Switches/redSwitchOff.png")
    offImage.thumbnail((manager.tileSize, manager.tileSize))
    offImage.save("sprites/Switches/NRedSwitchOff.png")

    offImage = Image.open("sprites/Switches/greenSwitchOff.png")
    offImage.thumbnail((manager.tileSize, manager.tileSize))
    offImage.save("sprites/Switches/NGreenSwitchOff.png")

    offImage = Image.open("sprites/Switches/blueSwitchOff.png")
    offImage.thumbnail((manager.tileSize, manager.tileSize))
    offImage.save("sprites/Switches/NBlueSwitchOff.png")

    onImage = Image.open("sprites/Switches/redSwitchOn.png")
    onImage.thumbnail((manager.tileSize, manager.tileSize))
    onImage.save("sprites/Switches/NRedSwitchOn.png")

    onImage = Image.open("sprites/Switches/greenSwitchOn.png")
    onImage.thumbnail((manager.tileSize, manager.tileSize))
    onImage.save("sprites/Switches/NGreenSwitchOn.png")

    onImage = Image.open("sprites/Switches/blueSwitchOn.png")
    onImage.thumbnail((manager.tileSize, manager.tileSize))
    onImage.save("sprites/Switches/NBlueSwitchOn.png")

    self.color = color

    if color == "red":
      image = "sprites/Switches/NRedSwitchOff.png"
    elif color == "green":
      image = "sprites/Switches/NGreenSwitchOff.png"
    else:
      image = "sprites/Switches/NBlueSwitchOff.png"

    super().__init__(image, startx, starty, manager, *groups)

    self.switchWall_group = switchWalls
    self.playerColliding = False
    self.boxColliding = []
    self.on = False

  def addSelf(self, manager):
    manager.switch_group.add(self)

  def update(self):
    if self.on == True:
      if self.color == "red":
        self.image = pg.image.load("sprites/Switches/NRedSwitchOn.png").convert_alpha()
      elif self.color == "green":
        self.image = pg.image.load("sprites/Switches/NGreenSwitchOn.png").convert_alpha()
      else:
        self.image = pg.image.load("sprites/Switches/NBlueSwitchOn.png").convert_alpha()
    else:
      if self.color == "red":
        self.image = pg.image.load("sprites/Switches/NRedSwitchOff.png").convert_alpha()
      elif self.color == "green":
        self.image = pg.image.load("sprites/Switches/NGreenSwitchOff.png").convert_alpha()
      else:
        self.image = pg.image.load("sprites/Switches/NBlueSwitchOff.png").convert_alpha()

  def switchValues(self):
    self.on = not (self.on)
    for switchWall in self.switchWall_group:
      switchWall.on = not switchWall.on


class switchWall(Collider):  ############ switchWall ######

  def __init__(self, startx, starty, manager, color, on=True, *groups):
    offImage = Image.open("sprites/Switches/redSwitchWallOff.png")
    offImage.thumbnail((manager.tileSize, manager.tileSize))
    offImage.save("sprites/Switches/NRedSwitchWallOff.png")

    offImage = Image.open("sprites/Switches/greenSwitchWallOff.png")
    offImage.thumbnail((manager.tileSize, manager.tileSize))
    offImage.save("sprites/Switches/NGreenSwitchWallOff.png")

    offImage = Image.open("sprites/Switches/blueSwitchWallOff.png")
    offImage.thumbnail((manager.tileSize, manager.tileSize))
    offImage.save("sprites/Switches/NBlueSwitchWallOff.png")

    onImage = Image.open("sprites/Switches/redSwitchWallOn.png")
    onImage.thumbnail((manager.tileSize, manager.tileSize))
    onImage.save("sprites/Switches/NRedSwitchWallOn.png")

    onImage = Image.open("sprites/Switches/greenSwitchWallOn.png")
    onImage.thumbnail((manager.tileSize, manager.tileSize))
    onImage.save("sprites/Switches/NGreenSwitchWallOn.png")

    onImage = Image.open("sprites/Switches/blueSwitchWallOn.png")
    onImage.thumbnail((manager.tileSize, manager.tileSize))
    onImage.save("sprites/Switches/NBlueSwitchWallOn.png")

    self.on = on
    self.color = color

    if on:
      if color == "red":
        image = "sprites/Switches/NRedSwitchWallOn.png"
      elif color == "green":
        image = "sprites/Switches/NGreenSwitchWallOn.png"
      else:
        image = "sprites/Switches/NBlueSwitchWallOn.png"
    else:
      if color == "red":
        image = "sprites/Switches/NRedSwitchWallOff.png"
      elif color == "green":
        image = "sprites/Switches/NGreenSwitchWallOff.png"
      else:
        image = "sprites/Switches/NBlueSwitchWallOff.png"

    self.switched = on

    super().__init__(image, startx, starty, manager, True)

  def update(self):
    if self.on == True:
      if self.color == "red":
        self.image = pg.image.load("sprites/Switches/NRedSwitchWallOn.png").convert_alpha()
      elif self.color == "green":
        self.image = pg.image.load("sprites/Switches/NGreenSwitchWallOn.png").convert_alpha()
      else:
        self.image = pg.image.load("sprites/Switches/NBlueSwitchWallOn.png").convert_alpha()
    else:
      if self.color == "red":
        self.image = pg.image.load("sprites/Switches/NRedSwitchWallOff.png").convert_alpha()
      elif self.color == "green":
        self.image = pg.image.load("sprites/Switches/NGreenSwitchWallOff.png").convert_alpha()
      else:
        self.image = pg.image.load("sprites/Switches/NBlueSwitchWallOff.png").convert_alpha()

  def addSelf(self, manager):
    manager.switchWall_group.add(self)


class Door(Collider):  ############# door ###########

  def __init__(self, startx, starty, direction, returnIndex, item, manager,
               *groups):
    doorImage = Image.open("sprites/Doors/door.png")
    doorImage.thumbnail((manager.tileSize, manager.tileSize * 2))
    doorImage.save("sprites/Doors/NewDoorW.png")
    doorImage = Image.open("sprites/Doors/NewDoorW.png")
    doorImage.rotate(180, expand=True).save("sprites/Doors/NewDoorE.png")

    if direction == "E":
      image = "sprites/Doors/NewDoorE.png"
    elif direction == "W":
      image = "sprites/Doors/NewDoorW.png"
    elif direction == "N":
      image = "sprites/Doors/NewDoorN.png"
    elif direction == "S":
      image = "sprites/Doors/NewDoorS.png"
    else:
      image = "sprites/Doors/NewDoorE.png"

    self.isOpen = False
    self.returnIndex = returnIndex
    self.item = item

    super().__init__(image, startx, starty, manager, *groups)

    if direction == "E":
      self.rect.x = startx * manager.tileSize
      self.rect.y = starty * manager.tileSize
    elif direction == "W":
      self.rect.x = (startx + 1) * manager.tileSize - self.rect.width
      self.rect.y = starty * manager.tileSize
    elif direction == "N":
      self.rect.x = startx * manager.tileSize
      self.rect.y = (starty + 1) * manager.tileSize - self.rect.height
    elif direction == "S":
      self.rect.x = startx * manager.tileSize
      self.rect.y = starty * manager.tileSize
    else:
      image = "sprites/Doors/NewDoorE.png"

  def addSelf(self, manager):
    manager.door_group.add(self)

  def open(self, manager):
    if self.isOpen and manager.searchInv(self.item):
      manager.removeCollect(self.item)
      return True


class Button(Sprite):  ############# button ##################

  def __init__(self, image, startx, starty, manager, grid=True, *groups):

    buttonImage = Image.open("sprites/Buttons/Button.png")
    newImage = buttonImage.crop((50, 200, 550, 400))
    newImage.thumbnail((manager.tileSize * 8, manager.tileSize * 8))
    newImage.save("sprites/Buttons/NewButton.png")

    super().__init__(image, startx, starty, manager, False, grid, *groups)

  def isClick(self, *groups):
    mouse_pos = pg.mouse.get_pos()
    mouse_click = pg.mouse.get_pressed()

    if self.rect.collidepoint(mouse_pos):
      if mouse_click[0]:
        return True


class killShadow(Collider):  ########### kill shadow ########

  def __init__(self, startx, starty, width, height, manager, *groups):
    super().__init__("sprites/BGs/NewBlackBG.png", startx, starty, manager,
                     *groups)

    self.startx = startx
    self.starty = starty
    self.manager = manager
    tempImage = Image.open("sprites/BGs/NewBlackBG.png")

    self.imageWidth = tempImage.width
    self.imageHeight = tempImage.height
    self.width = width
    self.height = height
    self.rect = pg.Rect(startx * manager.tileSize, starty * manager.tileSize,
                        self.width * manager.tileSize,
                        self.height * manager.tileSize)
    self.rect.center = [
        startx * manager.tileSize + self.width * self.imageWidth // 2,
        starty * manager.tileSize + self.height * self.imageHeight // 2
    ]

  def addSelf(self, manager):
    manager.kill_shadow.add(self)

  def draw(self, screen):
    for i in range(self.width):
      for j in range(self.height):
        tempRect = pg.Rect(
            self.startx * self.manager.tileSize + (i * self.imageWidth),
            self.starty * self.manager.tileSize + (j * self.imageHeight),
            self.imageWidth, self.imageHeight)
        screen.blit(self.image, tempRect)


class Wall(Collider):  ############# wall  ##################

  def __init__(self, startx, starty, manager, vertical, num, shadow, *groups):
    wallImage = Image.open("sprites/Walls/wall.png")
    wallImage = wallImage.crop((0, 0, 85, 400))
    wallImage.resize((manager.tileSize, manager.tileSize)).save(
        "sprites/Walls/newWallV.png")  # walls are 25 x 25

    wallImage = Image.open("sprites/Walls/newWallV.png")
    wallImage.rotate(270, expand=True).save("sprites/Walls/newWallH.png")

    wallImage = Image.open("sprites/Walls/solidWall.png")
    wallImage = wallImage.crop((0, 0, 120, 400))
    wallImage.resize((manager.tileSize, manager.tileSize)).save(
        "sprites/Walls/newSWallV.png")  # walls are 25 x 25

    wallImage = Image.open("sprites/Walls/newSWallV.png")
    wallImage.rotate(270, expand=True).save("sprites/Walls/newSWallH.png")

    self.shadow = shadow
    self.vertical = vertical  # boolean
    self.num = num  # number of walls
    if self.shadow:
      if (self.vertical):
        image = "sprites/Walls/newSWallV.png"
      else:
        image = "sprites/Walls/newSWallH.png"
    else:
      if (self.vertical):
        image = "sprites/Walls/newWallV.png"
      else:
        image = "sprites/Walls/newWallH.png"
    super().__init__(image, startx, starty, manager, shadow, *groups)
    self.startx = startx
    self.starty = starty

    if self.vertical:
      if self.shadow:
        tempImage = Image.open("sprites/Walls/newSWallV.png")
      else:
        tempImage = Image.open("sprites/Walls/newWallV.png")
      self.width = tempImage.width
      self.height = tempImage.height
      self.rect = pg.Rect(startx * manager.tileSize, starty * manager.tileSize,
                          self.width, self.height * num)
      self.rect.center = [
          startx * manager.tileSize + self.width // 2,
          starty * manager.tileSize + self.height * num // 2
      ]
    else:
      if self.shadow:
        tempImage = Image.open("sprites/Walls/newSWallH.png")
      else:
        tempImage = Image.open("sprites/Walls/newWallH.png")
      self.width = tempImage.width
      self.height = tempImage.height
      self.rect = pg.Rect(startx * manager.tileSize, starty * manager.tileSize,
                          self.width * num, self.height)
      self.rect.center = [
          startx * manager.tileSize + self.width * num // 2,
          starty * manager.tileSize + self.height // 2
      ]

  def addSelf(self, manager):
    manager.wall_group.add(self)
    if (self.shadow):
      manager.shadow_group.add(self)

  def draw(self, screen):
    for i in range(self.num):
      if (self.vertical):
        tempRect = pg.Rect((self.startx * self.width,
                            self.starty * self.height + i * self.height),
                           (self.width, self.height))
        screen.blit(self.image, tempRect)
      else:
        tempRect = pg.Rect(self.startx * self.width + i * self.width,
                           self.starty * self.height, self.width, self.height)
        screen.blit(self.image, tempRect)


class Background(Sprite):  ##########  BG  ###############

  def __init__(self, image, manager):
    BG = Image.open("sprites/BGs/edge.png")
    BG.thumbnail((manager.tileSize, manager.tileSize))
    BG.save("sprites/BGs/NewBG.png")

    BG = Image.open("sprites/BGs/blackBG.png")
    BG.thumbnail((manager.tileSize, manager.tileSize))
    BG.save("sprites/BGs/NewBlackBG.png")

    super().__init__(image, 0, 0, manager)


  def draw(self, screen):
    width, height = screen.get_size()
    for col in range(width // self.rect.width):
      for row in range(height // self.rect.height):
        tempRect = pg.Rect(col * self.rect.width, row * self.rect.height, col,
                           row)
        screen.blit(self.image, tempRect)

