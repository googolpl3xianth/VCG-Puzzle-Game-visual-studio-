from PIL import Image
from sys import exit
import pygame as pg
import sprites as spr
from shader import Shader, update_shader
import moderngl
import os.path


def main(gameManager):  # starting scene
  pg.init()
  pg.display.set_caption('menu')

  surface = pg.Surface((gameManager.screenWidth, gameManager.screenHeight),
                       pg.SRCALPHA)
  clock = pg.time.Clock()
  button = (spr.Button("sprites/Buttons/startButton.png",
                      (gameManager.screenWidth / 2,
                      gameManager.screenHeight / 2),
                      gameManager, False),
            spr.Button("sprites/Misc/dialogueBox.png", 
                       (gameManager.screenWidth / 2, 
                       gameManager.tileSize[1] * 3 + gameManager.screenHeight / 2), 
                       gameManager, False))  # start button
  background = spr.Background("sprites/BGs/titleScreen.jpg", gameManager, False)

  all_sprites = pg.sprite.Group()
  all_sprites.add(background, button)

  shader = Shader()
  t = 0

  run = True
  transparency = 255
  while True:
    for event in pg.event.get():  # closes window

      if event.type == pg.QUIT:
        pg.quit()
        exit()

    if (button[0].isClick()):  # checks if start button is clicked
        run = False
        gameManager.sceneIndex[0] = 1
    if (button[1].isClick()):  # checks if start button is clicked
        if gameManager.saveState.load():
            run = False

    for sprite in all_sprites:
      sprite.draw(gameManager.screen)
    gameManager.screen.blit(surface, (0, 0))
    pg.draw.rect(surface, (0, 0, 0, transparency),
                 [0, 0, gameManager.screenWidth, gameManager.screenHeight])

    keys = pg.key.get_pressed()
    if gameManager.devMode and keys[pg.K_LCTRL] and keys[pg.K_s]:
      saveName = input("saved under what name? \n>")
      if os.path.isfile('VCG Puzzle Game/saveFiles/' + saveName + '.dat'):
        gameManager.user = saveName
        gameManager.saveState.load()
        return None
      else:
          print("no saveFile under that name")
    if gameManager.devMode and keys[pg.K_LCTRL] and keys[pg.K_n]:
      username = input("what is your username \n>")
      if isinstance(username, (str)):
         gameManager.user = username
      else:
          print("name is not a string")
    if gameManager.devMode and keys[pg.K_t]:
        while True:
            try:
                scene = input("What scene? (1, 2, 3, ...) \n")
                partX = input("What grid? (x) \n")
                partY = input("What grid? (y) \n")

                gameManager.clearLevel()
                gameManager.sceneIndex[0] = int(scene)
                gameManager.sceneIndex[1][0] = int(partX)
                gameManager.sceneIndex[1][1] = int(partY)
                return None
            except:
              pass

    if run and transparency > 0:
      transparency -= 10
      if transparency < 0:
        transparency = 0
    elif not (run) and transparency < 255:
      transparency += 10
      if transparency > 255:
        transparency = 255
    elif not (run) and transparency == 255:
      return None

    update_shader(shader, gameManager.screen, t)

    pg.display.flip()  # updates screen

    clock.tick(gameManager.FPS)  # frame rate
