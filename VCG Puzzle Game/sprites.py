from msilib.schema import TextStyle
from PIL import Image
from PIL.ImageFilter import FIND_EDGES
import pygame as pg
import pickle
import os.path
from pathlib import Path

pg.init()
screen = pg.display.set_mode((0,0))

devMode = True

def spriteSheet(image, imageWidth, imageHeight, numFrames, gameManager): ################# spriteSheet #############
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
    self.user = 'username'
    self.screen = pg.display.set_mode((0,0), pg.OPENGL | pg.DOUBLEBUF, pg.FULLSCREEN)
    self.tileSize = (round(self.screen.get_width() / 22),  round(self.screen.get_width() / 22))
    self.screenWidth = self.tileSize[0] * 22
    self.screenHeight = self.tileSize[1] * 12
    self.FPS = FPS

    self.devMode = devMode

    self.sceneIndex = [0, [0, 0]]
    self.scenes = []
    self.shadow = False
    self.Player = Player
    self.cage = None
    self.saveState = saveState(self)
    self.undoManager = undoManager(self)
    self.inventoryImage = inventoryImage(self)
    self.dialogueManager = DialogueManager(self)
    self.wall_group = pg.sprite.Group()
    self.box_group = pg.sprite.Group()
    self.colliding_box_group = pg.sprite.Group()
    self.door_group = pg.sprite.Group()
    self.guard_group = pg.sprite.Group()
    self.enemy_group = pg.sprite.Group()
    self.NPC_group = pg.sprite.Group()
    self.collect_group = pg.sprite.Group()
    self.text_group = pg.sprite.Group()
    self.conveyor_group = pg.sprite.Group()
    self.switch_group = pg.sprite.Group()
    self.switchWall_group = pg.sprite.Group()
    self.kill_shadow = pg.sprite.Group()
    self.all_sprites = (self.wall_group,
                        self.box_group,
                        self.colliding_box_group,
                        self.door_group,
                        self.guard_group,
                        self.enemy_group,
                        self.NPC_group,
                        self.collect_group,
                        self.text_group,
                        self.conveyor_group,
                        self.switch_group,
                        self.switchWall_group,
                        self.kill_shadow)

  def clearLevel(self):
    self.cage = None
    self.wall_group.empty()
    self.box_group.empty()
    self.colliding_box_group.empty()
    self.door_group.empty()
    self.guard_group.empty()
    self.enemy_group.empty()
    self.NPC_group.empty
    self.collect_group.empty()
    self.text_group.empty()
    self.conveyor_group.empty()
    self.switch_group.empty()
    self.switchWall_group.empty()
    self.kill_shadow.empty()
    self.undoManager.clearActions()
      
  def checkCollisions(self):
    self.complexCollision(self.Player)
    for guard in self.guard_group:
        if guard.alive:
            self.complexCollision(guard)
    self.boxPush()
    self.undoManager.addActionMovement()
    if self.conveyorPush():
        self.undoManager.addActionConveyor()
    self.collisionReset()
                 
    player_switch = pg.sprite.spritecollide(self.Player, self.switch_group, False) # player * switch
    for switch in player_switch:
       if switch.playerColliding == False:
          switch.switchValues()
          switch.playerColliding = True
    for switch in self.switch_group:
      if switch not in player_switch and switch.playerColliding == True:
        switch.playerColliding = False
    for box in self.box_group:
        box_switch = pg.sprite.spritecollide(box, self.switch_group, False) # box * switch
        for switch in box_switch:
            if box not in switch.boxColliding:
                switch.switchValues()
                switch.boxColliding.append(box)
        for switch in self.switch_group:
            if len(box_switch) <= 0 and box in switch.boxColliding:
                switch.boxColliding.remove(box)
    for guard in self.guard_group:
        if guard.alive:
            guard_switch = pg.sprite.spritecollide(guard, self.switch_group, False) # guard * switch
            for switch in guard_switch:
                if guard not in switch.guardColliding:
                    switch.switchValues()
                    switch.guardColliding.append(guard)  
            for switch in self.switch_group:
                if len(guard_switch) <= 0 and guard in switch.guardColliding:
                    switch.guardColliding.remove(guard)
         
    
    collided_enemies = pg.sprite.spritecollide(self.Player, self.enemy_group, False) # player * enemy
    if len(collided_enemies) > 0:
        self.Player.killed()
    
    collided_killShadow = pg.sprite.spritecollide(self.Player, self.kill_shadow, False) # player * killShadow
    if (len(collided_killShadow) > 0 and self.Player.shadow):
        self.shadow = not(self.shadow)
            
    guard_box = pg.sprite.groupcollide(self.guard_group, self.box_group, False, False)   # guard * box
    for guard, box in guard_box.items():
        if guard.alive and guard.pos_float[0] == guard.preX and guard.pos_float[1] == guard.preY:
            guard.killed()
        
    guard_switchWall = pg.sprite.groupcollide(self.guard_group, self.switchWall_group, False, False) # guard * switchWall
    for guard, switchWalls in guard_switchWall.items():
        if guard.alive:
            for switchWall in switchWalls:
                if switchWall.on:
                    if guard.pos_float[0] == guard.preX and guard.pos_float[1] == guard.preY:
                        guard.killed()
                        break
                
    player_collectible = pg.sprite.spritecollide(self.Player, self.collect_group, False) # player * collectible
    for collect in player_collectible:
        collect.collected()
    
    collided_text = pg.sprite.spritecollide(self.Player, self.text_group, False) # player * text
    for text in self.text_group:
        text.colliding = False
    for text in collided_text:
        text.colliding = True

    collided_NPC = pg.sprite.spritecollide(self.Player, self.NPC_group, False) # player * NPC
    for NPC in self.NPC_group:
      NPC.colliding = False
    for NPC in collided_NPC:
      NPC.colliding = True
          
    player_wall = pg.sprite.spritecollide(self.Player, self.wall_group, False)
    player_box = pg.sprite.spritecollide(self.Player, self.box_group, False)
    player_door = pg.sprite.spritecollide(self.Player, self.door_group, False)
    player_switchWall = pg.sprite.spritecollide(self.Player, self.switchWall_group, False)
    if len(player_wall) > 0 or len(player_box) > 0 or len(player_door) > 0: # colliding real
          self.Player.collidingreal = True
    elif len(player_switchWall) > 0:
        for switchWall in player_switchWall:
            if switchWall.on:
                self.Player.collidingreal = True
        else:
            self.Player.collidingreal = False
    else:
        self.Player.collidingreal = False
        
    self.undoManager.addActionStatus()
    self.undoManager.addFrame()

  def gameCollision(self, obj):
    obj.pos_float[0] = (obj.preX)
    obj.pos_float[1] = (obj.preY)
    obj.rect.x = round(obj.pos_float[0])
    obj.rect.y = round(obj.pos_float[1])
  
  def gamePush(self, obj1, obj2):
    obj2.pos_float[0] += obj1.pos_float[0] - obj1.preX
    obj2.pos_float[1] += obj1.pos_float[1] - obj1.preY
    obj2.rect.x = round(obj2.pos_float[0])
    obj2.rect.y = round(obj2.pos_float[1])
    
  def complexCollision(self, obj):
    collision = False
    isPlayer = False
    isGuard = False
    
    if obj is self.Player: # obj == Player
       isPlayer = True
    elif obj in self.guard_group: # obj == guard
       isGuard = True
       
    if isPlayer: # obj * cage
       if not(self.Player.shadow):
           if self.cage is not None:
               if pg.Rect.colliderect(self.cage.rect, pg.Rect(self.Player.preX, self.Player.preY, self.Player.rect.width, self.Player.rect.height)):
                    self.gameCollision(obj)
                    self.Player.windup = 0
           
    obj_wall = pg.sprite.spritecollide(obj, self.wall_group, False) # obj * wall
    for wall in obj_wall:
       if isPlayer:
           if obj.shadow == wall.shadow or not (obj.shadow):
               self.gameCollision(obj)
               collision = True
       else:
          self.gameCollision(obj)
          collision = True
          if isGuard:
             obj.turnSelf()
       
    obj_switchWall = pg.sprite.spritecollide(obj, self.switchWall_group, False) # obj * switchWall
    for switchWall in obj_switchWall:
       if switchWall.on:
          self.gameCollision(obj)
          collision = True
          if isGuard:
             obj.turnSelf()
          break

    obj_door = pg.sprite.spritecollide(obj, self.door_group, False) # obj * door
    if isPlayer:
        for door in self.door_group:
          door.isOpen = False
        for door in obj_door:
          door.isOpen = True
          self.gameCollision(obj)
          collision = True
          break
    else:
       if len(obj_door) > 0:
          self.gameCollision(obj)
          if isGuard:
             obj.turnSelf()
          collision = True

    if obj in self.guard_group: # guard * box
        obj_box = pg.sprite.spritecollide(obj, self.box_group, False)
        if len(obj_box) > 0:
           self.gameCollision(obj)
           obj.turnSelf()
           collision = True
    
    if not(isPlayer) and (obj.rect.x < 0 or obj.rect.x + obj.rect.width > self.screenWidth or obj.rect.y < 0 or obj.rect.y + obj.rect.height > self.screenHeight):
        self.gameCollision(obj)
        
    if isGuard and collision:
        obj.cover = 0
          
    if isPlayer and collision:
       self.Player.windup = 0
       
    if collision:
       self.collisionReset()
       
    return collision
    
  def collisionReset(self):
     player_box = pg.sprite.spritecollide(self.Player, self.box_group, False)
     for box in player_box:
         if (self.Player.shadow == box.shadow or not (self.Player.shadow)) and box.pos_float[0] == box.preX and box.pos_float[1] == box.preY:
            if self.Player.pos_float[0] == self.Player.preX and self.Player.pos_float[1] == self.Player.preY:
                return False
            self.gameCollision(self.Player)
            self.collisionReset()
            return True
         elif (self.Player.shadow == box.shadow or not (self.Player.shadow)) and self.Player.pos_float[0] == self.Player.preX and self.Player.pos_float[1] == self.Player.preY:
            if box.pos_float[0] == box.preX and box.pos_float[1] == box.preY:
                return False
            else:
                self.Player.killed()
            return False
         
     for box1 in self.box_group:
        box_box = pg.sprite.spritecollide(box1, self.box_group, False)
        for box2 in box_box:
            if box2 is not box1:
               if box1.pos_float[0] == box1.preX and box1.pos_float[1] == box1.preY:
                 if box2.pos_float[0] == box2.preX and box2.pos_float[1] == box2.preY:
                    print("error, stacked boxes")
                    return False
                 self.gameCollision(box2)
                 self.collisionReset()
                 return True
        
  def boxPush(self):
    push = False
    player_box = pg.sprite.spritecollide(self.Player, self.box_group, False) # player * box
    for box in player_box:
        if (self.Player.shadow == box.shadow or not (self.Player.shadow)) and box.preX == box.pos_float[0] and box.preY == box.pos_float[1]:
            self.gamePush(self.Player, box)
            self.complexCollision(box)
            push = True
        elif not(box.preX == box.pos_float[0] and box.preY == box.pos_float[1]):
            #self.Player.killed()
            push = True
    
    for box1 in self.box_group:
        box_box = pg.sprite.spritecollide(box1, self.box_group, False) # box * box
        for box2 in box_box:
            if box2 is not box1:
                self.gamePush(box1, box2)
                self.complexCollision(box2)
                push = True
                if not(box1.pos_float[0] == box1.preX and box1.pos_float[1] == box1.preY) and not(box2.pos_float[0] == box2.preX and box2.pos_float[1] == box2.preY):
                    self.boxPush()
                    
    self.collisionReset()
    
    return push
        
  def conveyorPush(self):
    boxPushed = False
    player_conveyor = pg.sprite.spritecollide(self.Player, self.conveyor_group, False) # player * conveyor
    if len(player_conveyor) == 1:
        for conveyor in player_conveyor:
            if not(conveyor.on):  
                conveyor.on = True
            else:   
                conveyor.move(self.Player)
                self.complexCollision(self.Player)
                if self.boxPush():
                   boxPushed = True
    elif len(player_conveyor) > 1:
        tempArray = [0, 0]
        tempArray[0] = self.Player.pos_float[0]
        tempArray[1] = self.Player.pos_float[1]
        for conveyor in player_conveyor:
            if not(conveyor.on):  
                conveyor.on = True
            else:
                conveyor.move(self.Player)
                self.complexCollision(self.Player)
                if self.boxPush():
                   boxPushed = True
        if not(tempArray[0] == self.Player.pos_float[0] and tempArray[1] == self.Player.pos_float[1]):
            self.gameCollision(self.Player)
   
    box_conveyor = pg.sprite.groupcollide(self.box_group, self.conveyor_group, False, False) # box * conveyor
    for box, conveyors in box_conveyor.items():
        if len(conveyors) == 1:
            if not(conveyors[0].on):  
                conveyors[0].on = True
            else:            
                conveyors[0].move(box)
                self.complexCollision(box)
                if self.boxPush():
                   boxPushed = True
        elif len(conveyors) > 1:
            tempArray = [0, 0]
            tempArray[0] = box.pos_float[0]
            tempArray[1] = box.pos_float[1]
            for conveyor in conveyors:
                if not(conveyor.on):  
                    conveyor.on = True
                else:
                    conveyor.move(box)
                    self.complexCollision(box)
                    if self.boxPush():
                       boxPushed = True
            if not(tempArray[0] == box.pos_float[0] and tempArray[1] == box.pos_float[1]):
                self.gameCollision(box)
              
    guard_conveyor = pg.sprite.groupcollide(self.guard_group, self.conveyor_group, False, False) # guard * conveyor
    for guard, conveyors in guard_conveyor.items():
        if guard.alive:
            if len(conveyors) == 1:
                if not(conveyors[0].on):  
                    conveyors[0].on = True
                else:            
                    conveyors[0].move(guard)
                    self.complexCollision(guard)
            elif len(conveyors) > 1:
                tempArray = [0, 0]
                tempArray[0] = guard.pos_float[0]
                tempArray[1] = guard.pos_float[1]
                for conveyor in conveyors:
                    if not(conveyor.on):  
                        conveyor.on = True
                    else:
                        conveyor.move(guard)
                        self.complexCollision(guard)
                if not(tempArray[0] == guard.pos_float[0] and tempArray[1] == guard.pos_float[1]):
                    self.gameCollision(guard)
    return boxPushed
             
 
