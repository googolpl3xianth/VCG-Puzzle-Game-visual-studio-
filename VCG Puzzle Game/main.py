import menu
import scene_1
import scene_2
import scene_3
import scene_4
import scene_5
import showcase
import pygame as pg
import sprites as spr
import scenes as scn

scenes = [menu, scene_1, scene_2, scene_3, scene_4, scene_5, showcase]

WIDTH = 400
HEIGHT = 300
FPS = 60
tileSize = 25 # 50 * 50
speed = 3.0

gameManager = spr.GameManager(WIDTH, HEIGHT, FPS, tileSize)
player = spr.Player(0, 0, gameManager)


def runScene(scene):
  output = scene.main(
        gameManager
    )  # in main() of scene when you want to move scene, add a return int where int is the scene Index you want to go to after it ends

  return output


def main():
  pg.init()
  while True:
    gameManager.clearLevel()
    try:
      gameManager.sceneIndex = runScene(scenes[gameManager.sceneIndex])
    except IndexError or TypeError:
      gameManager.sceneIndex = void(gameManager)


def void(gameManager):
  all_sprites = pg.sprite.Group()
  background = spr.Background("sprites/BGs/NewBlackBG.png", gameManager)
  kill_shadow = pg.sprite.Group(spr.killShadow(0, 0, gameManager.screenWidth // gameManager.tileSize, gameManager.screenHeight // gameManager.tileSize, gameManager))
  all_sprites.add(background, kill_shadow, gameManager.Player)

  scene_void = scn.scene(gameManager, all_sprites)

  shadowIndex = [0, 0]

  while True:
    temp = scene_void.main()
    try:
      shadowIndex[0] += temp[0]
      shadowIndex[1] += temp[1]
    except TypeError:
      if isinstance(temp, int):
          return temp
      else:
        print("Error, temp is: " + str(temp))

if __name__ == "__main__":
  main()

# Controls:
# WASD movement
# Space to grab boxes and move them
# Shift to go into shadow mode and move through most objects
# Press ESC to pause
# Press R to restart while paused
# Press G while in menu or when paused then type in the scene index into the console to skip to it
