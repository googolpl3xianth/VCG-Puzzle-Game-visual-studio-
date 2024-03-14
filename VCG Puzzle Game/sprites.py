from PIL import Image
from PIL.ImageFilter import FIND_EDGES
import pygame as pg

pg.init()
screen = pg.display.set_mode((1,1))

def spriteSheet(image, imageWidth, imageHeight, numFrames, gameManager):
    frames = []
    i = 0 
    spriteImage = pg.image.load(image).convert_alpha()
    tempRect = spriteImage.get_rect()
    for y in range(tempRect.height // imageHeight):
      for x in range(tempRect.width // imageWidth):
          i += 1
          if i > numFrames:
              y = (tempRect.height // imageHeight) + 1
              x = (tempRect.width // imageWidth) + 1
              break
          frame = spriteImage.subsurface((x * imageWidth, y * imageHeight, imageWidth, imageHeight))
          frame = pg.transform.scale(frame, (gameManager.tileSize[0], gameManager.tileSize[1]))
          frames.append(frame)
    return frames


class GameManager:  ########## Game manager #########

  def __init__(self, FPS):
    self.Player = Player
    self.inventoryImage = invetoryShow
    self.wall_group = pg.sprite.Group()
    self.box_group = pg.sprite.Group()
    self.colliding_box_group = pg.sprite.Group()
    self.shadow_group = pg.sprite.Group()
    self.door_group = pg.sprite.Group()
    self.guard_group = pg.sprite.Group()
    self.enemy_group = pg.sprite.Group()
    self.collect_group = pg.sprite.Group()
    self.text_group = pg.sprite.Group()
    self.switch_group = pg.sprite.Group()
    self.switchWall_group = pg.sprite.Group()
    self.kill_shadow = pg.sprite.Group()
    self.inventory = pg.sprite.Group()

    width, height = pg.display.get_desktop_sizes()[0]
    width = round(width / 22) * 22
    self.screen = pg.display.set_mode((round(width), round(width * 6/11)))
    #self.screen = pg.display.set_mode((width, width * 9/16))
    self.screenWidth = self.screen.get_width()
    self.screenHeight = self.screen.get_height()
    self.tileSize = (self.screenWidth / 22,  self.screenWidth / 22)
    #self.tileSize = (self.screenWidth / 22,  self.screenHeight / 12)
    self.FPS = FPS

    self.sceneIndex = [0, [0, 0]]

  def clearLevel(self):
    self.wall_group.empty()
    self.box_group.empty()
    self.colliding_box_group.empty()
    self.shadow_group.empty()
    self.door_group.empty()
    self.guard_group.empty()
    self.enemy_group.empty()
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

    collided_switchWalls = pg.sprite.spritecollide(self.Player,
                                                   self.switchWall_group,
                                                   False)

    for switchWall in collided_switchWalls:
      if switchWall.on:
        self.Player.pos_float[0] = round(self.Player.preX)
        self.Player.pos_float[1] = round(self.Player.preY)
        self.Player.rect.x = round(self.Player.pos_float[0])
        self.Player.rect.y = round(self.Player.pos_float[1])
        self.Player.windup = 0


    collided_walls = pg.sprite.spritecollide(self.Player, self.wall_group,
                                             False)
    collided_boxes = pg.sprite.spritecollide(self.Player, self.box_group,
                                             False)
    if len(collided_walls) > 0 or len(collided_boxes) > 0:
      self.Player.collidingreal = True
    elif len(collided_switchWalls) > 0: # player * wall
      for wall in collided_switchWalls:
        if wall.on:
          self.Player.collidingreal = True
        else:
          self.Player.collidingreal = False
    else:
      self.Player.collidingreal = False

    for wall in collided_walls:
      if self.Player.PShadow == wall.shadow or not (self.Player.PShadow):
        self.Player.pos_float[0] = round(self.Player.preX)
        self.Player.pos_float[1] = round(self.Player.preY)
        self.Player.rect.x = round(self.Player.pos_float[0])
        self.Player.rect.y = round(self.Player.pos_float[1])
        self.Player.windup = 0

    for box in collided_boxes:
      if self.Player.PShadow == box.shadow or not (self.Player.PShadow):
        box.pos_float[0] += self.Player.pos_float[0] - self.Player.preX
        box.pos_float[1] += self.Player.pos_float[1] - self.Player.preY
        box.rect.x = round(box.pos_float[0])
        box.rect.y = round(box.pos_float[1])

        self.colliding_box_group.add(box)
        self.box_group.remove(box)

    boxLoop = True
    while boxLoop:
      for box1 in self.colliding_box_group:
        box_box = pg.sprite.spritecollide(box1, self.box_group, False)
        for box2 in box_box:
          box2.pos_float[0] += self.Player.pos_float[0] - self.Player.preX
          box2.pos_float[1] += self.Player.pos_float[1] - self.Player.preY
          box2.rect.x = round(box2.pos_float[0])
          box2.rect.y = round(box2.pos_float[1])

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
        box.pos_float[0] = round(box.preX) # moving a box
        box.pos_float[1] = round(box.preY)
        box.rect.x = round(box.pos_float[0])
        box.rect.y = round(box.pos_float[1])
      self.Player.pos_float[0] = round(self.Player.preX)
      self.Player.pos_float[1] = round(self.Player.preY)
      self.Player.rect.x = round(self.Player.pos_float[0])
      self.Player.rect.y = round(self.Player.pos_float[1])
      self.Player.windup = 0

    box_door_col_group = pg.sprite.groupcollide(self.colliding_box_group,
      self.door_group, False,
      False)  # box * door collision
    if len(box_door_col_group) > 0:
      for box in self.colliding_box_group:
        box.pos_float[0] = round(box.preX) # moving a box
        box.pos_float[1] = round(box.preY)
        box.rect.x = round(box.pos_float[0])
        box.rect.y = round(box.pos_float[1])
        self.Player.pos_float[0] = round(self.Player.preX)
        self.Player.pos_float[1] = round(self.Player.preY)
        self.Player.rect.x = round(self.Player.pos_float[0])
        self.Player.rect.y = round(self.Player.pos_float[1])
        self.Player.windup = 0


    box_switchWall_col_group = pg.sprite.groupcollide(self.colliding_box_group,
                                                      self.switchWall_group,
                                                      False, False) # box * switchWall collision
    for box, switchWall in box_switchWall_col_group.items():
      if switchWall[0].on:
        box.pos_float[0] = round(box.preX)
        box.pos_float[1] = round(box.preY)
        box.rect.x = round(box.pos_float[0])
        box.rect.y = round(box.pos_float[1])
        self.Player.pos_float[0] = round(self.Player.preX)
        self.Player.pos_float[1] = round(self.Player.preY)
        self.Player.rect.x = round(self.Player.pos_float[0])
        self.Player.rect.y = round(self.Player.pos_float[1])
        self.Player.windup = 0

    for box in self.colliding_box_group:
      if box.rect.x < 0 or box.rect.x + box.rect.width > self.screenWidth or box.rect.y < 0 or box.rect.y + box.rect.height > self.screenHeight:
        box.pos_float[0] = round(box.preX)
        box.pos_float[1] = round(box.preY)
        box.rect.x = round(box.pos_float[0])
        box.rect.y = round(box.pos_float[1])
        self.Player.pos_float[0] = round(self.Player.preX)
        self.Player.pos_float[1] = round(self.Player.preY)
        self.Player.rect.x = round(self.Player.pos_float[0])
        self.Player.rect.y = round(self.Player.pos_float[1])

      self.box_group.add(box)
      self.colliding_box_group.remove(box)


    collided_doors = pg.sprite.spritecollide(self.Player, self.door_group,
                                             False) # player * door
    for door in self.door_group:
      door.isOpen = False
    for door in collided_doors:
      door.isOpen = True
      self.Player.pos_float[0] = round(self.Player.preX)
      self.Player.pos_float[1] = round(self.Player.preY)
      self.Player.rect.x = round(self.Player.pos_float[0])
      self.Player.rect.y = round(self.Player.pos_float[1])
      self.Player.windup = 0
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

    for guard in self.guard_group:
      guard_box = pg.sprite.spritecollide(guard, self.box_group, False) # guard * box
      if len(guard_box) > 0:
        if not(guard.pos_float[0] == guard.preX and guard.pos_float[1] == guard.preY):
          guard.pos_float[0] = guard.preX
          guard.pos_float[1] = guard.preY
          guard.rect.x = round(guard.pos_float[0])
          guard.rect.y = round(guard.pos_float[1])
          guard.cover = 0
          guard.turnSelf()
      else:
        guard_wall = pg.sprite.spritecollide(guard, self.wall_group, False)
        if len(guard_wall) > 0:
          guard.pos_float[0] = guard.preX
          guard.pos_float[1] = guard.preY
          guard.rect.x = round(guard.pos_float[0])
          guard.rect.y = round(guard.pos_float[1])
          guard.cover = 0
          guard.turnSelf()
        else:
          guard_door = pg.sprite.spritecollide(guard, self.door_group, False)
          if len(guard_door) > 0:
            guard.pos_float[0] = guard.preX
            guard.pos_float[1] = guard.preY
            guard.rect.x = round(guard.pos_float[0])
            guard.rect.y = round(guard.pos_float[1])
            guard.cover = 0
            guard.turnSelf()

    collided_enemies = pg.sprite.spritecollide(self.Player, self.enemy_group,
                                               False)
    collided_killShadow = pg.sprite.spritecollide(self.Player,
                                                  self.kill_shadow, False)
    if len(collided_enemies) > 0 or (len(collided_killShadow) > 0
                                     and self.Player.PShadow):
      self.Player.killed()

    for guard in self.guard_group:
      guard_box = pg.sprite.spritecollide(guard, self.box_group, False)
      if len(guard_box) > 0:
        guard.vision.kill()
        guard.kill()

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
               pos,
               manager,
               grid=True,
               *groups):
    super().__init__(*groups)

    if image is not None:
        self.image = image
        self.rect = image.get_rect()
    
    if pos is not None:
        if grid:
          self.rect.x = (pos[0] + .5) * manager.tileSize[0] - self.rect.width / 2
          self.rect.y = (pos[1] + .5) * manager.tileSize[1] - self.rect.height / 2
        else:
          self.rect.center = (pos[0], pos[1])

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
               pos,
               manager,
               shadow=False, 
               grid=True,
               *groups):
    self.shadow = shadow
    super().__init__(image, pos, manager, grid, *groups)

  def addSelf(self, manager):
    if (self.shadow):
      manager.shadow_group.add(self)
      


class invetoryShow(Sprite):
  
    def __init__(self, manager, *groups):
      self.manager = manager
      self.font = pg.font.Font('freesansbold.ttf', round(manager.tileSize[1]))
      super().__init__(None, None, manager, *groups)
      manager.inventoryImage = self
      
    def sort(self):
      temp = pg.sprite.Group()
      while len(self.manager.inventory) > 0:
        collectible1 = self.manager.inventory.sprites()[0]
        temp.add(collectible1)
        self.manager.inventory.remove(collectible1)
        i = 0
        for collectable2 in self.manager.inventory:
          if collectable2.type == collectible1.type:
            self.manager.inventory.remove(collectable2)
            i += 1
        collectible1.num += i
        
      for collectible in temp:
        self.manager.inventory.add(collectible)
        temp.remove(collectible)
      
       
    def draw(self, screen):
      i = 0
      
      for collectible in self.manager.inventory:
        collectibleImage = collectible.image.copy()
        alpha = 128
        collectibleImage.fill((255, 255, 255, alpha), None, pg.BLEND_RGBA_MULT)
        screen.blit(collectibleImage, ((2 * i + .5) * self.manager.tileSize[0], .5 * self.manager.tileSize[1], collectible.rect.width, collectible.rect.height))
        text = self.font.render(str(collectible.num), 0, (0,0,0))
        outline = self.font.render(str(collectible.num), 0, (255,255,255))
        screen.blit(outline, ((2 * i + 1.75) * self.manager.tileSize[0] + outline.get_height() * .02, .5 * self.manager.tileSize[1] + outline.get_height() * .02, collectible.rect.width, collectible.rect.height))
        screen.blit(outline, ((2 * i + 1.75) * self.manager.tileSize[0] + outline.get_height() * .02, .5 * self.manager.tileSize[1] - outline.get_height() * .02, collectible.rect.width, collectible.rect.height))
        screen.blit(outline, ((2 * i + 1.75) * self.manager.tileSize[0] - outline.get_height() * .02, .5 * self.manager.tileSize[1] + outline.get_height() * .02, collectible.rect.width, collectible.rect.height))
        screen.blit(outline, ((2 * i + 1.75) * self.manager.tileSize[0] - outline.get_height() * .02, .5 * self.manager.tileSize[1] - outline.get_height() * .02, collectible.rect.width, collectible.rect.height))
        screen.blit(text, ((2 * i + 1.75) * self.manager.tileSize[0], .5 * self.manager.tileSize[1], collectible.rect.width, collectible.rect.height))
        i += 1
        
        


class Collectable(Collider):  ####### Collectable #########

  def __init__(self, pos, type, name, manager, *groups):
    if type == "key":
        image = pg.transform.scale(pg.image.load("sprites/Collectibles/key.png").convert_alpha(), (manager.tileSize[0],manager.tileSize[1]))
        self.frames = [image]
    elif type == "coin":
        self.frames = spriteSheet("sprites/Collectibles/coin.png", 32, 32, 10, manager)
        image = self.frames[0]
    else:
        image = pg.transform.scale(pg.image.load("sprites/Collectibles/key.png").convert_alpha(), (manager.tileSize[0],
            manager.tileSize[1]))
        self.frames = [image]

    self.clock = 0
    self.globalFPS = manager.FPS

    self.inInventory = False
    self.name = name
    self.type = type
    super().__init__(image, pos, manager, *groups)
    self.manager = manager
    self.num = 1

  def collected(self):
    self.image = self.frames[0]
    self.manager.inventory.add(self)
    self.manager.collect_group.remove(self)
    self.inInventory = True
    self.manager.inventoryImage.sort()

  def draw(self, screen):
    if not(self.inInventory):
      screen.blit(self.image, self.rect)

  def addSelf(self, manager):
    manager.collect_group.add(self)


  def animate(self):
    if not(self.inInventory):
        FPS = 6

        numFrames = self.globalFPS / FPS
        if self.clock > self.globalFPS:
          self.clock = 0
        self.clock += 1

        self.image = self.frames[round((self.clock / numFrames)) % len(self.frames)]


class Player(Collider):  ############ player ##############

  def __init__(self, pos, manager, *groups):
    playerImage = pg.transform.scale(pg.image.load("sprites/Player/Player.jpeg").convert_alpha(), (manager.tileSize[0] * 4 // 5, manager.tileSize[1] * 4 // 5))

    shadowImage = Image.open("sprites/Player/Player.jpeg")
    shadowImage = shadowImage.filter(FIND_EDGES)
    shadowImage.putalpha(128)
    shadowImage.save("sprites/Player/SPShadow.png")
    shadowPlayerImage = pg.transform.scale(pg.image.load("sprites/Player/SPShadow.png").convert_alpha(), (manager.tileSize[0] * 4 // 5, manager.tileSize[1] * 4 // 5))

    self.preX = pos[0]
    self.preY = pos[1]
    self.pos_float = [pos[0], pos[1]]

    super().__init__(playerImage, pos, manager,
                     *groups)
    self.collidingreal = False
    self.PShadow = False
    self.alive = True

    self.direction = "E"
    self.clock = 0
    self.globalFPS = manager.FPS

    # animation lists
    self.walkN = [pg.transform.rotate(playerImage, 180)]
    self.walkE = [pg.transform.rotate(playerImage, 90)]
    self.walkS = [playerImage]
    self.walkW = [pg.transform.rotate(playerImage, -90)]
    self.SWalkN = [pg.transform.rotate(shadowPlayerImage, 180)]
    self.SWalkE = [pg.transform.rotate(shadowPlayerImage, 90)]
    self.SWalkS = [shadowPlayerImage]
    self.SWalkW = [pg.transform.rotate(shadowPlayerImage, -90)]

    self.frames = self.walkS

    self.cooldown = 0
    self.windup = 0

    manager.Player = self
    self.manager = manager

  def update(self):
    self.preX = self.pos_float[0]
    self.preY = self.pos_float[1]
    keys = pg.key.get_pressed()

    if not (keys[pg.K_w]) and not (keys[pg.K_a]) and not (
        keys[pg.K_s]) and not (keys[pg.K_d]):
      self.cooldown = 0

    if self.cooldown <= 0:
      if keys[pg.K_a]:
        self.direction = "W"
        self.move(-1, 0)
        self.cooldown = self.manager.FPS
      elif keys[pg.K_d]:
        self.direction = "E"
        self.move(1, 0)
        self.cooldown = self.manager.FPS
      elif keys[pg.K_w]:
        self.direction = "N"
        self.move(0, -1)
        self.cooldown = self.manager.FPS
      elif keys[pg.K_s]:
        self.direction = "S"
        self.move(0, 1)
        self.cooldown = self.manager.FPS

      if self.preX == self.rect.x and self.preY == self.rect.y:
        self.windup = 0
    else:
      self.cooldown -= self.windup
      self.windup += 1
      if self.windup > self.manager.FPS / 7:
        self.windup = self.manager.FPS / 7

    if keys[pg.K_LSHIFT]:
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

    self.rect.x = round(self.pos_float[0])
    self.rect.y = round(self.pos_float[1])

  def move(self, x, y):
    self.pos_float[0] += x * self.manager.tileSize[0]
    self.pos_float[1] += y * self.manager.tileSize[1]


  def killed(self):
    self.alive = False

  def animate(self):
    FPS = 2

    numFrames = self.globalFPS / FPS
    if self.clock > self.globalFPS:
      self.clock = 0
    self.clock += 1

    self.image = self.frames[round((self.clock / numFrames)) % len(self.frames)]
    super().animate()

  def setPos(self, x, y):
    if x is not None:
        self.rect.x = (x + .5) * self.manager.tileSize[0] - self.rect.width / 2
        self.pos_float[0] = (x + .5) * self.manager.tileSize[0] - self.rect.width / 2
    if y is not None:
        self.rect.y = (y + .5) * self.manager.tileSize[1] - self.rect.height / 2
        self.pos_float[1] = (y + .5) * self.manager.tileSize[1] - self.rect.height / 2


class text(Collider):  ################ text ###############

  def __init__(self, pos, width, text, manager, textSize=16, textColor=(0,0,0), font='freesansbold.ttf', *groups):

    self.manager = manager
    image = pg.transform.scale(pg.image.load("sprites/Misc/textBubble.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))
    self.font = pg.font.Font(font, round(textSize * manager.tileSize[1]))

    self.words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    self.textColor = textColor

    self.colliding = False

    self.startx = ((pos[0] + .5) * manager.tileSize[0])
    self.starty = ((pos[1] + .5) * manager.tileSize[1])

    self.textBoxWdith = width * manager.tileSize[0]

    super().__init__(image, pos, manager, True, *groups)

  def draw(self, screen):

    if self.colliding:
      x, y = (self.startx, self.starty)
      maxX = x
      posArray = []
      space = self.font.size(' ')[0]  # The width of a space
      for line in self.words:
          for word in line:
              word_surface = self.font.render(word, 0, self.textColor)
              word_width, word_height = self.font.size(word)
              if x + word_width >= self.textBoxWdith:
                  x = self.startx  # Reset the x.
                  y += word_height  # Start on new row.
              posArray.append((x, y))
              x += word_width + space
              if x > maxX:
                maxX = x
          x = self.startx  # Reset the x.
          y += word_height
      maxX = maxX - self.startx
      height = y - self.starty


      s = pg.Surface((maxX, height), pg.SRCALPHA)
      pg.draw.rect(s, (255, 255, 255, 128), (s.get_rect()))
      screen.blit(s, (self.startx - (maxX / 2), self.starty - (height / 2), maxX, height))

      i = 0
      for line in self.words:
        for word in line:
          word_surface = self.font.render(word, 0, self.textColor)
          screen.blit(word_surface, (posArray[i][0] - (maxX / 2), posArray[i][1] - (height / 2)))
          i += 1


    else:
      screen.blit(self.image, self.rect)

  def addSelf(self, manager):
    manager.text_group.add(self)


class Spike(Collider): ############### spike ###############

  def __init__(self, pos, manager, grid=True, *groups):
    image = pg.transform.scale(pg.image.load("sprites/Enemies/spike.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))

    super().__init__(image, pos, manager, grid, *groups)

  def addSelf(self, manager):
    manager.enemy_group.add(self)


class visionCone(Collider): ############### guardVision ########

  def __init__(self, guard):
    image = pg.transform.scale(pg.image.load("sprites/Enemies/visionCone.png").convert_alpha(), (guard.manager.tileSize[0] * 2, guard.manager.tileSize[1] * 3))
    image = image.copy()
    alpha = 128
    image.fill((255, 255, 255, alpha), None, pg.BLEND_RGBA_MULT)

    self.preX = guard.pos_float[0]
    self.preY = guard.pos_float[1]

    super().__init__(image, (round(guard.pos_float[0]), round(guard.pos_float[1])), guard.manager , False, False)


class Guard(Collider):  ############ guard ############

  def __init__(self,
               pos,
               distance,
               speed,
               manager,
               hor=True,
               *groups):
    image = pg.transform.scale(pg.image.load("sprites/Enemies/Guard.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))

    self.distance = distance
    self.cover = 0

    self.hor = hor
    self.turn = False

    self.preX = pos[0] * manager.tileSize[0]
    self.preY = pos[1] * manager.tileSize[1]
    self.pos_float = [pos[0] * manager.tileSize[0], pos[1] * manager.tileSize[1]]

    self.cooldown = 0
    self.windup = speed

    super().__init__(image, pos, manager, *groups)

    self.manager = manager

    self.vision = visionCone(self)

    if not(hor):
      self.vision.image = pg.transform.rotate(self.vision.image, -90)
      self.image = pg.transform.rotate(self.image, 90)
    else:
      self.vision.image = pg.transform.rotate(self.vision.image, 180)


  def update(self):
    self.preX = self.pos_float[0]
    self.preY = self.pos_float[1]
    self.vision.preX = self.vision.rect.x
    self.vision.preY = self.vision.rect.y
    if self.cooldown <= 0:
      if self.hor:
        if self.cover < self.distance:
          self.cover += 1
          if not(self.turn):
            self.pos_float[0] += self.manager.tileSize[0]
            self.rect.x = self.pos_float[0]
            self.vision.rect.midleft = self.rect.center
          else:
            self.pos_float[0] -= self.manager.tileSize[0]
            self.rect.x = self.pos_float[0]
            self.vision.rect.midright = self.rect.center
        else:
          self.cover = 0
          self.turnSelf()
      else:
        if self.cover < self.distance:
          self.cover += 1
          if not(self.turn):
            self.pos_float[1] += self.manager.tileSize[1]
            self.rect.y = self.pos_float[1]
            self.vision.rect.midtop = self.rect.center
          else:
            self.pos_float[1] -= self.manager.tileSize[1]
            self.rect.y = self.pos_float[1]
            self.vision.rect.midbottom = self.rect.center
        else:
          self.cover = 0
          self.turnSelf()
      self.cooldown = self.manager.FPS
    else:
      self.cooldown -= self.windup

  def turnSelf(self):
    self.vision.image = pg.transform.rotate(self.vision.image, 180)
    self.image = pg.transform.rotate(self.image, 180)
    if self.hor:
      if not(self.turn):
        self.vision.rect = self.vision.image.get_rect(midright=self.rect.center)
        self.turn = True
      else:
        self.vision.rect = self.vision.image.get_rect(midleft=self.rect.center)
        self.turn = False
    else:
      if not(self.turn):
        self.vision.rect = self.vision.image.get_rect(midbottom=self.rect.center)
        self.turn = True
      else:
        self.vision.rect = self.vision.image.get_rect(midtop=self.rect.center)
        self.turn = False

  def addSelf(self, manager):
    manager.guard_group.add(self)
    manager.enemy_group.add(self)
    manager.enemy_group.add(self.vision)

  def draw(self, screen):
    screen.blit(self.image, self.rect)
    screen.blit(self.vision.image, self.vision.rect)


class Box(Collider):  ############### box ################

  def __init__(self, pos, shadow, manager, *groups):
    if not shadow:
        boxImage = Image.open("sprites/Boxes/box_moveable.png").crop((90, 100, 400, 410)).save("sprites/Boxes/NewBox.png")
        image = pg.transform.scale(pg.image.load("sprites/Boxes/NewBox.png").convert_alpha(), (manager.tileSize[0] * 4 // 5, manager.tileSize[1] * 4 // 5))
    else:
        boxImage = Image.open("sprites/Boxes/box_unmoveable.png").crop((90, 100, 400, 410)).save("sprites/Boxes/NewSBox.png")
        image = pg.transform.scale(pg.image.load("sprites/Boxes/NewSBox.png").convert_alpha(), (manager.tileSize[0] * 4 // 5, manager.tileSize[1] * 4 // 5))

    self.shadow = shadow

    super().__init__(image, pos, manager, shadow, *groups)

    self.preX = self.rect.x
    self.preY = self.rect.y
    self.pos_float = [self.rect.x, self.rect.y]

  def update(self):
    self.preX = self.pos_float[0]
    self.preY = self.pos_float[1]

  def addSelf(self, manager):
    manager.box_group.add(self)
    if (self.shadow):
      manager.shadow_group.add(self)


class Switch(Collider):  ############ switch #############

  def __init__(self, pos, color, switchWalls, manager, *groups):
    redSwitchOff = pg.transform.scale(pg.image.load("sprites/Switches/redSwitchOff.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))
    redSwitchOn = pg.transform.scale(pg.image.load("sprites/Switches/redSwitchOn.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))

    blueSwitchOff = pg.transform.scale(pg.image.load("sprites/Switches/blueSwitchOff.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))
    blueSwitchOn = pg.transform.scale(pg.image.load("sprites/Switches/blueSwitchOn.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))

    greenSwitchOff = pg.transform.scale(pg.image.load("sprites/Switches/greenSwitchOff.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))
    greenSwitchOn = pg.transform.scale(pg.image.load("sprites/Switches/greenSwitchOn.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))

    self.frames = ((redSwitchOff, redSwitchOn), (blueSwitchOff, blueSwitchOn), (greenSwitchOff, greenSwitchOn))

    self.color = color

    if color == "red":
      image = self.frames[0][0]
    elif color == "blue":
      image = self.frames[1][0]
    else:
      image = self.frames[2][0]

    super().__init__(image, pos, manager, *groups)

    self.switchWall_group = switchWalls
    self.playerColliding = False
    self.boxColliding = []
    self.on = False

  def addSelf(self, manager):
    manager.switch_group.add(self)

  def update(self):
    if self.color == "red":
      i = 0
    elif self.color == "blue":
      i = 1
    else:
      i = 2

    if self.on == True:
        j = 1
    else:
        j = 0

    self.image = self.frames[i][j]


  def switchValues(self):
    self.on = not (self.on)
    for switchWall in self.switchWall_group:
      switchWall.on = not switchWall.on


class switchWall(Collider):  ############ switchWall ######

  def __init__(self, pos, color, on, manager, *groups):
    redSwitchWallOff = pg.transform.scale(pg.image.load("sprites/Switches/redSwitchWallOff.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))
    redSwitchWallOn = pg.transform.scale(pg.image.load("sprites/Switches/redSwitchWallOn.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))

    blueSwitchWallOff = pg.transform.scale(pg.image.load("sprites/Switches/blueSwitchWallOff.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))
    blueSwitchWallOn = pg.transform.scale(pg.image.load("sprites/Switches/blueSwitchWallOn.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))

    greenSwitchWallOff = pg.transform.scale(pg.image.load("sprites/Switches/greenSwitchWallOff.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))
    greenSwitchWallOn = pg.transform.scale(pg.image.load("sprites/Switches/greenSwitchWallOn.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))

    self.frames = ((redSwitchWallOff, redSwitchWallOn), (blueSwitchWallOff, blueSwitchWallOn), (greenSwitchWallOff, greenSwitchWallOn))

    self.color = color

    if color == "red":
      image = self.frames[0][0]
    elif color == "blue":
      image = self.frames[1][0]
    else:
      image = self.frames[2][0]


    self.on = on
    self.color = color

    self.switched = on

    super().__init__(image, pos, manager, True)

  def update(self):
    if self.color == "red":
      i = 0
    elif self.color == "blue":
      i = 1
    else:
      i = 2

    if self.on == True:
        j = 1
    else:
        j = 0

    self.image = self.frames[i][j]

  def addSelf(self, manager):
    manager.switchWall_group.add(self)


class Door(Collider):  ############# door ###########

  def __init__(self, pos, direction, returnIndex, item, manager,
               *groups):
    doorImage = pg.transform.scale(pg.image.load("sprites/Doors/door.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1] * 2))

    self.isOpen = False
    self.returnIndex = returnIndex
    self.item = item

    super().__init__(doorImage, pos, manager, *groups)

    if direction == "E":
      self.image = pg.transform.rotate(self.image, 180)
      self.rect.x = pos[0] * manager.tileSize[0]
      self.rect.y = pos[1] * manager.tileSize[1]
      self.playerPos = (manager.screenWidth / manager.tileSize[0] - 1, None)
    elif direction == "W":
      self.rect.right = (pos[0] + 1) * manager.tileSize[0]
      self.rect.y = pos[1] * manager.tileSize[1]
      self.playerPos = (1, None)
    elif direction == "N":
      self.image = pg.transform.rotate(self.image, 90)
      self.rect.x = pos[0] * manager.tileSize[0]
      self.rect.bottom = (pos[1] + 1) * manager.tileSize[1]
      self.playerPos = (None, 1)
    elif direction == "S":
      self.image = pg.transform.rotate(self.image, -90)
      self.rect.x = pos[0] * manager.tileSize[0]
      self.rect.y = pos[1] * manager.tileSize[1]
      self.playerPos = (manager.screenHeight / manager.tileSize[1] - 1, None)

  def addSelf(self, manager):
    manager.door_group.add(self)

  def open(self, manager):
    if self.isOpen and manager.searchInv(self.item):
      manager.removeCollect(self.item)
      return True


class Button(Sprite):  ############# button ##################

  def __init__(self, image, pos, manager, grid=True, *groups):
    image = pg.transform.scale(pg.image.load(image).convert_alpha(), (manager.tileSize[0] * 8, manager.tileSize[1] * 4))

    super().__init__(image, pos, manager, grid, *groups)

  def isClick(self, *groups):
    mouse_pos = pg.mouse.get_pos()
    mouse_click = pg.mouse.get_pressed()

    if self.rect.collidepoint(mouse_pos):
      if mouse_click[0]:
        return True


class killShadow(Collider):  ########### kill shadow ########

  def __init__(self, rect, manager, *groups):
    image = pg.transform.scale(pg.image.load("sprites/BGs/blackBG.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))
    super().__init__(image, (rect[0], rect[1]), manager,
                     *groups)

    self.rectCoverage = rect
    self.startx = rect[0]
    self.starty = rect[1]
    self.manager = manager
    tempImage = Image.open("sprites/BGs/blackBG.png")

    self.imageWidth, self.imageHeight = image.get_size()
    self.width = rect[2]
    self.height = rect[3]
    self.rect = pg.Rect(rect[0] * manager.tileSize[0], rect[1] * manager.tileSize[1],
                        rect[2] * manager.tileSize[0],
                        rect[3] * manager.tileSize[1])
    self.rect.center = [
        rect[0] * manager.tileSize[0] + self.width * self.imageWidth // 2,
        rect[1] * manager.tileSize[1] + self.height * self.imageHeight // 2
    ]

  def addSelf(self, manager):
    manager.kill_shadow.add(self)

  def draw(self, screen):
    for i in range(round(self.width)):
      for j in range(round(self.height)):
        tempRect = pg.Rect(
            self.startx * self.manager.tileSize[0] + (i * self.imageWidth),
            self.starty * self.manager.tileSize[1] + (j * self.imageHeight),
            self.imageWidth, self.imageHeight)
        screen.blit(self.image, tempRect)


class Wall(Collider):  ############# wall  ##################

  def __init__(self, pos, vertical, num, shadow, manager, *groups):

    wallImage = Image.open("sprites/Walls/wall.png")
    wallImage = wallImage.crop((0, 0, 85, 400))
    wallImage.save( "sprites/Walls/newWall.png")

    wallImage = Image.open("sprites/Walls/solidWall.png")
    wallImage = wallImage.crop((0, 0, 120, 400))
    wallImage.save("sprites/Walls/newSWall.png")

    self.shadow = shadow
    self.vertical = vertical  # boolean
    self.num = num  # number of walls
    if self.shadow:
      image = pg.transform.scale(pg.image.load("sprites/Walls/newSWall.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))
    else:
      image = pg.transform.scale(pg.image.load("sprites/Walls/newWall.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))

    super().__init__(image, pos, manager, shadow, *groups)
    self.startx = pos[0]
    self.starty = pos[1]
    self.manager = manager


    if self.vertical:
      self.width = self.rect.width
      self.height = self.rect.height
      self.rect = pg.Rect(pos[0] * manager.tileSize[0], pos[1] * manager.tileSize[1],
                          self.width, self.height * num)
      self.rect.center = [
          pos[0] * manager.tileSize[0] + self.width / 2,
          pos[1] * manager.tileSize[1] + self.height * num / 2
      ]
    else:
      self.image = pg.transform.rotate(self.image, 90)
      pg.transform.scale(self.image, (manager.tileSize[0], manager.tileSize[1]))
      self.rect = self.image.get_rect()
      self.width = self.rect.width
      self.height = self.rect.height
      self.rect = pg.Rect(pos[0] * manager.tileSize[0], pos[1] * manager.tileSize[1],
                          self.width * num, self.height)
      self.rect.center = [
          pos[0] * manager.tileSize[0] + self.width * num / 2,
          pos[1] * manager.tileSize[1] + self.height / 2
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

  def __init__(self, image, manager, tile=True):
    if not tile:
      image = pg.image.load(image).convert_alpha()
      image = pg.transform.scale(image, (manager.screenWidth, manager.screenHeight))
    else:
      image = pg.transform.scale(pg.image.load(image).convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))

    self.tile = tile


    if tile:
        super().__init__(image, (0,0), manager)
    else:
        super().__init__(image, (manager.screenWidth / 2, manager.screenHeight / 2), manager, False)


  def draw(self, screen):
    if self.tile:
        width, height = screen.get_size()
        for col in range(width // self.rect.width):
          for row in range(height // self.rect.height):
            tempRect = pg.Rect(col * self.rect.width, row * self.rect.height, col,
                               row)
            screen.blit(self.image, tempRect)
    else:
      screen.blit(self.image, self.rect)


class Grid: ################ grid ###################
  def __init__(self, manager):
    self.manager = manager

  def draw(self, screen):
    for i in range(round(self.manager.screenWidth / self.manager.tileSize[0])):
      pg.draw.line(screen, (0, 0, 0), (i * self.manager.tileSize[0], 0), (i * self.manager.tileSize[0], self.manager.screenHeight))
    for i in range(round(self.manager.screenHeight / self.manager.tileSize[1])):
      pg.draw.line(screen, (0, 0, 0), (0, i * self.manager.tileSize[1]), (self.manager.screenWidth, i * self.manager.tileSize[1]))


