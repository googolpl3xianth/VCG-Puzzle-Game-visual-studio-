from os import truncate
from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):
  pg.display.set_caption('scene_4')
  ##################### a ########################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/edge.png", gameManager)

  wall_group = pg.sprite.Group(spr.Wall((4, 1), True, 5, True, gameManager),
                               spr.Wall((4, 7), True, 4, True, gameManager),
                               spr.Wall((1, 6), False, 6, False, gameManager),
                               spr.Wall((8, 6), False, 14, False, gameManager),
                               spr.Wall((10, 1), True, 5, True, gameManager),
                               spr.Wall((10, 7), True, 4, True, gameManager),
                               spr.Wall((0, 11), False, 22, True, gameManager),
                               spr.Wall((0, 0), False, 5, True, gameManager),
                               spr.Wall((10, 0), False, 12, True, gameManager),
                               spr.Wall((0, 0), True, 8, True, gameManager),
                               spr.Wall((0, 10), True, 2, True, gameManager))
  door_group = pg.sprite.Group(spr.Door((0, 8), "E", (3, [1, 0]), "key3", gameManager))

  kill_shadow = pg.sprite.Group(spr.killShadow((7, 6, 1, 1), gameManager))

  if not (gameManager.searchInv("key4")):
    collectible_group = pg.sprite.Group(
        spr.Collectable((7, 2), "key", "key4", gameManager))
  else:
    collectible_group = pg.sprite.Group()

  all_sprites.add(background, wall_group, collectible_group, kill_shadow,
                  gameManager.Player, door_group)

  scene_4_a = scn.scene(gameManager, all_sprites, (1, 8))

  ######################### b #######################
  all_sprites = pg.sprite.Group()
  wall_group = pg.sprite.Group(spr.Wall((0, 6), False, 21, False, gameManager),
                               spr.Wall((1, 7), False, 20, True, gameManager),
                               spr.Wall((1, 9), False, 15, True, gameManager),
                               spr.Wall((0, 11), False, 22, True, gameManager),
                               spr.Wall((0, 0), False, 22, True, gameManager),
                               spr.Wall((21, 0), True, 8, True, gameManager),
                               spr.Wall((1, 10), True, 1, True, gameManager),
                               spr.Wall((21, 10), True, 2, True, gameManager))
  door_group = pg.sprite.Group(spr.Door((21, 8), "W", (5, [0, 0]), "key4", gameManager))
  gaurd = pg.sprite.Group(spr.Guard((2, 8), 15, 7, gameManager))
  box_group = pg.sprite.Group(spr.Box((1, 8), False, gameManager))

  all_sprites.add(background, wall_group, gaurd, box_group, gameManager.Player, door_group)

  scene_4_b = scn.scene(gameManager, all_sprites, (0, 9))

  ############# c #######################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/edge.png", gameManager)

  kill_shadow = pg.sprite.Group(
      spr.killShadow((0, 0, (gameManager.screenWidth / gameManager.tileSize[0]),
                      (gameManager.screenHeight // gameManager.tileSize[1]) - 5),
                     gameManager),
      spr.killShadow(
          (0, (gameManager.screenHeight // gameManager.tileSize[1]) - 5, 3, 5),
          gameManager),
      spr.killShadow(
          (0, (gameManager.screenHeight // gameManager.tileSize[1]) - 2, 1, 1),
          gameManager),
      spr.killShadow(
          (4, (gameManager.screenHeight // gameManager.tileSize[1]) - 2, 2, 1),
          gameManager),
      spr.killShadow(
          (3, (gameManager.screenHeight // gameManager.tileSize[1]) - 5, 3, 3),
          gameManager),
      spr.killShadow(
          (5, (gameManager.screenHeight // gameManager.tileSize[1]) - 4, 3, 2),
          gameManager),
      spr.killShadow(
          (7, (gameManager.screenHeight // gameManager.tileSize[1]) - 5, 5, 2),
          gameManager),
      spr.killShadow(
          (13, (gameManager.screenHeight // gameManager.tileSize[1]) - 5, 9, 5),
          gameManager),
      spr.killShadow(
          (12, (gameManager.screenHeight // gameManager.tileSize[1]) - 4, 4, 2),
          gameManager),
      spr.killShadow(
          (10, (gameManager.screenHeight // gameManager.tileSize[1]) - 1, 3, 1),
          gameManager),
      spr.killShadow(
          (10, (gameManager.screenHeight // gameManager.tileSize[1]) - 3, 1, 1),
          gameManager),
      spr.killShadow(
          (11, (gameManager.screenHeight // gameManager.tileSize[1]) - 2, 1, 1),
          gameManager),
      spr.killShadow(
          (13, (gameManager.screenHeight // gameManager.tileSize[1]) - 2, 3, 2),
          gameManager),
      spr.killShadow(
          (3, (gameManager.screenHeight // gameManager.tileSize[1]) - 1, 2, 1),
          gameManager))

  all_sprites.add(background, kill_shadow, gameManager.Player)

  scene_4_c = scn.scene(gameManager, all_sprites)

  blankScene = scn.scene(gameManager, pg.sprite.Group(), True)

  sceneParts = [[scene_4_c, scene_4_a], [blankScene, scene_4_b]]

  return scn.gameLoop(gameManager, sceneParts, [0, 1])