class saveState: ########## saveState ###########
    def __init__(self, gameManager):
       self.manager = gameManager
       self.saveSprites = None
       
    def save(self):
      allSpriteData = []
      allSpriteData.append([self.manager.Player.alive])
      for switch in self.manager.switch_group:
           boxArray = []
           guardArray = []
           for box in switch.boxColliding:
              boxArray.append(box.initPos)
           for guard in switch.guardColliding:
              guardArray.append(guard.initPos)
           allSpriteData.append([switch.initPos, switch.on, switch.playerColliding, boxArray, guardArray])
      for switchWall in self.manager.switchWall_group:
           allSpriteData.append([switchWall.initPos, switchWall.on])
      for box in self.manager.box_group:
           allSpriteData.append([box.initPos, box.pos_float])
      for guard in self.manager.guard_group:
           allSpriteData.append([guard.initPos, guard.pos_float, guard.alive, guard.cover, guard.turn, guard.cooldown])

      data = [self.manager.sceneIndex, 
               self.manager.Player.pos_float,
               self.manager.Player.shadow,
               self.manager.inventoryImage.keys.names,
               self.manager.inventoryImage.coins.names,
               self.manager.inventoryImage.maps.names,
               allSpriteData]
      if not os.path.exists(str(Path.home()) + "/breakSaveFiles"):
        os.makedirs(str(Path.home()) + "/breakSaveFiles")
      with open(str(Path.home()) + "/breakSaveFiles/" + self.manager.user + ".dat", "wb") as f:
          pickle.dump(data, f)

    def checkFile(self):
      if os.path.isfile(str(Path.home()) + "/breakSaveFiles/" + self.manager.user + ".dat"):
          return True           
      else:
          return False
      
    def load(self):
        if os.path.isfile(str(Path.home()) + "/breakSaveFiles/" + self.manager.user + ".dat"):
            with open(str(Path.home()) + "/breakSaveFiles/" + self.manager.user + ".dat", "rb") as f:
                sceneIndex, player_pos_float, self.manager.Player.shadow, self.manager.inventoryImage.keys.names, coinNames,  self.manager.inventoryImage.maps.names, self.saveSprites = pickle.load(f)
                self.manager.sceneIndex[0] = sceneIndex[0]
                self.manager.sceneIndex[1] = sceneIndex[1]
                if self.manager.Player.shadow:
                  self.manager.Player.collidingreal = True
                  self.manager.Player.update()
                self.manager.Player.setPos(player_pos_float[0], player_pos_float[1], False)
                if len(coinNames) > 0:
                  self.manager.inventoryImage.coins.num = []
                  Collectible((0,0), "coin", "coin1", self.manager).collected()
                  self.manager.inventoryImage.coins.names.pop()
                  self.manager.inventoryImage.coins.names = []
                  self.manager.inventoryImage.coins.num = []
                self.manager.inventoryImage.coins.names = coinNames
                for name in self.manager.inventoryImage.keys.names:
                  self.manager.inventoryImage.keys.num.append(name)
                for name in self.manager.inventoryImage.coins.names:
                  self.manager.inventoryImage.coins.num.append(name)
                for name in self.manager.inventoryImage.maps.names:
                  self.manager.inventoryImage.maps.num.append(name)
            return True           
        else:
           print("no save file")
           return False
       

