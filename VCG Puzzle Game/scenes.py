from sys import exit
from PIL import Image
import pygame as pg
import sprites as spr

grid = False

class scene:

  def __init__(self, gameManager, all_sprites, playerPos=(0,0), blank=False, *groups):
    pg.init()

    if grid:
      self.grid = spr.Grid(gameManager)

    self.blank = blank

    self.playerPos = playerPos

    self.gameManager = gameManager

    self.shadowSpawn = []

    for sprite in all_sprites:
      sprite.addSelf(self.gameManager)

    for killShadow in self.gameManager.kill_shadow:
      self.shadowSpawn.append(killShadow.rect)

    self.gameManager.clearLevel()

    self.screen = gameManager.screen
    self.surface = pg.Surface(
        (gameManager.screenWidth, gameManager.screenHeight), pg.SRCALPHA)
    self.clock = pg.time.Clock()

    gameManager.Player.alive = True

    font = pg.font.Font('freesansbold.ttf', int(gameManager.tileSize[1]))
    pausedText = font.render("Paused", True, (0, 0, 0))
    font = pg.font.Font('freesansbold.ttf', int(gameManager.tileSize[1] * 3 / 4))
    restartText = font.render("Press r to restart", True, (0, 0, 0))

    self.menuText = pg.sprite.Group(
        spr.Sprite(pausedText, (gameManager.screenWidth // 2,
                   gameManager.screenHeight // 2), self.gameManager,
                   False, *groups),
        spr.Sprite(
            restartText,
            (gameManager.screenWidth // 2,
            gameManager.screenHeight // 2 + int(gameManager.tileSize[1])),
            self.gameManager,
            False,
        ))

    self.all_sprites = pg.sprite.Group()

    for group in all_sprites:
      if group is not (None):
        self.all_sprites.add(pg.sprite.Group(group))

  def main(self):
    if self.blank:
      raise IndexError

    for sprite in self.all_sprites:
      sprite.addSelf(self.gameManager)

    menu = False
    returnValue = None
    transparency = 255
    while True:
      for event in pg.event.get():  # closes window

        if event.type == pg.QUIT:
          pg.quit()
          exit()
        elif event.type == pg.KEYDOWN:
          if event.key == pg.K_ESCAPE:
            menu = not (menu)

      pg.event.pump()
      if not (menu) and returnValue is None:
        self.all_sprites.update()
        if self.gameManager.Player.rect.x > self.gameManager.screenWidth - self.gameManager.Player.rect.width:
          returnValue = [1, 0]
        elif self.gameManager.Player.rect.x < 0:
          returnValue = [-1, 0]
        elif self.gameManager.Player.rect.y > self.gameManager.screenHeight - self.gameManager.Player.rect.height:
          returnValue = [0, 1]
        elif self.gameManager.Player.rect.y < 0:
          returnValue = [0, -1]
        self.gameManager.checkCollisions()
      for door in self.gameManager.door_group:
        if door.open(self.gameManager):
          self.gameManager.Player.setPos(door.playerPos[0], door.playerPos[1])
          returnValue = door.returnIndex
          self.gameManager.sceneIndex = door.returnIndex
          return None
      for sprite in self.all_sprites:
        if not (menu) and returnValue is None:
          sprite.animate()
        sprite.draw(self.screen)

      if grid:
        self.grid.draw(self.screen)

      self.screen.blit(self.surface, (0, 0))
      pg.draw.rect(
          self.surface, (0, 0, 0, transparency),
          [0, 0, self.gameManager.screenWidth, self.gameManager.screenHeight])

      if menu and returnValue is None:
        keys = pg.key.get_pressed()
        if keys[pg.K_r]:
          self.gameManager.Player.alive = False
        if keys[pg.K_g]:
            scene = input("What scene? (1, 2, 3, ...) \n")
            partX = input("What grid? (x) \n")
            partY = input("What grid? (y) \n")

            self.gameManager.clearLevel()
            self.gameManager.sceneIndex[0] = int(scene)
            self.gameManager.sceneIndex[1][0] = int(partX)
            self.gameManager.sceneIndex[1][1] = int(partY)
            return None
        self.screen.blit(self.surface, (0, 0))
        pg.draw.rect(self.surface, (0, 0, 0, 100), [
            0, 0, self.gameManager.screenWidth, self.gameManager.screenHeight
        ])
        self.menuText.draw(self.screen)

      if not (self.gameManager.Player.alive):
        self.gameManager.clearLevel()
        for collectible in self.gameManager.inventory:
          self.gameManager.removeCollect(collectible.name)
        self.gameManager.Player.alive = True
        self.gameManager.Player.setPos(self.playerPos[0], self.playerPos[1])
        return self.gameManager.sceneIndex

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
          self.gameManager.Player.setPos(None, (self.gameManager.screenHeight / self.gameManager.tileSize[1]) - 1)
        elif returnValue == [1, 0]:
          self.gameManager.Player.setPos(0, None)
        elif returnValue == [0, 1]:
          self.gameManager.Player.setPos(None, 0)
        elif returnValue == [-1, 0]:
          self.gameManager.Player.setPos((self.gameManager.screenWidth / self.gameManager.tileSize[0]) - 1, None)
        return returnValue

      pg.display.flip()

      self.clock.tick(self.gameManager.FPS)



def gameLoop(gameManager, scenes, start=[0,0]):
  tempArray = start.copy()
  #gameManager.sceneIndex[1][0] = tempArray[0]
  #gameManager.sceneIndex[1][1] = tempArray[1]

  ################ void #################
  all_sprites = pg.sprite.Group()
  background = spr.Background("sprites/BGs/blackBG.png", gameManager)
  kill_shadow = pg.sprite.Group(
      spr.killShadow((0, 0, gameManager.screenWidth // gameManager.tileSize[0],
                     gameManager.screenHeight // gameManager.tileSize[1]),
                     gameManager))

  all_sprites.add(background, kill_shadow, gameManager.Player)

  if not(gameManager.sceneIndex == 5):
    font = pg.font.Font('freesansbold.ttf', int(gameManager.tileSize[1]))
    WIPFont1 = font.render("Work in progress, ignore this place", True,
                           (255, 255, 255))
    WIPFont2 = font.render("press shift to return", True, (255, 255, 255))
    WIPText = pg.sprite.Group(
        spr.Sprite(WIPFont1, (gameManager.screenWidth // 2,
                   gameManager.screenHeight // 2), gameManager, False),
        spr.Sprite(WIPFont2, (gameManager.screenWidth // 2,
                   gameManager.screenHeight // 2 + int(gameManager.tileSize[1])), gameManager, False))
    all_sprites.add(WIPText)

  scene_void = scene(gameManager, all_sprites)

  ################# voidEnd #################
  all_sprites = pg.sprite.Group()
  kill_shadow = pg.sprite.Group(
      spr.killShadow((0, 0, gameManager.screenWidth // gameManager.tileSize[0],
                     gameManager.screenHeight // gameManager.tileSize[1]),
                     gameManager))


  all_sprites.add(background, kill_shadow)
  if gameManager.sceneIndex == 5:
    mapImage = Image.open(
      "sprites/Maps/map5.png")
    mapImage.thumbnail((gameManager.tileSize[0] * 3, gameManager.tileSize[1] * 3))
    mapImage.save("sprites/Maps/NMap5.png")
    map = spr.Sprite("sprites/Maps/NMap5.png", (gameManager.screenWidth // 2,
    gameManager.screenHeight // 2), gameManager, False)
    all_sprites.add(map)
  all_sprites.add(gameManager.Player)
  voidEnd = scene(gameManager, all_sprites)

  sceneParts = scenes
  shadowIndex = [0, 0]
  shadowIndex[0] = start[0]
  shadowIndex[1] = start[1]
  shadowTimer = 1

  while True:
    try:
      if gameManager.sceneIndex[1][0] < 0 or gameManager.sceneIndex[1][1] < 0:
          raise IndexError
      temp = sceneParts[gameManager.sceneIndex[1][0]][gameManager.sceneIndex[1][1]].main()
      try:
        gameManager.sceneIndex[1][1] += temp[1]
        gameManager.sceneIndex[1][0] += temp[0]
        shadowIndex[1] = gameManager.sceneIndex[1][1]
        shadowIndex[0] = gameManager.sceneIndex[1][0]
      except TypeError:
        return None
    except IndexError:
      if shadowTimer % 10 == 0:
        temp = voidEnd.main()
      else:
        temp = scene_void.main()
      try:
        shadowIndex[0] += temp[0]
        shadowIndex[1] += temp[1]
        shadowTimer += 1
      except TypeError:
        try:
          for shadowRect in sceneParts[shadowIndex[0]][shadowIndex[1]].shadowSpawn:
            if shadowRect.colliderect(gameManager.Player.rect):
              gameManager.sceneIndex[1][0] = shadowIndex[0]
              gameManager.sceneIndex[1][1] = shadowIndex[1]
              break
        except:
          gameManager.sceneIndex[1][0] = tempArray[0]
          gameManager.sceneIndex[1][1] = tempArray[1]
          tempPos = sceneParts[gameManager.sceneIndex[1][0]][gameManager.sceneIndex[1][1]].playerPos
          gameManager.Player.setPos(tempPos[0], tempPos[1])
