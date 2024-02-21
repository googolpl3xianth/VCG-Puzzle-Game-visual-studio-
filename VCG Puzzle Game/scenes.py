from sys import exit
import pygame as pg
import sprites as spr


class scene:

  def __init__(self, gameManager, all_sprites, *groups):
    pg.init()
    self.gameManager = gameManager

    self.shadowSpawn = [[None, None]]

    self.screen = pg.display.set_mode(
        (gameManager.screenWidth, gameManager.screenHeight))
    self.surface = pg.Surface(
        (gameManager.screenWidth, gameManager.screenHeight), pg.SRCALPHA)
    self.clock = pg.time.Clock()

    gameManager.Player.alive = True

    self.all_sprites = pg.sprite.Group()

    for group in all_sprites:
      if group is not (None):
        self.all_sprites.add(pg.sprite.Group(group))

  def main(self):  
    for sprite in self.all_sprites:
      sprite.addSelf(self.gameManager)

    for killShadow in self.gameManager.kill_shadow:
      temp = [killShadow.rect]
      self.shadowSpawn.append(temp)

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
          returnValue = door.returnIndex
      for sprite in self.all_sprites:
        if not (menu) and returnValue is None:
          sprite.animate()
        sprite.draw(self.screen)

      self.screen.blit(self.surface, (0, 0))
      pg.draw.rect(
          self.surface, (0, 0, 0, transparency),
          [0, 0, self.gameManager.screenWidth, self.gameManager.screenHeight])

      if menu and returnValue is None:
        keys = pg.key.get_pressed()
        if keys[pg.K_r]:
          self.gameManager.Player.alive = False
        if keys[pg.K_g]:
          level = input("What level?\n")
          self.gameManager.clearLevel()
          return int(level)
        self.screen.blit(self.surface, (0, 0))
        pg.draw.rect(self.surface, (0, 0, 0, 100), [
            0, 0, self.gameManager.screenWidth, self.gameManager.screenHeight
        ])

      if not (self.gameManager.Player.alive):
        self.gameManager.clearLevel()
        self.gameManager.Player.alive = True
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
          pass
          self.gameManager.Player.rect.y = self.gameManager.screenHeight - (self.gameManager.Player.rect.height + .5 * self.gameManager.tileSize - self.gameManager.Player.rect.height / 2)
        elif returnValue == [1, 0]:
          self.gameManager.Player.rect.x = .5 * self.gameManager.tileSize - self.gameManager.Player.rect.width / 2
        elif returnValue == [0, 1]:
          self.gameManager.Player.rect.y = .5 * self.gameManager.tileSize - self.gameManager.Player.rect.height / 2
        elif returnValue == [-1, 0]:
          pass
          self.gameManager.Player.rect.x = self.gameManager.screenWidth - (self.gameManager.Player.rect.width + .5 * self.gameManager.tileSize - self.gameManager.Player.rect.width / 2)
        return returnValue

      pg.display.flip()

      self.clock.tick(self.gameManager.FPS)


def gameLoop(gameManager, scenes):
  ################ void #################
  all_sprites = pg.sprite.Group()
  background = spr.Background("sprites/BGs/NewBlackBG.png", gameManager)
  kill_shadow = pg.sprite.Group(
      spr.killShadow(0, 0, gameManager.screenWidth // gameManager.tileSize,
                     gameManager.screenHeight // gameManager.tileSize,
                     gameManager))
  all_sprites.add(background, kill_shadow, gameManager.Player)
  scene_void = scene(gameManager, all_sprites)

  sceneParts = scenes
  sceneIndex = [0, 0]
  shadowIndex = [0, 0]
  while True:
    try:
      temp = sceneParts[sceneIndex[0]][sceneIndex[1]].main()
      try:
        sceneIndex[0] += temp[0]
        sceneIndex[1] += temp[1]
        shadowIndex[0] = sceneIndex[0]
        shadowIndex[1] = sceneIndex[1]

        if sceneIndex[0] < 0 or sceneIndex[1] < 0:
          raise IndexError
      except TypeError:
        if isinstance(temp, int):
          return temp
        else:
          print("Error, temp is: " + str(temp))
    except IndexError:
      temp = scene_void.main()
      try:
        shadowIndex[0] += temp[0]
        shadowIndex[1] += temp[1]
      except TypeError:
        if isinstance(temp, int):
          #try:
          #  sceneParts[shadowIndex[0]][shadowIndex[1]]
          #  sceneIndex[0] = shadowIndex[0]
          #  sceneIndex[1] = shadowIndex[1]
          #except IndexError:
          #  return temp
          return temp
        else:
          print("Error, temp is: " + str(temp))
