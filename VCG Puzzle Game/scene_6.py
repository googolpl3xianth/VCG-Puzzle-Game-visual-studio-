from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene
  pg.display.set_caption('???')
  ##################### a ########################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/blackBG.png", gameManager)

  door_group = (spr.Door((0, 8), "E", (5, [1, 2]), "key5", gameManager))

  text_group = (
      spr.text((4, 7), 12, "there are 5 coins to collect",
               gameManager, 1, (0, 255, 0)),
      spr.text((4, 5), 12, "scattered at the edges of each past scene", gameManager, 1, (0, 255, 0)))

  kill_shadow = (
      spr.killShadow((0, 0, gameManager.screenWidth / gameManager.tileSize[0],
                     gameManager.screenHeight / gameManager.tileSize[1]),
                     gameManager))

  all_sprites.add(background, kill_shadow, door_group, gameManager.Player,
                  text_group)

  scene_5 = scn.scene(gameManager, all_sprites)

  sceneParts = [[scene_5]]

  return scn.gameLoop(gameManager, sceneParts, [0, 0])