class undoManager: ############ undo manager #############
   def __init__(self, manager):
      self.manager = manager
      self.sprite_actions = []
      self.frame = []
      
   def update(self, event):
        if event.key == pg.K_z:
            self.undo()
            
   def undo(self):
      length = len(self.sprite_actions)
      if length > 0:
          for action in self.sprite_actions[length - 1]:
             if action[0] == self.manager.Player:
                 self.setPos(action[0], action[1])
                 if action[3] is not None and not(action[3].playerColliding):
                    action[3].playerColliding = True
                 action[0].direction = action[2]
                 action[0].shadow = action[4]
                 action[0].collidingreal = action[5]
             elif action[0] in self.manager.box_group:
                 self.setPos(action[0], action[1])
                 for switch in self.manager.switch_group:
                    if action[0] in switch.boxColliding:
                        switch.boxColliding.remove(action[0])
                 if action[2] is not None and action[0] not in action[2].boxColliding:
                    action[2].boxColliding.append(action[0])    
             elif action[0] in self.manager.guard_group:
                 if isinstance(action[1], (int)):
                     if action[1]:
                        action[0].revive()
                     else:
                        action[0].killed()
                 else:
                     self.setPos(action[0], action[1])
                     action[0].vision.image= action[2]
                     action[0].cover = action[3]
                     action[0].turn = action[4]
                     action[0].cooldown = action[5]
                     action[0].updateVision()
                     for switch in self.manager.switch_group:
                        if action[0] in switch.guardColliding:
                            switch.guardColliding.remove(action[0])
                     if action[6] is not None and action[0] not in action[6].guardColliding:
                        action[6].guardColliding.append(action[0])
             elif action[0] in self.manager.switch_group:
                action[0].switchValues()
          self.sprite_actions.pop()

   def setPos(self, obj, pos):
      obj.pos_float[0] = pos[0]
      obj.pos_float[1] = pos[1]
      obj.preX = obj.pos_float[0]
      obj.preY = obj.pos_float[1]
      obj.rect.x = round(obj.pos_float[0])
      obj.rect.y = round(obj.pos_float[1])
            
   def clearActions(self):
      self.sprite_actions.clear()
      
   def addActionMovement(self):
      self.frame = []
      if not(self.manager.Player.preX == self.manager.Player.pos_float[0] and self.manager.Player.preY == self.manager.Player.pos_float[1]):
          collidedSwitches = None
          for switch in self.manager.switch_group:
             if switch.playerColliding:
                collidedSwitches = switch
          self.frame.append([self.manager.Player, [self.manager.Player.preX, self.manager.Player.preY], self.manager.Player.preDirection, collidedSwitches, self.manager.Player.preShadow, self.manager.Player.collidingreal])
      for box in self.manager.box_group:
         if not(box.preX == box.pos_float[0] and box.preY == box.pos_float[1]):
            switchCollide = None
            for switch in self.manager.switch_group:
                if box in switch.boxColliding:
                    switchCollide = switch
            self.frame.append([box, [box.preX, box.preY], switchCollide])
      if len(self.frame) > 0:
         for guard in self.manager.guard_group:
            switchCollide = None
            for switch in self.manager.switch_group:
                if guard in switch.guardColliding:
                    switchCollide = switch
                    break
                else:
                    pass
            self.frame.append([guard, [guard.preX, guard.preY], guard.preImage, guard.preCover, guard.preTurn, guard.preCooldown, switchCollide])
   
   def addActionConveyor(self):
      if len(self.frame) > 0:
          for box in self.manager.box_group:
             if not(box.preX == box.pos_float[0] and box.preY == box.pos_float[1]):
                switchCollide = None
                for switch in self.manager.switch_group:
                    if box in switch.boxColliding:
                        switchCollide = switch
                self.frame.append([box, [box.preX, box.preY], switchCollide])

   def addActionStatus(self):
      for switch in self.manager.switch_group:
         if not(switch.preOn == switch.on):
            self.frame.append([switch])  
      for guard in self.manager.guard_group:
          if not(guard.preAlive == guard.alive):
            self.frame.append([guard, guard.preAlive])
  
   def addFrame(self):
      if not(len(self.frame) == 0):
        self.sprite_actions.append(self.frame)
        self.frame = []
      if len(self.sprite_actions) > 100:
         self.sprite_actions.pop(0)


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
          self.rect.x = round((pos[0] + .5) * manager.tileSize[0] - self.rect.width / 2)
          self.rect.y = round((pos[1] + .5) * manager.tileSize[1] - self.rect.height / 2)
        else:
          self.rect.center = (round(pos[0]), round(pos[1]))

  def update(self):
    pass

  def draw(self, screen):
    screen.blit(self.image, self.rect)

  def drawSelf(self, screen, image, rect):
    screen.blit(image, rect)

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
      

