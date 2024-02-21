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

  button = spr.Button("sprites/Buttons/NewButton.png",
                      gameManager.screenWidth / 2,
                      gameManager.screenHeight / 2,
                      gameManager, False)  # start button

  background = spr.Background("sprites/BGs/NewBG.png", gameManager)

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
      level = input("What level?\n")
      return int(level)

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
      return 1

    pg.display.flip()  # updates screen

    clock.tick(gameManager.FPS)  # frame rate
