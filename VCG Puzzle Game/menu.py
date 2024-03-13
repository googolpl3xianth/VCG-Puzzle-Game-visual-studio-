from PIL import Image
from sys import exit
import pygame as pg
import sprites as spr


def main(gameManager):  # starting scene
  pg.init()
  pg.display.set_caption('menu')

  screen = pg.display.set_mode(
      (gameManager.screenWidth, gameManager.screenHeight))
  surface = pg.Surface((gameManager.screenWidth, gameManager.screenHeight),
                       pg.SRCALPHA)
  clock = pg.time.Clock()

  button = spr.Button("sprites/Buttons/startButton.png",
                      (gameManager.screenWidth / 2,
                      gameManager.screenHeight / 2),
                      gameManager, False)  # start button


  background = spr.Background("sprites/BGs/titleScreen.jpg", gameManager, False)

  all_sprites = pg.sprite.Group()
  all_sprites.add(background, button)

  menu = False
  run = True
  transparency = 255
  while True:
    for event in pg.event.get():  # closes window

      if event.type == pg.QUIT:
        pg.quit()
        exit()

      elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
          menu = not (menu)

    if (button.isClick()):  # checks if start button is clicked
      if not (menu):
        run = False  # tells main to add 1 to scene index

    for sprite in all_sprites:
      sprite.draw(screen)
    screen.blit(surface, (0, 0))
    pg.draw.rect(surface, (0, 0, 0, transparency),
                 [0, 0, gameManager.screenWidth, gameManager.screenHeight])

    keys = pg.key.get_pressed()
    if keys[pg.K_g]:
        scene = input("What scene? (1, 2, 3, ...) \n")
        partX = input("What grid? (x) \n")
        partY = input("What grid? (y) \n")

        gameManager.clearLevel()
        gameManager.sceneIndex[0] = int(scene)
        gameManager.sceneIndex[1][0] = int(partX)
        gameManager.sceneIndex[1][1] = int(partY)
        return None

    if menu:
      keys = pg.key.get_pressed()
      if keys[pg.K_g]:
        level = input("What level?\n")
        return int(level)
      screen.blit(surface, (0, 0))
      pg.draw.rect(surface, (0, 0, 0, 100),
                   [0, 0, gameManager.screenWidth, gameManager.screenHeight])

    if run and transparency > 0:
      transparency -= 10
      if transparency < 0:
        transparency = 0
    elif not (run) and transparency < 255:
      transparency += 10
      if transparency > 255:
        transparency = 255
    elif not (run) and transparency == 255:
      gameManager.sceneIndex[0] = 1
      return None

    pg.display.flip()  # updates screen

    clock.tick(gameManager.FPS)  # frame rate