class DialogueManager(Sprite): ########## dialogueManager ###########

    def __init__(self, manager):
       self.image = pg.transform.scale(pg.image.load("sprites/Misc/dialogueBox.png").convert_alpha(), (manager.screenWidth - manager.tileSize[0], 4.5 * manager.tileSize[1]))
       self.speakerImage = pg.transform.scale(pg.image.load("sprites/Misc/speakerBox.png").convert_alpha(), (manager.tileSize[0] * 2.5, manager.tileSize[1] * .75))
       super().__init__(self.image, None, manager)
       
       self.rect.x = manager.tileSize[0] * .5
       self.rect.y = manager.tileSize[0] * 7
       self.startx = self.rect.x
       self.starty = self.rect.y
       self.manager = manager
       self.textTimer = 0
       self.show = False
       
       self.text = ""
       self.speakerName = ""
       self.font = pg.font.Font('freesansbold.ttf', round(manager.tileSize[1] / 2))
       self.words = [word.split(' ') for word in self.text.splitlines()]  # 2D array where each row is a list of words.
       self.textColor = (255,255,255)
       self.boxNum = 0
       self.boxIndex = 0
       
    def setText(self, text, speakerName="", color=(255,255,255), size=.5, font='freesansbold.ttf'):
       self.textTimer = 0
       self.boxIndex = 0
       self.text = text
       self.speakerName = speakerName
       self.font = pg.font.Font(font, round(self.manager.tileSize[1] * size))
       self.words = [word.split(' ') for word in text.splitlines()]
       self.textColor = color
       self.show = True
       
    def update(self):
        if self.show:
            self.textTimer += 0
            keys = pg.key.get_pressed()
            if keys[pg.K_RETURN]:
                self.boxIndex += 1
                if self.boxIndex >= self.boxNum:
                    self.show = False
                    self.textTimer = 0
                    self.boxIndex = 0
       
    def draw(self, screen):
      if self.show:
        super().draw(screen)
        margin = [self.manager.tileSize[0] / 3, self.manager.tileSize[1] / 3]
        if not(self.speakerName == ""):
            screen.blit(self.speakerImage, pg.Rect(self.startx, self.starty - self.manager.tileSize[1], 0, 0))
            screen.blit(self.font.render(self.speakerName, 0, self.textColor), pg.Rect(self.startx + margin[0], self.starty - self.manager.tileSize[1] + margin[1] / 2, 0, 0))
        x, y = (self.startx + margin[0], self.starty + margin[1])
        maxX = x
        posArray = [[]]
        imageWidth = self.image.get_width() - (2 * margin[0])
        imageHeight = self.image.get_height() - (2 * margin[1])
        space = self.font.size(' ')[0]  # The width of a space
        i = 0
        for line in self.words:
            for word in line:
                word_surface = self.font.render(word, 0, self.textColor)
                word_width, word_height = self.font.size(word)
                if x + word_width >= (imageWidth + self.startx):
                    x = self.startx + margin[0]  # Reset the x.
                    y += word_height  # Start on new row.
                    if y >= (imageHeight + self.starty):
                        i += 1
                        y = self.starty + margin[1]
                        posArray.append([])
                posArray[i].append((x, y))
                x += word_width + space
                if x > maxX:
                    maxX = x
            x = self.startx + margin[0]  # Reset the x.
            y += word_height
            if y >= (imageHeight + self.starty):
                i += 1
                y = self.starty + margin[1]
                posArray.append([])
        self.boxNum = i
        j = 0
        for line in self.words:
            for word in line:
                word_surface = self.font.render(word, 0, self.textColor)
                screen.blit(word_surface, (posArray[self.boxIndex][j][0], posArray[self.boxIndex][j][1]))
                j += 1
                if len(posArray[self.boxIndex]) <= j:
                    break
        font = pg.font.Font('freesansbold.ttf', round(self.manager.tileSize[1] / 4))
        text = font.render("'ENTER' ->", 0, (225,225,225))
        screen.blit(text, (self.startx + imageWidth - text.get_width(), self.starty + imageHeight - text.get_height(), 0, 0))
        
    

