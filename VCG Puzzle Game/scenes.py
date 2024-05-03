from http.client import NETWORK_AUTHENTICATION_REQUIRED
from sys import exit
from PIL import Image
import pygame as pg
import sprites as spr
from shader import Shader, update_shader
from crt_shader import Graphic_engine
import os


class scene:

  def __init__(self, gameManager, all_sprites, blank=False, *groups):
    pg.init()
    self.blank = blank
    self.shadowSpawn = []
    self.cage = None
    if not blank:
        if gameManager.devMode:
          self.grid = spr.Grid(gameManager)

        self.gameManager = gameManager

        for sprite in all_sprites:
          sprite.addSelf(self.gameManager)

        for killShadow in self.gameManager.kill_shadow:
          self.shadowSpawn.append(killShadow.rect)
          
        self.cage = self.gameManager.cage

        self.gameManager.clearLevel()

        self.screen = gameManager.screen
        self.surface = pg.Surface((self.gameManager.screenWidth, self.gameManager.screenHeight), pg.SRCALPHA)
        #self.surface = pg.Surface((self.gameManager.screenWidth, self.gameManager.screenHeight), pg.SRCALPHA).convert((255, 65282, 16711681, 0))
        self.lowerBound = pg.Surface(
            (self.gameManager.screen.get_width(), self.gameManager.screen.get_height() - self.gameManager.screenHeight))
        self.upperBound = pg.Surface(
            (self.gameManager.screen.get_width() - self.gameManager.screenWidth, self.gameManager.screen.get_height()))
        self.clock = pg.time.Clock()

        gameManager.Player.alive = True

        font = pg.font.Font('freesansbold.ttf', int(gameManager.tileSize[1]))
        pausedText = font.render("Paused", True, (0, 0, 0))
        
        font = pg.font.Font('freesansbold.ttf', int(gameManager.tileSize[1]))
        deadText = font.render("You Died", True, (255, 0, 0))
        font = pg.font.Font('freesansbold.ttf', int(gameManager.tileSize[1] * 3 / 4))
        returnText = font.render("Press r to restart or z to undo", True, (255, 0, 0))

        self.menuText = pg.sprite.Group(
            spr.Sprite(pausedText, (gameManager.screenWidth // 2,
                       gameManager.screenHeight // 2), gameManager,
                       False, *groups))
        self.deadText = pg.sprite.Group(
            spr.Sprite(deadText, (gameManager.screenWidth // 2,
                       gameManager.screenHeight // 2), self.gameManager,
                       False, *groups),
            spr.Sprite(
                returnText,
                (gameManager.screenWidth // 2,
                gameManager.screenHeight // 2 + int(gameManager.tileSize[1])),
                self.gameManager,
                False,
            ))

        font = pg.font.Font('freesansbold.ttf', int(gameManager.tileSize[1] * 1 / 2))
        exitText = font.render("save and exit", True, (0, 0, 0))
        self.exitButton = spr.Button(exitText, (gameManager.screenWidth // 2,
                       (gameManager.screenHeight // 2) + gameManager.tileSize[1]), gameManager,
                       False)

        self.all_sprites = pg.sprite.Group()

        for group in all_sprites:
          if group is not (None):
            self.all_sprites.add(pg.sprite.Group(group))
        self.all_sprites.add(pg.sprite.Group(gameManager.inventoryImage))
        self.all_sprites.add(pg.sprite.Group(gameManager.dialogueManager))

  def main(self):
    
    if self.blank:
      raise IndexError
  
    self.gameManager.clearLevel()

    for sprite in self.all_sprites:
      sprite.addSelf(self.gameManager)
    
    if self.gameManager.saveState.saveSprites is not None:
        for saveSprite in self.gameManager.saveState.saveSprites:
            if isinstance(saveSprite[0], (int)):
               if not(saveSprite[0]):
                  self.gameManager.Player.killed()
            for box in self.gameManager.box_group:
                if box.pos_float == saveSprite[0]:
                    box.pos_float = saveSprite[1]
                    box.rect.x = round(box.pos_float[0])
                    box.rect.y = round(box.pos_float[1])
                    break
            for guard in self.gameManager.guard_group:
                if guard.pos_float == saveSprite[0]:
                    guard.pos_float = saveSprite[1]
                    guard.rect.x = round(guard.pos_float[0])
                    guard.rect.y = round(guard.pos_float[1])
                    if not(saveSprite[2]):
                      guard.killed()
                    guard.cover = saveSprite[3]
                    guard.turn = saveSprite[4]
                    if guard.turn:
                      guard.vision.image = pg.transform.rotate(guard.vision.image, 180)
                    guard.cooldown = saveSprite[5]
                    guard.updateVision()
                    break
            for switch in self.gameManager.switch_group:
                if [switch.rect.x, switch.rect.y] == saveSprite[0]:
                    switch.on = saveSprite[1]
                    switch.playerColliding = saveSprite[2]
                    for pos in saveSprite[3]:
                       for box in self.gameManager.box_group:
                          if box.pos_float == pos:
                             switch.boxColliding.append(box)
                             break
                    for pos in saveSprite[4]:
                       for guard in self.gameManager.guard_group:
                          if guard.pos_float == pos:
                             switch.boxColliding.append(guard)
                             break
                    break
            for switchWall in self.gameManager.switchWall_group:
                if [switchWall.rect.x, switchWall.rect.y] == saveSprite[0]:
                    switchWall.on = saveSprite[1]
                    break
        self.gameManager.saveState.saveSprites = None

    for sprite in self.all_sprites:
      if sprite is not self.gameManager.Player:
         sprite.update()

    tempShadow = self.gameManager.shadow
    menu = False
    restart = False
    returnValue = None
    transparency = 255

    shader = Shader()
    #crt_shader =  Graphic_engine(self.surface, 1, False, True)
    t = 0
  
    while True:
      for event in pg.event.get():  # closes window

        if event.type == pg.QUIT:
          self.gameManager.saveState.save()
          pg.quit()
          exit()
        elif event.type == pg.KEYDOWN:
          if event.key == pg.K_ESCAPE and self.gameManager.Player.alive:
            menu = not (menu)
          if event.key == pg.K_r:
              self.gameManager.Player.alive = False
              restart = True
          self.gameManager.undoManager.update(event)
            
      pg.event.pump()
      if transparency == 0 and not (menu) and returnValue is None and self.gameManager.Player.alive:
        self.all_sprites.update()
        self.gameManager.checkCollisions()
        if self.gameManager.Player.rect.x > self.gameManager.screenWidth: ###### player changing rooms ###########
          returnValue = [1, 0]
        elif self.gameManager.Player.rect.x + self.gameManager.Player.rect.width < 0:
          returnValue = [-1, 0]
        elif self.gameManager.Player.rect.y > self.gameManager.screenHeight:
          returnValue = [0, 1]
        elif self.gameManager.Player.rect.y + self.gameManager.Player.rect.height < 0:
          returnValue = [0, -1]

      for door in self.gameManager.door_group: ############## check if player is going through a door ################
        if door.open(self.gameManager):
          self.gameManager.Player.setPos(door.playerPos[0], door.playerPos[1])
          returnValue = door.returnIndex
          self.gameManager.sceneIndex = door.returnIndex
          return None
          
      if self.gameManager.devMode and self.grid.drawAllRect:
        i = 0
      for sprite in self.all_sprites: ################ draws each sprite #######
        if not (menu) and returnValue is None:
          sprite.animate()
        sprite.draw(self.screen)
        if self.gameManager.devMode and self.grid.drawAllRect and sprite is not (self.gameManager.inventoryImage) and sprite is not (self.gameManager.dialogueManager):
          color = [0,0,0]
          tempNum = i
          if tempNum >= 4:
            tempNum -= 4
            color[0] = 1
          if tempNum >= 2:
            tempNum -= 2
            color[1] = 1
          if tempNum >= 1:
            color[2] = 1
          pg.draw.rect(self.screen, (255*color[0], 255*color[1], 255*color[2]), sprite.rect, 3)
          if sprite in self.gameManager.guard_group:
            pg.draw.rect(self.screen, (255*color[0], 255*color[1], 255*color[2]), sprite.vision.rect, 3)
          i += 1
          if i > 7:
            i = 0

        

      self.screen.blit(self.lowerBound, (0, self.gameManager.screenHeight))
      self.screen.blit(self.upperBound, (self.gameManager.screenWidth, 0))

      if self.gameManager.devMode: ############# devMode ################
        self.grid.update()
        self.grid.draw(self.screen)

      self.screen.blit(self.surface, (0, 0))
      
      pg.draw.rect(
          self.surface, (0, 0, 0, transparency),
          [0, 0, self.gameManager.screenWidth, self.gameManager.screenHeight])

      if menu and returnValue is None:
        keys = pg.key.get_pressed()
        if self.gameManager.devMode and keys[pg.K_LCTRL] and keys[pg.K_s]:
            saveName = input("save under what name? \n>")
            if isinstance(saveName, (str)):
                self.gameManager.user = saveName
                self.gameManager.saveState.save()
                pg.quit()
                exit()
            else:
                print("name is not a string. input: " + saveName)
        if self.gameManager.devMode and keys[pg.K_k]:
            if keys[pg.K_1]:
              if not(self.gameManager.inventoryImage.searchInv("key1")):
                spr.Collectible((0,0), "key", "key1", self.gameManager).collected()
            if keys[pg.K_2]:
              if not(self.gameManager.inventoryImage.searchInv("key2")):
                spr.Collectible((0,0), "key", "key2", self.gameManager).collected()
            if keys[pg.K_3]:
              if not(self.gameManager.inventoryImage.searchInv("key3")):
                spr.Collectible((0,0), "key", "key3", self.gameManager).collected()
            if keys[pg.K_4]:
              if not(self.gameManager.inventoryImage.searchInv("key4")):
                spr.Collectible((0,0), "key", "key4", self.gameManager).collected()
            if keys[pg.K_5]:
              if not(self.gameManager.inventoryImage.searchInv("key5")):
                spr.Collectible((0,0), "key", "key5", self.gameManager).collected()
        if self.gameManager.devMode and keys[pg.K_c]:
            if keys[pg.K_1]:
              if not(self.gameManager.inventoryImage.searchInv("coin1")):
                spr.Collectible((0,0), "coin", "coin1", self.gameManager).collected()
            if keys[pg.K_2]:
              if not(self.gameManager.inventoryImage.searchInv("coin2")):
                spr.Collectible((0,0), "coin", "coin2", self.gameManager).collected()
            if keys[pg.K_3]:
              if not(self.gameManager.inventoryImage.searchInv("coin3")):
                spr.Collectible((0,0), "coin", "coin3", self.gameManager).collected()
            if keys[pg.K_4]:
              if not(self.gameManager.inventoryImage.searchInv("coin4")):
                spr.Collectible((0,0), "coin", "coin4", self.gameManager).collected()
            if keys[pg.K_5]:
              if not(self.gameManager.inventoryImage.searchInv("coin5")):
                spr.Collectible((0,0), "coin", "coin5", self.gameManager).collected()
        if self.gameManager.devMode and keys[pg.K_m]:
            if keys[pg.K_1]:
              if not(self.gameManager.inventoryImage.searchInv("map1")):
                spr.Collectible((0,0), "map", "map1", self.gameManager).collected()
            if keys[pg.K_2]:
              if not(self.gameManager.inventoryImage.searchInv("map2")):
                spr.Collectible((0,0), "map", "map2", self.gameManager).collected()
            if keys[pg.K_3]:
              if not(self.gameManager.inventoryImage.searchInv("map3")):
                spr.Collectible((0,0), "map", "map3", self.gameManager).collected()
            if keys[pg.K_4]:
              if not(self.gameManager.inventoryImage.searchInv("map4")):
                spr.Collectible((0,0), "map", "map4", self.gameManager).collected()
            if keys[pg.K_5]:
              if not(self.gameManager.inventoryImage.searchInv("map5")):
                spr.Collectible((0,0), "map", "map5", self.gameManager).collected()
        if self.gameManager.devMode and keys[pg.K_t]:
            while True:
                try:
                    scene = input("What scene? (1, 2, 3, ...) \n")
                    if not(str(scene) == "esc"):
                        partX = input("What grid? (x) \n")
                        partY = input("What grid? (y) \n")
                        self.gameManager.clearLevel()
                        self.gameManager.sceneIndex = [0, [0,0]]
                        self.gameManager.sceneIndex[0] = int(scene)
                        self.gameManager.sceneIndex[1][0] = int(partX)
                        self.gameManager.sceneIndex[1][1] = int(partY)
                        return None
                    break
                except Exception as e:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(e).__name__, e.args)
                    print(message)
        self.screen.blit(self.surface, (0, 0))
        pg.draw.rect(self.surface, (0, 0, 0, 100), [
            0, 0, self.gameManager.screenWidth, self.gameManager.screenHeight
        ])
        self.menuText.draw(self.screen)
        self.exitButton.animate() 
        self.exitButton.draw(self.screen)
        if self.exitButton.isClick():
          self.gameManager.saveState.save()
          pg.quit()
          exit()


      if not (self.gameManager.Player.alive): ########### if player dies ###############
        keys = pg.key.get_pressed()
        if keys[pg.K_z]:
          self.gameManager.Player.alive = True
        if keys[pg.K_r] or restart:
            restart = False
            if not(self.gameManager.shadow):
                self.gameManager.Player.alive = True
                if self.gameManager.cage is not None:
                    self.gameManager.Player.setPos(self.gameManager.cage.pos[0], self.gameManager.cage.pos[1])
                else:
                    self.gameManager.Player.setPos(0, 0)
                self.gameManager.clearLevel()
                return None
            else:
              self.gameManager.Player.alive = True
              self.gameManager.clearLevel()
              return "reset"
        self.screen.blit(self.surface, (0, 0))
        pg.draw.rect(self.surface, (0, 0, 0, 100), [
            0, 0, self.gameManager.screenWidth, self.gameManager.screenHeight
        ])
        self.deadText.draw(self.screen)
        
      if tempShadow != self.gameManager.shadow: ############### switchVoid ###########
        return "shadow"

      t += 1
      update_shader(shader, self.screen, t)
      #crt_shader()

      pg.display.flip()

      if returnValue is None and transparency > 0:
        transparency -= 10
        if transparency < 0:
          transparency = 0
      elif returnValue is not (None) and transparency < 255:
        transparency += 10
        if transparency > 255:
          transparency = 255
      elif returnValue is not (None) and transparency == 255:
        self.gameManager.clearLevel()
        if returnValue == [0, -1]:
          self.gameManager.Player.setPos(None, (self.gameManager.Player.rect.center[1] / self.gameManager.tileSize[1] - .5 + self.gameManager.screenHeight / self.gameManager.tileSize[1]))
        elif returnValue == [1, 0]:
          self.gameManager.Player.setPos((self.gameManager.Player.rect.center[0] / self.gameManager.tileSize[0] - .5 - self.gameManager.screenWidth / self.gameManager.tileSize[0]), None)
        elif returnValue == [0, 1]:
          self.gameManager.Player.setPos(None, (self.gameManager.Player.rect.center[1] / self.gameManager.tileSize[1] - .5 - self.gameManager.screenHeight / self.gameManager.tileSize[1]))
        elif returnValue == [-1, 0]:
          self.gameManager.Player.setPos((self.gameManager.Player.rect.center[0] / self.gameManager.tileSize[0] - .5 + self.gameManager.screenWidth / self.gameManager.tileSize[0]), None)
        return returnValue

      self.clock.tick(self.gameManager.FPS)


def gameLoop(gameManager, scenes, start=[0,0]):
  gameManager.scenes.clear()
  gameManager.scenes = scenes
  tempArray = start.copy()

  ################ void #################
  all_sprites = pg.sprite.Group()
  background = spr.Background("sprites/BGs/blackBG.png", gameManager)
  kill_shadow = (
      spr.killShadow((0, 0, gameManager.screenWidth // gameManager.tileSize[0],
                     gameManager.screenHeight // gameManager.tileSize[1]),
                     gameManager))

  all_sprites.add(background, kill_shadow, gameManager.Player)

  scene_void = scene(gameManager, all_sprites)

  ################# voidEnd #################
  all_sprites = pg.sprite.Group()
  kill_shadow = (
      spr.killShadow((0, 0, gameManager.screenWidth // gameManager.tileSize[0],
                     gameManager.screenHeight // gameManager.tileSize[1]),
                     gameManager))

  if os.path.isfile("map" + str(gameManager.sceneIndex[0])):
    map_group = (spr.Collectible((11, 6), "map", "map" + str(gameManager.sceneIndex[0]), gameManager))
  else:
    map_group = (spr.text((11, 6), 6, "nothing here yet, come back when the game is complete", gameManager))

  all_sprites.add(background, kill_shadow, map_group, gameManager.Player)
  voidEnd = scene(gameManager, all_sprites)

  sceneParts = scenes
  shadowIndex = [0, 0]
  shadowIndex[0] = gameManager.sceneIndex[1][0]
  shadowIndex[1] = gameManager.sceneIndex[1][1]
  shadowTimer = 1

  while True:
    try:
      if gameManager.sceneIndex[1][0] < 0 or gameManager.sceneIndex[1][1] < 0:
          raise IndexError
      gameManager.shadow = False
      temp = sceneParts[gameManager.sceneIndex[1][0]][gameManager.sceneIndex[1][1]].main()
      if temp is None:
        return None
      try:
        gameManager.sceneIndex[1][1] += temp[1]
        gameManager.sceneIndex[1][0] += temp[0]
        shadowIndex[1] = gameManager.sceneIndex[1][1]
        shadowIndex[0] = gameManager.sceneIndex[1][0]
        gameManager.shadow = False
      except TypeError:
        if temp == "shadow":
            gameManager.shadow = True
        raise IndexError
    except IndexError:
      gameManager.sceneIndex[1][0] = -1
      gameManager.sceneIndex[1][1] = -1
      if shadowTimer % 7 == 0:
        gameManager.shadow = True
        temp = voidEnd.main()
      else:
        gameManager.shadow = True
        temp = scene_void.main()
      if temp == "reset":
        gameManager.shadow = False
        gameManager.sceneIndex[1][0] = tempArray[0]
        gameManager.sceneIndex[1][1] = tempArray[1]
        shadowIndex[1] = gameManager.sceneIndex[1][1]
        shadowIndex[0] = gameManager.sceneIndex[1][0]
        if sceneParts[tempArray[0]][tempArray[1]].cage is not None:
            gameManager.Player.setPos(sceneParts[tempArray[0]][tempArray[1]].cage.pos[0], sceneParts[tempArray[0]][tempArray[1]].cage.pos[1])
        else:
            gameManager.Player.setPos(0, 0)
        gameManager.clearLevel()
      else:
          if temp == "shadow":
            try:
              switch = False
              for shadowRect in sceneParts[shadowIndex[0]][shadowIndex[1]].shadowSpawn:
                if shadowRect.colliderect(gameManager.Player.rect):
                  gameManager.Player.shadow = False
                  gameManager.Player.alive = True
                  gameManager.sceneIndex[1][0] = shadowIndex[0]
                  gameManager.sceneIndex[1][1] = shadowIndex[1]
                  gameManager.shadow = False
                  switch = True
                  break
              if not(switch):
                gameManager.shadow = True
                gameManager.Player.alive = False
            except IndexError:
              gameManager.shadow = True
              gameManager.Player.alive = False
          else:
            if temp is None:
              return None
            shadowIndex[1] += temp[1]
            shadowIndex[0] += temp[0]
            shadowTimer += 1
            gameManager.shadow = True
