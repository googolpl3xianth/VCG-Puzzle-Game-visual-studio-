from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):
  pg.display.set_caption('scene_3')
  ##################### a ########################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/edge.png", gameManager)

  wall_group = pg.sprite.Group(spr.Wall((0, 11), False, 22, True, gameManager),
                               spr.Wall((0, 0), False, 22, True, gameManager),
                               spr.Wall((0, 0), True, 8, True, gameManager),
                               spr.Wall((0, 10), True, 2, True, gameManager),
                               spr.Wall((21, 0), True, 6, True, gameManager),
                               spr.Wall((21, 6), False, 1, True, gameManager))
  door_group = pg.sprite.Group(spr.Door((0, 8), "E", (2, [1, 0]), "key2", gameManager))
  switchWall_group = pg.sprite.Group(
      spr.switchWall((5, 2), "green", True, gameManager),
      spr.switchWall((5, 4), "green", True, gameManager),
      spr.switchWall((5, 6), "green", True, gameManager),
      spr.switchWall((5, 8), "green", True, gameManager),
      spr.switchWall((5, 10), "green", True, gameManager),
      spr.switchWall((6, 1), "green", False, gameManager),
      spr.switchWall((6, 3), "green", False, gameManager),
      spr.switchWall((6, 5), "green", False, gameManager),
      spr.switchWall((6, 7), "green", False, gameManager),
      spr.switchWall((6, 9), "green", False, gameManager),
      spr.switchWall((7, 2), "green", True, gameManager),
      spr.switchWall((7, 4), "green", True, gameManager),
      spr.switchWall((7, 6), "green", True, gameManager),
      spr.switchWall((7, 8), "green", True, gameManager),
      spr.switchWall((7, 10), "green", True, gameManager),
      spr.switchWall((8, 1), "green", False, gameManager),
      spr.switchWall((8, 2), "green", False, gameManager),
      spr.switchWall((8, 3), "green", False, gameManager),
      spr.switchWall((8, 4), "green", False, gameManager),
      spr.switchWall((8, 5), "green", False, gameManager),
      spr.switchWall((8, 6), "green", False, gameManager),
      spr.switchWall((8, 7), "green", False, gameManager),
      spr.switchWall((8, 8), "green", False, gameManager),
      spr.switchWall((8, 9), "green", False, gameManager),
      spr.switchWall((8, 10), "green", False, gameManager))
  switch_group = pg.sprite.Group(
      spr.Switch((5, 3), "green", switchWall_group, gameManager),
      spr.Switch((5, 1), "green", switchWall_group, gameManager),
      spr.Switch((5, 5), "green", switchWall_group, gameManager),
      spr.Switch((5, 7), "green", switchWall_group, gameManager),
      spr.Switch((5, 9), "green", switchWall_group, gameManager),
      spr.Switch((6, 2), "green", switchWall_group, gameManager),
      spr.Switch((6, 4), "green", switchWall_group, gameManager),
      spr.Switch((6, 6), "green", switchWall_group, gameManager),
      spr.Switch((6, 8), "green", switchWall_group, gameManager),
      spr.Switch((6, 10), "green", switchWall_group, gameManager),
      spr.Switch((7, 3), "green", switchWall_group, gameManager),
      spr.Switch((7, 1), "green", switchWall_group, gameManager),
      spr.Switch((7, 5), "green", switchWall_group, gameManager),
      spr.Switch((7, 7), "green", switchWall_group, gameManager),
      spr.Switch((7, 9), "green", switchWall_group, gameManager))
  if not (gameManager.searchInv("key3")):
    collectible_group = pg.sprite.Group(
        spr.Collectable((10, 9), "key", "key3", gameManager))
  else:
    collectible_group = pg.sprite.Group()

  all_sprites.add(background, wall_group, switchWall_group, switch_group,
                  collectible_group, gameManager.Player, door_group)

  scene_3_a = scn.scene(gameManager, all_sprites, (1,8))

  ######################### b #######################
  all_sprites = pg.sprite.Group()
  wall_group = pg.sprite.Group(spr.Wall((1, 7), True, 2, True, gameManager),
                               spr.Wall((1, 9), False, 7, True, gameManager),
                               spr.Wall((9, 9), False, 12, True, gameManager),
                               spr.Wall((21, 9), True, 2, True, gameManager),
                               spr.Wall((0, 6), False, 22, True, gameManager),
                               spr.Wall((0, 11), False, 22, True, gameManager))
  door_group = pg.sprite.Group(spr.Door((21, 7), "W", (4, [0, 1]), "key3", gameManager))

  GSwitchWall_group = pg.sprite.Group(
      spr.switchWall((9, 7), "green", True, gameManager),
      spr.switchWall((9, 8), "green", True, gameManager),
      spr.switchWall((7, 10), "green", False, gameManager),
      spr.switchWall((10, 10), "green", False, gameManager))
  GSwitch_group = pg.sprite.Group(
      spr.Switch((8, 10), "green", GSwitchWall_group, gameManager),
      spr.Switch((9, 10), "green", GSwitchWall_group, gameManager))
  BSwitchWall_group = pg.sprite.Group(
      spr.switchWall((8, 8), "blue", False, gameManager))
  BSwitch_group = pg.sprite.Group(
      spr.Switch((8, 9), "blue", BSwitchWall_group, gameManager))

  kill_shadow = pg.sprite.Group(
      spr.killShadow(
          (0, 0, gameManager.screenWidth / gameManager.tileSize[0], 6),
          gameManager))
  all_sprites.add(background, wall_group, GSwitchWall_group, BSwitchWall_group,
                  GSwitch_group, BSwitch_group, kill_shadow,
                  gameManager.Player, door_group)

  scene_3_b = scn.scene(gameManager, all_sprites, (0, 10))

  sceneParts = [[scene_3_a], [scene_3_b]]

  return scn.gameLoop(gameManager, sceneParts, [0, 0])
