import menu
import scene_1
import scene_2
import scene_3
import scene_4
import scene_5
import scene_6
import pygame as pg
import sprites as spr
import scenes as scn
import os
import sys

application_path = os.path.dirname(__file__)
os.chdir(application_path)

scenes = [menu, scene_1, scene_2, scene_3, scene_4, scene_5, scene_6]

FPS = 60
speed = 3.0

gameManager = spr.GameManager(FPS)
player = spr.Player((0, 0), gameManager)
player.setPos(2, 6)


def main():
  pg.init()
  while True:
    gameManager.clearLevel()
    scenes[gameManager.sceneIndex[0]].main(gameManager)


def void(gameManager):
  all_sprites = pg.sprite.Group()
  background = spr.Background("sprites/BGs/blackBG.png", gameManager, False)
  kill_shadow = (spr.killShadow((0, 0, gameManager.screenWidth / gameManager.tileSize[0], gameManager.screenHeight / gameManager.tileSize[1]), gameManager))
  all_sprites.add(background, kill_shadow, gameManager.Player)

  scene_void = scn.scene(gameManager, all_sprites)

  shadowIndex = [0, 0]

  while True:
    print(gameManager.sceneIndex)
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
