import menu
import scene_1
import scene_2
import scene_3
import scene_4
import scene_5
import scene_6
import scene_7
import pygame as pg
import sprites as spr
import scenes as scn
import win32com.client
import os
from pathlib import Path

application_path = os.path.dirname(__file__)
os.chdir(application_path)
user = str(Path.home()) # path to where you want to put the .lnk
path = os.path.join(user, 'break.lnk')
target = str(application_path) + '\\dist\\break.exe'
icon = str(application_path) + '\\sprites\\Player\\Player.png'

shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = target
shortcut.IconLocation = icon
shortcut.WindowStyle = 7 # 7 - Minimized, 3 - Maximized, 1 - Normal
shortcut.save()

scenes = [menu, scene_1, scene_2, scene_3, scene_4, scene_5, scene_6, scene_7]

FPS = 60
speed = 3.0

gameManager = spr.GameManager(FPS)
player = spr.Player((0, 0), gameManager)
player.setPos(2, 6)


def main():
  pg.init()
  while True:
    gameManager.clearLevel()
    try:
      scenes[gameManager.sceneIndex[0]].main(gameManager)
    except Exception as e:
      template = "An exception otf type {0} occurred. Arguments:\n{1!r}"
      message = template.format(type(e).__name__, e.args)
      print(message)
      gameManager.saveState.save()
      pg.quit()
      exit()


def void(gameManager):
  all_sprites = pg.sprite.Group()
  background = spr.Background("sprites/BGs/blackBG.png", gameManager, False)
  kill_shadow = (spr.killShadow((0, 0, gameManager.screenWidth / gameManager.tileSize[0], gameManager.screenHeight / gameManager.tileSize[1]), gameManager))
  all_sprites.add(background, kill_shadow, gameManager.Player)

  scene_void = scn.scene(gameManager, all_sprites)
  shadowIndex = [0, 0]

  while True:
    temp = scene_void.main()
    try:
      shadowIndex[0] += temp[0]
      shadowIndex[1] += temp[1]
    except TypeError:
      return None


if __name__ == "__main__":
  main()

# Controls:
# WASD movement
# Hold SPACE to go into shadow mode and move through most objects
# Hold SHIFT to sprint
# Press ESC to pause
# Press R to restart while paused
# Press Z to undo

















# ***************** DEV ONLY ***************** #
# Press ctrl + s while paused to save to name
# Press ctrl + s while in menu to load name save
# Hold g to toggle grid
# Hold h to hide player
# Press t while in menu or when paused then type in the scene index into the console to skip to it

# rule 0: Once you enter the void, there is no return
# rule 1: As long as there is a physical object, you are anchored to the real world
# rule 2: A shadow that enters a shadow will become merged with it
# rule 3: A merged shadow in the void will ascend if there is void in the real world