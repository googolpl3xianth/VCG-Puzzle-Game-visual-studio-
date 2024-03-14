from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene
  pg.display.set_caption('???')
  ##################### a ########################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/blackBG.png", gameManager)

  door_group = pg.sprite.Group(spr.Door((0, 8), "E", (5, [1, 0]), "key5", gameManager))

  text_group = pg.sprite.Group(
      spr.text((4, 7), 12, "return to the beginning", gameManager, 1,
               (0, 255, 0)),
      spr.text((4, 5), 12, "there are 2 coins to collect in scene_1 and 2",
               gameManager, 1, (0, 255, 0)),
      spr.text((4, 3), 12, "press esc then g", gameManager, 1, (0, 255, 0)))

  kill_shadow = pg.sprite.Group(
      spr.killShadow((0, 0, gameManager.screenWidth / gameManager.tileSize[0],
                     gameManager.screenHeight / gameManager.tileSize[1]),
                     gameManager))

  all_sprites.add(background, kill_shadow, door_group, gameManager.Player,
                  text_group)

  scene_5 = scn.scene(gameManager, all_sprites, (1, 8))

  sceneParts = [[scene_5]]

  return scn.gameLoop(gameManager, sceneParts, [0, 0])