class inventoryImage(Sprite): ############### inventoryImage #################
    def __init__(self, manager, *groups):
      self.manager = manager
      self.font = pg.font.Font('freesansbold.ttf', round(manager.tileSize[1]))
      super().__init__(None, None, manager, *groups)
      manager.inventoryImage = self

      self.collectibles = pg.sprite.Group()
      self.keys = Item(pg.transform.scale(pg.image.load("sprites/Collectibles/key.png").convert_alpha(), (manager.tileSize[0],manager.tileSize[1])))
      self.coins = Item(pg.transform.scale(pg.image.load("sprites/Collectibles/coin.png").convert_alpha(), (manager.tileSize[0],manager.tileSize[1])))
      self.maps = Item(pg.transform.scale(pg.image.load("sprites/Maps/map.png").convert_alpha(), (manager.tileSize[0],manager.tileSize[1])))
      self.collectibles.add(self.keys, self.coins, self.maps)
      self.showMap = False
      self.show = True

    def update(self):
      keys = pg.key.get_pressed()
      if keys[pg.K_m] and self.searchInv("map" + str(self.manager.sceneIndex[0])):
        self.showMap = True
      else:
        self.showMap = False
      if self.manager.devMode and keys[pg.K_h]:
        self.show = False
      else:
        self.show = True

    def addItem(self, collectible):
        if collectible.type == "key":
            self.keys.addItem(collectible)
        elif collectible.type == "coin":
            self.coins.addItem(collectible)
        elif collectible.type == "map":
            self.maps.addItem(collectible)

    def searchMap(self):
        if len(self.maps.num) == 0:
            return False
        return True

    def searchInv(self, name):
        for item in self.collectibles:
            if name in item.names:
                return True
        return False

    def removeCollect(self, name):
        for item in self.collectibles:
            if name in item.num:
              item.num.remove(name)
            if name in item.names:
              item.names.remove(name)
              return True
        return False
    
    def draw(self, screen):
      if self.show:
        i = 0
        if self.showMap:
          #tempSprites = []
          #tempImages = []
          #tempRects = []
          #scale = .2

          #for scene_group in self.manager.scenes:
          #  for scene in scene_group:
          #    if not(scene.blank):
          #      for sprite_group in scene.all_sprites:
          #        if isinstance(sprite_group, list):
          #          for sprite in sprite_group:
          #            tempSprites.append(sprite)
          #            tempImages.append(pg.transform.scale(sprite.image, (round(self.manager.tileSize[0] * scale), round(self.manager.tileSize[1] * scale))))
          #            tempRect = sprite.rect.copy()
          #            tempRect.x = round(tempRect.x * scale)
          #            tempRect.y = round(tempRect.y * scale)
          #            tempRect.width = round(tempRect.width * scale)
          #            tempRect.height = round(tempRect.height * scale)
          #            tempRects.append(tempRect)
          #        else:
          #          if sprite_group is not(self.manager.inventoryImage or self.manager.DialogueManager):
          #            tempSprites.append(sprite_group)
          #            tempImages.append(pg.transform.scale(sprite_group.image, (round(self.manager.tileSize[0] * scale), round(self.manager.tileSize[1] * scale))))
          #            tempRect = sprite_group.rect.copy()
          #            tempRect.x = round(tempRect.x * scale)
          #            tempRect.y = round(tempRect.y * scale)
          #            tempRect.width = round(tempRect.width * scale)
          #            tempRect.height = round(tempRect.height * scale)
          #            tempRects.append(tempRect)
          #width = self.manager.screenWidth * scale
          #height = self.manager.screenHeight * scale
          #shift = [(self.manager.screenWidth - width) / 2, (self.manager.screenHeight - height) / 2]
          #mapSurface = pg.Surface((width, height), pg.SRCALPHA)
          #for rect in tempRects:
          #   rect[0] += shift[0]
          #   rect[1] += shift[1]
          #for i in range(len(tempSprites)):
          #  tempSprites[i].drawSelf(mapSurface, tempImages[i], tempRects[i])
          #screen.blit(mapSurface, shift)
          if os.path.isfile("sprites/Maps/map" + str(self.manager.sceneIndex[0]) + ".png"):
            tempImage = pg.image.load("sprites/Maps/map" + str(self.manager.sceneIndex[0]) + ".png").convert_alpha()
            original_width, original_height = tempImage.get_size()
            if original_width / 22 < original_height / 12:
              new_height = round(self.manager.screenHeight * 3 / 4)
              new_width = round(original_width * (new_height / original_height))
            else:
              new_width = round(self.manager.screenWidth * 3 / 4)
              new_height = round(original_height * (new_width / original_width))
            scaled_image = pg.transform.scale(tempImage, (new_width, new_height))
            tempRect = scaled_image.get_rect()
            tempRect.center = [self.manager.screenWidth // 2, self.manager.screenHeight // 2]
            screen.blit(scaled_image, tempRect)
          else:
            self.manager.dialogueManager.setText("It looks like the map is blank")
        for item in self.collectibles:
          if len(item.num) > 0:
              itemImage = item.image.copy()
              alpha = 128
              itemImage.fill((255, 255, 255, alpha), None, pg.BLEND_RGBA_MULT)
              screen.blit(itemImage, ((2 * i + .5) * self.manager.tileSize[0], .5 * self.manager.tileSize[1], 0, 0))
              text = self.font.render(str(len(item.num)), 0, (0,0,0))
              outline = self.font.render(str(len(item.num)), 0, (255,255,255))
              screen.blit(outline, ((2 * i + 1.75) * self.manager.tileSize[0] + outline.get_height() * .02, .5 * self.manager.tileSize[1] + outline.get_height() * .02, 0, 0))
              screen.blit(outline, ((2 * i + 1.75) * self.manager.tileSize[0] + outline.get_height() * .02, .5 * self.manager.tileSize[1] - outline.get_height() * .02, 0, 0))
              screen.blit(outline, ((2 * i + 1.75) * self.manager.tileSize[0] - outline.get_height() * .02, .5 * self.manager.tileSize[1] + outline.get_height() * .02, 0, 0))
              screen.blit(outline, ((2 * i + 1.75) * self.manager.tileSize[0] - outline.get_height() * .02, .5 * self.manager.tileSize[1] - outline.get_height() * .02, 0, 0))
              screen.blit(text, ((2 * i + 1.75) * self.manager.tileSize[0], .5 * self.manager.tileSize[1], 0, 0))
              i += 1
        text = self.font.render("FL " + str(self.manager.sceneIndex[0]), 0, (0,0,0))
        outline = self.font.render("FL " + str(self.manager.sceneIndex[0]), 0, (255,255,255))
        screen.blit(outline, ((19) * self.manager.tileSize[0] + outline.get_height() * .02, .5 * self.manager.tileSize[1] + outline.get_height() * .02, 0, 0))
        screen.blit(outline, ((19) * self.manager.tileSize[0] + outline.get_height() * .02, .5 * self.manager.tileSize[1] - outline.get_height() * .02, 0, 0))
        screen.blit(outline, ((19) * self.manager.tileSize[0] - outline.get_height() * .02, .5 * self.manager.tileSize[1] + outline.get_height() * .02, 0, 0))
        screen.blit(outline, ((19) * self.manager.tileSize[0] - outline.get_height() * .02, .5 * self.manager.tileSize[1] - outline.get_height() * .02, 0, 0))
        screen.blit(text, ((19) * self.manager.tileSize[0], .5 * self.manager.tileSize[1], 0, 0))
        

class Item(Sprite): ############ Item #################

    def __init__(self, image, *groups):
        self.names = []
        self.num = []
        self.image = image
        
        super().__init__(image, None, None, *groups)

    def addItem(self, collectible):
        self.num.append(collectible.name)
        self.names.append(collectible.name)
        self.image = collectible.image

    def clear(self):
      self.num.clear()
      self.names.clear()


class Collectible(Collider):  ####### Collectible #########

  def __init__(self, pos, collectType, name, manager, *groups):
    if collectType == "key":
        image = pg.transform.scale(pg.image.load("sprites/Collectibles/key.png").convert_alpha(), (manager.tileSize[0],manager.tileSize[1]))
        self.frames = [image]
    elif collectType == "coin":
        self.frames = spriteSheet("sprites/Collectibles/coin.png", 32, 32, 10, manager)
        image = self.frames[0]
    elif collectType == "map":
        image = pg.transform.scale(pg.image.load("sprites/Maps/map.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))
        self.frames = [image]
    else:
        image = pg.transform.scale(pg.image.load("sprites/Collectibles/key.png").convert_alpha(), (manager.tileSize[0],
            manager.tileSize[1]))
        self.frames = [image]

    self.clock = 0
    self.globalFPS = manager.FPS

    self.inInventory = False
    self.type = collectType
    self.name = name
    self.manager = manager
    super().__init__(image, pos, manager, *groups)
    
  def collected(self):
    if self.type == "map" and not(self.manager.inventoryImage.searchMap()):
       self.manager.dialogueManager.setText("'those who are lost will find direction'\n\npress 'M' to open the map. ('ENTER' to close dialogue)")
    self.image = self.frames[0]
    self.inInventory = True
    self.manager.inventoryImage.addItem(self)
    self.kill()

  def draw(self, screen):
    if not(self.inInventory):
      screen.blit(self.image, self.rect)

  def addSelf(self, manager):
    if manager.inventoryImage.searchInv(self.name):
        self.kill()
    else:
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
    # made player file png
    playerImage = pg.transform.scale(pg.image.load("sprites/Player/Player.png").convert_alpha(), (manager.tileSize[0] * 4 // 5, manager.tileSize[1] * 4 // 5))
    shadowImage = Image.open("sprites/Player/Player.png")
    shadowImage = shadowImage.filter(FIND_EDGES)
    shadowImage.putalpha(128)
    shadowImage.save("sprites/Player/SPShadow.png")
    shadowPlayerImage = pg.transform.scale(pg.image.load("sprites/Player/SPShadow.png").convert_alpha(), (manager.tileSize[0] * 4 // 5, manager.tileSize[1] * 4 // 5))

    self.pos_float = [(pos[0] + .5) * manager.tileSize[0] - playerImage.get_width() / 2, (pos[1] + .5) * manager.tileSize[1] - playerImage.get_height() / 2]
    self.preX = self.pos_float[0]
    self.preY = self.pos_float[1]

    super().__init__(playerImage, pos, manager,
                     *groups)
    self.collidingreal = False
    self.shadow = False
    self.preShadow = self.shadow
    self.alive = True

    self.direction = "S"
    self.preDirection = self.direction
    self.clock = 0
    self.globalFPS = manager.FPS

    # animation lists
    self.walkN = [pg.transform.scale(pg.transform.rotate(playerImage, 180), (manager.tileSize[0] * 4 // 5, manager.tileSize[1] * 4 // 5))]
    self.walkE = [pg.transform.scale(pg.transform.rotate(playerImage, 90), (manager.tileSize[0] * 4 // 5, manager.tileSize[1] * 4 // 5))]
    self.walkS = [playerImage]
    self.walkW = [pg.transform.scale(pg.transform.rotate(playerImage, -90), (manager.tileSize[0] * 4 // 5, manager.tileSize[1] * 4 // 5))]
    self.SWalkN = [pg.transform.scale(pg.transform.rotate(shadowPlayerImage, 180), (manager.tileSize[0] * 4 // 5, manager.tileSize[1] * 4 // 5))]
    self.SWalkE = [pg.transform.scale(pg.transform.rotate(shadowPlayerImage, 90), (manager.tileSize[0] * 4 // 5, manager.tileSize[1] * 4 // 5))]
    self.SWalkS = [shadowPlayerImage]
    self.SWalkW = [pg.transform.scale(pg.transform.rotate(shadowPlayerImage, -90), (manager.tileSize[0] * 4 // 5, manager.tileSize[1] * 4 // 5))]

    self.frames = self.walkS

    self.cooldown = 0
    self.windup = 0

    self.hide = False
    
    manager.Player = self
    self.manager = manager

  def update(self):
    self.preX = self.pos_float[0]
    self.preY = self.pos_float[1]
    self.preDirection = self.direction
    self.preShadow = self.shadow
    keys = pg.key.get_pressed()

    if self.direction == "N":
      if keys[pg.K_a] or keys[pg.K_LEFT]:
        self.direction = "W"
        self.move(-1, 0)
        self.cooldown = self.manager.FPS
      elif keys[pg.K_d] or keys[pg.K_RIGHT]:
        self.direction = "E"
        self.move(1, 0)
        self.cooldown = self.manager.FPS
      elif keys[pg.K_w] or keys[pg.K_UP]:
        if self.cooldown <= 0:
           self.move(0, -1)
           self.cooldown = self.manager.FPS
        else:
          self.cooldown -= self.windup
      elif keys[pg.K_s] or keys[pg.K_DOWN]:
        self.direction = "S"
        self.move(0, 1)
        self.cooldown = self.manager.FPS
    if self.direction == "E":
      if keys[pg.K_a] or keys[pg.K_LEFT]:
        self.direction = "W"
        self.move(-1, 0)
        self.cooldown = self.manager.FPS
      elif keys[pg.K_d] or keys[pg.K_RIGHT]:
        if self.cooldown <= 0:
           self.move(1, 0)
           self.cooldown = self.manager.FPS
        else:
          self.cooldown -= self.windup
      elif keys[pg.K_w] or keys[pg.K_UP]:
        self.direction = "N"
        self.move(0, -1)
        self.cooldown = self.manager.FPS
      elif keys[pg.K_s] or keys[pg.K_DOWN]:
        self.direction = "S"
        self.move(0, 1)
        self.cooldown = self.manager.FPS
    if self.direction == "S":
      if keys[pg.K_a] or keys[pg.K_LEFT]:
        self.direction = "W"
        self.move(-1, 0)
        self.cooldown = self.manager.FPS
      elif keys[pg.K_d] or keys[pg.K_RIGHT]:
        self.direction = "E"
        self.move(1, 0)
        self.cooldown = self.manager.FPS
      elif keys[pg.K_w] or keys[pg.K_UP]:
        self.direction = "N"
        self.move(0, -1)
        self.cooldown = self.manager.FPS
      elif keys[pg.K_s] or keys[pg.K_DOWN]:
        if self.cooldown <= 0:
           self.move(0, 1)
           self.cooldown = self.manager.FPS
        else:
          self.cooldown -= self.windup
    if self.direction == "W":
      if keys[pg.K_a] or keys[pg.K_LEFT]:
        if self.cooldown <= 0:
           self.move(-1, 0)
           self.cooldown = self.manager.FPS
        else:
          self.cooldown -= self.windup
      elif keys[pg.K_d] or keys[pg.K_RIGHT]:
        self.direction = "E"
        self.move(1, 0)
        self.cooldown = self.manager.FPS
      elif keys[pg.K_w] or keys[pg.K_UP]:
        self.direction = "N"
        self.move(0, -1)
        self.cooldown = self.manager.FPS
      elif keys[pg.K_s] or keys[pg.K_DOWN]:
        self.direction = "S"
        self.move(0, 1)
        self.cooldown = self.manager.FPS
    
    if not (keys[pg.K_w]) and not (keys[pg.K_a]) and not (
        keys[pg.K_s]) and not (keys[pg.K_d]) and not (keys[pg.K_LEFT]) and not (keys[pg.K_RIGHT]) and not (keys[pg.K_UP]) and not (keys[pg.K_DOWN]):
      self.cooldown = 0

    if self.cooldown <= 0:
      if self.preX == self.rect.x and self.preY == self.rect.y:
        self.windup = 0
    else:
      self.windup += 1
      if keys[pg.K_LSHIFT]:
          self.windup = self.manager.FPS / 2
      else:
          if self.windup > self.manager.FPS / 6:
            self.windup = self.manager.FPS / 6
      
    if keys[pg.K_SPACE]:
      self.shadow = True
    elif keys[pg.K_SPACE] is False and not (self.collidingreal):
      self.shadow = False
      
    if self.manager.devMode and keys[pg.K_h]:
        self.hide = True
    else:
        self.hide = False

    if self.shadow:
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

  def setPos(self, x, y, scaled=True):
    if scaled:
        if x is not None:
            self.rect.x = (x + .5) * self.manager.tileSize[0] - self.rect.width / 2
            self.pos_float[0] = (x + .5) * self.manager.tileSize[0] - self.rect.width / 2
        if y is not None:
            self.rect.y = (y + .5) * self.manager.tileSize[1] - self.rect.height / 2
            self.pos_float[1] = (y + .5) * self.manager.tileSize[1] - self.rect.height / 2
    else:
        self.pos_float[0] = x
        self.pos_float[1] = y
        self.rect.x = x
        self.rect.y = y

  def draw(self, screen):
    if not(self.hide):
        if self.alive:
            screen.blit(self.image, self.rect)


class NPC(Collider): ################ NPC #############
  def __init__(self, image, pos, text, condition, manager, *groups):
    self.text = text
    self.condition = condition
    self.colliding = False
    self.textIndex = [0,0]
    self.manager = manager
    super().__init__(image, pos, manager, False, True, *groups)

  def setDialogue(self, events):
    if self.colliding:
      for event in events:
        self.manager.dialogueManager.setText(self.text[self.textIndex[0]][self.textIndex[1]])
        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
          if self.condition:
            if not(self.manager.inventoryImage.searchInv("map6")):
              Collectible((0,0), "map", "map6", self.manager).collected()
              self.manager.inventoryImage.coins.clear()
            if len(self.text) > self.textIndex[0] + 1:
              self.textIndex[1] = 0
              self.textIndex[0] += 1
            elif len(self.text[self.textIndex[0]]) > self.textIndex[1] + 1:
              self.textIndex[1] += 1
          else:
            if len(self.text[self.textIndex[0]]) > self.textIndex[1] + 1:
              self.textIndex[1] += 1

  def addSelf(self, manager):
    manager.NPC_group.add(self)


class Cage(Collider): ################## cage ################ 
    def __init__(self, pos, manager, *groups):
        image = pg.transform.scale(pg.image.load("sprites/Cage/cage.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]), )
        self.pos = pos
        super().__init__(image, pos, manager, False, True, *groups)
        
    def addSelf(self, manager):
       manager.cage = self


class text(Collider):  ################ text ###############

  def __init__(self, pos, width, text, manager, textSize=.5, textColor=(0,0,0), font='freesansbold.ttf', *groups):

    self.manager = manager
    image = pg.transform.scale(pg.image.load("sprites/Misc/textBubble.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))
    self.font = pg.font.Font(font, round(textSize * manager.tileSize[1]))

    self.text = text
    self.words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    self.textColor = textColor

    self.colliding = False

    self.startx = ((pos[0] + .5) * manager.tileSize[0])
    self.starty = ((pos[1] + .5) * manager.tileSize[1])

    self.textBoxWdith = width * manager.tileSize[0]

    super().__init__(image, pos, manager, True, *groups)

  def draw(self, screen):

    if self.colliding:
      #self.manager.dialogueManager.setText("the most common pencil casing is thin wood, usually hexagonal in section, but sometimes cylindrical or triangular, permanently bonded to the core. Casings may be of other materials, such as plastic or paper. To use the pencil, the casing must be carved or peeled off to expose the working end of the core as a sharp point. Mechanical pencils have more elaborate casings which are not bonded to the core; instead, they support separate, mobile pigment cores that can be extended or retracted (usually through the casing's tip) as needed. These casings can be reloaded with new cores (usually graphite) as the previous ones are exhausted. As a technique for drawing, the closest predecessor to the pencil was silverpoint or leadpoint until in 1565 (some sources say as early as 1500), a large deposit of graphite was discovered on the approach to Grey Knotts from the hamlet of Seathwaite in Borrowdale parish, Cumbria, England.[4][5][6][7] This particular deposit of graphite was extremely pure and solid, and it could easily be sawn into sticks. It remains the only large-scale deposit of graphite ever found in this solid form.", "Sam")
      x, y = (self.startx, self.starty)
      maxX = x
      posArray = []
      space = self.font.size(' ')[0]  # The width of a space
      for line in self.words:
          for word in line:
              word_surface = self.font.render(word, 0, self.textColor)
              word_width, word_height = self.font.size(word)
              if x + word_width >= (self.textBoxWdith + self.startx):
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


class Conveyor(Collider): ############## conveyor ##############
  def __init__(self, pos, direction, manager, *groups):
    self.frames = spriteSheet("sprites/Conveyors/conveyorSpriteSheet.png", 32, 32, 4, manager)
    
    self.clock = 0
    self.frameNum = 0
    
    self.direction = direction
    self.on = False
    self.manager = manager
    
    if self.direction == "N":
        for i in range(len(self.frames)):
          self.frames[i] = pg.transform.scale(pg.transform.rotate(self.frames[i], 90), (manager.tileSize[0], manager.tileSize[1]))
    elif self.direction == "S":
        for i in range(len(self.frames)):
          self.frames[i] = pg.transform.scale(pg.transform.rotate(self.frames[i], -90), (manager.tileSize[0], manager.tileSize[1]))
    elif self.direction == "W":
        for i in range(len(self.frames)):
          self.frames[i] = pg.transform.scale(pg.transform.rotate(self.frames[i], 180), (manager.tileSize[0], manager.tileSize[1]))

    image = self.frames[0]
    

    
    super().__init__(image, pos, manager, True, *groups)
    
  def addSelf(self, manager):
    manager.conveyor_group.add(self)

  def animate(self):
    if not(self.on):
        self.frameNum = 0
    else:
        self.clock += 1

        if self.clock % 10 == 0:
            self.frameNum += 1
            if self.frameNum >= len(self.frames):
              self.clock = 0
              self.frameNum = 0
              self.on = False
          
    self.image = self.frames[self.frameNum]

  def move(self, collidable):
      tempArray = [0,0]
      if self.direction == "N":
        for frame in self.frames:
            tempArray = [0, -self.manager.tileSize[1] / 2]
      elif self.direction == "S":
        for frame in self.frames:
            tempArray = [0, self.manager.tileSize[1] / 2]
      elif self.direction == "W":
        for frame in self.frames:
            tempArray = [-self.manager.tileSize[0] / 2, 0]
      elif self.direction == "E":
            tempArray = [self.manager.tileSize[0] / 2, 0]
      else:
          print("Error, Conveyor direction inputed wrong. direction is: " + str(self.direction) + " should be either N, E, S, or W")
          raise Exception
      collidable.preX = collidable.pos_float[0]
      collidable.preY = collidable.pos_float[1]
      collidable.pos_float[0] += tempArray[0]
      collidable.pos_float[1] += tempArray[1]
      collidable.rect.x = round(collidable.pos_float[0])
      collidable.rect.y = round(collidable.pos_float[1])


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
               turn=False,
               *groups):
    image = pg.transform.scale(pg.image.load("sprites/Enemies/Guard.png").convert_alpha(), (manager.tileSize[0] * 4 // 5, manager.tileSize[1] * 4 // 5))
    
    self.pos_float = [(pos[0] + .5) * manager.tileSize[0] - image.get_width() / 2, (pos[1] + .5) * manager.tileSize[1] - image.get_height() / 2]
    self.initPos = [self.pos_float[0], self.pos_float[1]]
    
    self.distance = distance
    self.cover = 0
    self.preCover = 0

    self.hor = hor
    self.turn = turn
    self.preTurn = turn

    self.preX = (pos[0] + .5) * manager.tileSize[0] - image.get_width() / 2
    self.preY = (pos[1] + .5) * manager.tileSize[1] - image.get_height() / 2

    self.cooldown = 0
    self.preCooldown = 0
    self.windup = speed

    super().__init__(image, pos, manager, *groups)

    self.manager = manager

    self.alive = True
    self.preAlive = True

    self.vision = visionCone(self)

    if not(hor):
      self.vision.image = pg.transform.scale(pg.transform.rotate(self.vision.image, -90), (manager.tileSize[0] * 3, manager.tileSize[1] * 2))
      self.image = pg.transform.scale(pg.transform.rotate(self.image, 90), (manager.tileSize[0] * 4 // 5, manager.tileSize[1] * 4 // 5))
    else:
      self.vision.image = pg.transform.scale(pg.transform.rotate(self.vision.image, 180), (manager.tileSize[0] * 2, manager.tileSize[1] * 3))
    if turn:
      self.vision.image = pg.transform.rotate(self.vision.image, -180)
    self.preImage = self.vision.image
      

  def killed(self):
      self.alive = False
      self.manager.enemy_group.remove(self.vision)
      self.manager.enemy_group.remove(self)

  def revive(self):
      self.alive = True
      self.manager.enemy_group.add(self)
      self.manager.enemy_group.add(self.vision)

  def update(self):
    self.preAlive = self.alive
    self.preImage = self.vision.image
    self.preCover = self.cover
    self.preTurn = self.turn
    self.preCooldown = self.cooldown
    if self.alive:
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

  def updateVision(self):
    if self.hor:
        if self.turn:
            self.vision.rect = self.vision.image.get_rect(midright=self.rect.center)
        else:
            self.vision.rect = self.vision.image.get_rect(midleft=self.rect.center)
    else:
        if self.turn:
            self.vision.rect = self.vision.image.get_rect(midbottom=self.rect.center)
        else:
            self.vision.rect = self.vision.image.get_rect(midtop=self.rect.center)

  def turnSelf(self):
    if self.alive:
        self.vision.image = pg.transform.rotate(self.vision.image, 180)
        self.image = pg.transform.scale(pg.transform.rotate(self.image, 180), (self.manager.tileSize[0] * 4 // 5, self.manager.tileSize[1] * 4 // 5))
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
    if self.alive:
      manager.enemy_group.add(self)
      manager.enemy_group.add(self.vision)

  def draw(self, screen):
    if self.alive:
        screen.blit(self.image, self.rect)
        screen.blit(self.vision.image, self.vision.rect)


class Box(Collider):  ############### box ################
  def __init__(self, pos, shadow, manager, *groups):
    if not shadow:
        image = pg.transform.scale(pg.image.load("sprites/Boxes/NewBox.png").convert_alpha(), (manager.tileSize[0] * 4 // 5, manager.tileSize[1] * 4 // 5))
    else:
        image = pg.transform.scale(pg.image.load("sprites/Boxes/NewSBox.png").convert_alpha(), (manager.tileSize[0] * 4 // 5, manager.tileSize[1] * 4 // 5))

    self.pos_float = [(pos[0] + .5) * manager.tileSize[0] - image.get_width() / 2, (pos[1] + .5) * manager.tileSize[1] - image.get_height() / 2]
    self.initPos = [self.pos_float[0], self.pos_float[1]]
    self.shadow = shadow

    super().__init__(image, pos, manager, shadow, *groups)

    self.preX = self.rect.x
    self.preY = self.rect.y

    self.pushed = False

  def update(self):
    self.pushed = False
    self.preX = self.pos_float[0]
    self.preY = self.pos_float[1]

  def addSelf(self, manager):
    manager.box_group.add(self)


class Switch(Collider):  ############ switch #############
  def __init__(self, pos, switchWalls, manager, *groups):
    redSwitchOff = pg.transform.scale(pg.image.load("sprites/Switches/redSwitchOff.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))
    redSwitchOn = pg.transform.scale(pg.image.load("sprites/Switches/redSwitchOn.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))

    blueSwitchOff = pg.transform.scale(pg.image.load("sprites/Switches/blueSwitchOff.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))
    blueSwitchOn = pg.transform.scale(pg.image.load("sprites/Switches/blueSwitchOn.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))

    greenSwitchOff = pg.transform.scale(pg.image.load("sprites/Switches/greenSwitchOff.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))
    greenSwitchOn = pg.transform.scale(pg.image.load("sprites/Switches/greenSwitchOn.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))

    self.frames = ((redSwitchOff, redSwitchOn), (blueSwitchOff, blueSwitchOn), (greenSwitchOff, greenSwitchOn))

    self.color = switchWalls[0].color

    if self.color == "red":
      image = self.frames[0][0]
    elif self.color == "blue":
      image = self.frames[1][0]
    else:
      image = self.frames[2][0]

    super().__init__(image, pos, manager, *groups)
    self.initPos = [self.rect.x, self.rect.y]
    self.switchWall_group = pg.sprite.Group(switchWalls)
    self.playerColliding = False
    self.boxColliding = []
    self.guardColliding = []
    self.on = False
    self.preOn = False

  def addSelf(self, manager):
    manager.switch_group.add(self)

  def update(self):
    self.preOn = self.on
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


    self.color = color

    self.on = on
    self.preOn = on

    super().__init__(image, pos, manager, True)
    self.initPos = [self.rect.x, self.rect.y]
    
    self.update()

  def update(self):
    self.preOn = self.on
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
      self.image = pg.transform.scale(pg.transform.rotate(self.image, 180), (manager.tileSize[0], manager.tileSize[1] * 2))
      self.rect.x = pos[0] * manager.tileSize[0]
      self.rect.y = pos[1] * manager.tileSize[1]
      self.playerPos = (manager.screenWidth / manager.tileSize[0] - 2, None)
    elif direction == "W":
      self.rect.right = (pos[0] + 1) * manager.tileSize[0]
      self.rect.y = pos[1] * manager.tileSize[1]
      self.playerPos = (1, None)
    elif direction == "N":
      self.image = pg.transform.scale(pg.transform.rotate(self.image, 90), (manager.tileSize[0], manager.tileSize[1] * 2))
      self.rect.x = pos[0] * manager.tileSize[0]
      self.rect.bottom = (pos[1] + 1) * manager.tileSize[1]
      self.playerPos = (None, 1)
    elif direction == "S":
      self.image = pg.transform.scale(pg.transform.rotate(self.image, -90), (manager.tileSize[0], manager.tileSize[1] * 2))
      self.rect.x = pos[0] * manager.tileSize[0]
      self.rect.y = pos[1] * manager.tileSize[1]
      self.playerPos = (manager.screenHeight / manager.tileSize[1] - 2, None)

  def addSelf(self, manager):
    manager.door_group.add(self)

  def open(self, manager):
    if self.isOpen and manager.inventoryImage.searchInv(self.item):
      if self.item in manager.inventoryImage.keys.num:
        manager.inventoryImage.keys.num.remove(self.item)
      return True
    elif self.isOpen:
       manager.dialogueManager.setText("Missing" + " key. ('ENTER' to close dialogue)")


class Button(Sprite):  ############# button ##################

  def __init__(self, image, pos, manager, grid=True, condition=True, *groups):
    self.condition = condition
    self.mouseHover = False

    super().__init__(image, pos, manager, grid, *groups)
    self.image.fill((255, 255, 255), special_flags=pg.BLEND_RGB_SUB) 
    if not(self.condition):
      brighten = 128
      self.image.fill((brighten, brighten, brighten), special_flags=pg.BLEND_RGB_ADD) 

  def isClick(self):
    if self.condition:
      mouse_pos = pg.mouse.get_pos()
      mouse_click = pg.mouse.get_pressed()

      if self.rect.collidepoint(mouse_pos):
        if mouse_click[0]:
          return True
    return False
      
  def animate(self):
    if self.condition:
      mouse_pos = pg.mouse.get_pos()
      brighten = 255
      if self.rect.collidepoint(mouse_pos) and not(self.mouseHover):
        self.image.fill((brighten, brighten, brighten), special_flags=pg.BLEND_RGB_ADD) 
        self.mouseHover = True
      elif not(self.rect.collidepoint(mouse_pos)) and self.mouseHover:
        self.image.fill((brighten, brighten, brighten), special_flags=pg.BLEND_RGB_SUB) 
        self.mouseHover = False


class killShadow(Collider):  ########### kill shadow ########
  def __init__(self, rect, manager, *groups):
    image = pg.transform.scale(pg.image.load("sprites/BGs/blackBG.png").convert_alpha(), (manager.tileSize[0], manager.tileSize[1]))
    super().__init__(image, (rect[0], rect[1]), manager,
                     *groups)

    
    self.startx = rect[0]
    self.starty = rect[1]
    self.manager = manager
    tempImage = Image.open("sprites/BGs/blackBG.png")

    self.imageWidth, self.imageHeight = image.get_size()
    self.width = rect[2]
    self.height = rect[3]
    self.rect = pg.Rect(rect[0] * manager.tileSize[0], 
                        rect[1] * manager.tileSize[1],
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

  def drawSelf(self, screen, image, rect):
    imageWidth, imageHeight = image.get_size()
    for i in range(round(self.width)):
      for j in range(round(self.height)):
        tempRect = pg.Rect(
            rect[0] + (i * imageWidth),
            rect[1] + (j * imageHeight),
            imageWidth, imageHeight)
        screen.blit(image, tempRect)


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
      self.image = pg.transform.scale(pg.transform.rotate(self.image, 90), (manager.tileSize[0], manager.tileSize[1]))
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
  
  def drawSelf(self, screen, image, rect):
    for i in range(self.num):
      if (self.vertical):
        tempRect = pg.Rect(rect[0], rect[1] + i * rect[3],
                           rect[2], rect[3])
        screen.blit(image, tempRect)
      else:
        tempRect = pg.Rect(rect[0] + i * rect[2], rect[1], 
                           rect[2], rect[3])
        screen.blit(image, tempRect)


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

  def drawSelf(self, screen, image, rect):
    if self.tile:
        for col in range(22):
          for row in range(12):
            tempRect = pg.Rect(col * rect.width, row * rect.height, col,
                               row)
            screen.blit(image, tempRect)
    else:
      screen.blit(image, rect)


class Grid: ################ grid ###################
  def __init__(self, manager):
    self.manager = manager
    self.hide = True
    self.drawAllRect = False

  def update(self):
     keys = pg.key.get_pressed()
        
     if self.manager.devMode and keys[pg.K_g]:
         self.hide = False
         self.drawAllRect = True
     else:
         self.hide = True
         self.drawAllRect = False

  def draw(self, screen):
    if not self.hide:
        for i in range(round(self.manager.screenWidth / self.manager.tileSize[0])):
          pg.draw.line(screen, (0, 0, 0), (i * self.manager.tileSize[0], 0), (i * self.manager.tileSize[0], self.manager.screenHeight))
        for i in range(round(self.manager.screenHeight / self.manager.tileSize[1])):
          pg.draw.line(screen, (0, 0, 0), (0, i * self.manager.tileSize[1]), (self.manager.screenWidth, i * self.manager.tileSize[1]))