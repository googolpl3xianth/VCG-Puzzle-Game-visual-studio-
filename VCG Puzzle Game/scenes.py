from http.client import NETWORK_AUTHENTICATION_REQUIRED
from sys import exit
from PIL import Image
import pygame as pg
import sprites as spr

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
        self.surface = pg.Surface(
            (gameManager.screenWidth, gameManager.screenHeight), pg.SRCALPHA)
        self.clock = pg.time.Clock()

        gameManager.Player.alive = True

        font = pg.font.Font('freesansbold.ttf', int(gameManager.tileSize[1]))
        pausedText = font.render("Paused", True, (0, 0, 0))
        
        font = pg.font.Font('freesansbold.ttf', int(gameManager.tileSize[1]))
        deadText = font.render("You Died", True, (255, 0, 0))
        font = pg.font.Font('freesansbold.ttf', int(gameManager.tileSize[1] * 3 / 4))
        returnText = font.render("Press r to restart", True, (255, 0, 0))
        

        self.menuText = pg.sprite.Group(
            spr.Sprite(pausedText, (gameManager.screenWidth // 2,
                       gameManager.screenHeight // 2), self.gameManager,
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

        self.all_sprites = pg.sprite.Group()

        for group in all_sprites:
          if group is not (None):
            self.all_sprites.add(pg.sprite.Group(group))
        self.all_sprites.add(pg.sprite.Group(gameManager.inventoryImage))

  def main(self):
    
    if self.blank:
      raise IndexError
  
    self.gameManager.clearLevel()

    for sprite in self.all_sprites:
      sprite.addSelf(self.gameManager)

    tempShadow = self.gameManager.shadow
    menu = False
    restart = False
    returnValue = None
    transparency = 255
    while True:
      for event in pg.event.get():  # closes window

        if event.type == pg.QUIT:
          pg.quit()
          exit()
        elif event.type == pg.KEYDOWN:
          if event.key == pg.K_ESCAPE and self.gameManager.Player.alive:
            menu = not (menu)
          if event.key == pg.K_r:
              self.gameManager.Player.alive = False
              restart = True
            
      pg.event.pump()
      if transparency == 0 and not (menu) and returnValue is None and self.gameManager.Player.alive:
        self.all_sprites.update()
        if self.gameManager.Player.rect.x > self.gameManager.screenWidth - self.gameManager.Player.rect.width: ###### player changing rooms ###########
          returnValue = [1, 0]
        elif self.gameManager.Player.rect.x + self.gameManager.Player.rect.width < 0:
          returnValue = [-1, 0]
        elif self.gameManager.Player.rect.y > self.gameManager.screenHeight - self.gameManager.Player.rect.height:
          returnValue = [0, 1]
        elif self.gameManager.Player.rect.y + self.gameManager.Player.rect.height < 0:
          returnValue = [0, -1]
        self.gameManager.checkCollisions()
      for door in self.gameManager.door_group: ############## check if player is going through a door ################
        if door.open(self.gameManager):
          self.gameManager.Player.setPos(door.playerPos[0], door.playerPos[1])
          returnValue = door.returnIndex
          self.gameManager.sceneIndex = door.returnIndex
          return None
      for sprite in self.all_sprites: ################ draws each sprite #######
        if not (menu) and returnValue is None:
          sprite.animate()
        sprite.draw(self.screen)

      if self.gameManager.devMode: ############# devMode ################
        self.grid.update()
        self.grid.draw(self.screen)

      self.screen.blit(self.surface, (0, 0))
      pg.draw.rect(
          self.surface, (0, 0, 0, transparency),
          [0, 0, self.gameManager.screenWidth, self.gameManager.screenHeight])

      if menu and returnValue is None:
        keys = pg.key.get_pressed()
        if keys[pg.K_t] and self.gameManager.devMode:
            while True:
                try:
                    scene = input("What scene? (1, 2, 3, ...) \n")
                    partX = input("What grid? (x) \n")
                    partY = input("What grid? (y) \n")

                    self.gameManager.clearLevel()
                    self.gameManager.sceneIndex[0] = int(scene)
                    self.gameManager.sceneIndex[1][0] = int(partX)
                    self.gameManager.sceneIndex[1][1] = int(partY)
                    return None
                except:
                  pass
            return None
        self.screen.blit(self.surface, (0, 0))
        pg.draw.rect(self.surface, (0, 0, 0, 100), [
            0, 0, self.gameManager.screenWidth, self.gameManager.screenHeight
        ])
        self.menuText.draw(self.screen)

      if not (self.gameManager.Player.alive): ########### if player dies ###############
        keys = pg.key.get_pressed()
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

      pg.display.flip()

      self.clock.tick(self.gameManager.FPS)



def gameLoop(gameManager, scenes, start=[0,0]):
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


  all_sprites.add(background, kill_shadow)
  if gameManager.sceneIndex[0] == 5:
    mapImage = Image.open(
      "sprites/Maps/map5.png")
    mapImage.thumbnail((gameManager.tileSize[0] * 8, gameManager.tileSize[1] * 8))
    mapImage.save("sprites/Maps/NMap5.png")
    map = spr.Sprite(pg.image.load("sprites/Maps/NMap5.png"), (gameManager.screenWidth // 2,
    gameManager.screenHeight // 2), gameManager, False)
    all_sprites.add(map)
  elif gameManager.sceneIndex[0] == 4:
    mapImage = Image.open(
      "sprites/Maps/map4.png")
    mapImage.thumbnail((gameManager.tileSize[0] * 8, gameManager.tileSize[1] * 8))
    mapImage.save("sprites/Maps/NMap4.png")
    map = spr.Sprite(pg.image.load("sprites/Maps/NMap4.png"), (gameManager.screenWidth // 2,
    gameManager.screenHeight // 2), gameManager, False)
    all_sprites.add(map)
  all_sprites.add(gameManager.Player)
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
      if shadowTimer % 10 == 0:
        temp = voidEnd.main()
      else:
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
