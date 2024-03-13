from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene
  pg.display.set_caption('scene_2')
  ##################### a ########################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/edge.png", gameManager)

  wall_group = pg.sprite.Group(spr.Wall((8, 7), False, 4, False, gameManager),
                               spr.Wall((11, 7), True, 5, False, gameManager),
                               spr.Wall((0, 11), False, 11, True, gameManager),
                               spr.Wall((12, 11), False, 10, True, gameManager),
                               spr.Wall((7, 2), True, 10, True, gameManager),
                               spr.Wall((0, 0), False, 22, True, gameManager),
                               spr.Wall((0, 0), True, 8, True, gameManager),
                               spr.Wall((0, 10), True, 2, True, gameManager))
  door_group = pg.sprite.Group(spr.Door((0, 8), "E", (1, [1, 0]), "key1", gameManager))
  switchWall_group = pg.sprite.Group(
      spr.switchWall((7, 1), "red", False, gameManager))
  switch_group = pg.sprite.Group(
      spr.Switch((6, 1), "red", switchWall_group, gameManager))

  if not (gameManager.searchInv("key2")):
    collectible_group = pg.sprite.Group(
        spr.Collectable((9, 9), "key", "key2", gameManager))
  else:
    collectible_group = pg.sprite.Group()
  all_sprites.add(background, wall_group, switchWall_group, switch_group,
                  collectible_group, gameManager.Player, door_group)

  scene_2_a = scn.scene(gameManager, all_sprites, (1, 8))

  ######################### b #######################
  all_sprites = pg.sprite.Group()
  wall_group = pg.sprite.Group(spr.Wall((3, 1), True, 2, True, gameManager),
                               spr.Wall((4, 2), False, 2, True, gameManager),
                               spr.Wall((7, 2), True, 2, True, gameManager),
                               spr.Wall((3, 4), False, 7, True, gameManager),
                               spr.Wall((7, 4), True, 6, True, gameManager),
                               spr.Wall((0, 11), False, 22, True, gameManager),
                               spr.Wall((0, 0), False, 22, True, gameManager),
                               spr.Wall((21, 0), True, 8, True, gameManager),
                               spr.Wall((21, 10), True, 2, True, gameManager))
  box_group = pg.sprite.Group(spr.Box((7, 10), False, gameManager))
  door_group = pg.sprite.Group(spr.Door((21, 8), "W", (3, [0, 0]), "key2", gameManager))

  if not (gameManager.searchInv("coin2")):
    collectible_group = pg.sprite.Group(
        spr.Collectable((6, 3), "coin", "coin2", gameManager))
  else:
    collectible_group = pg.sprite.Group()

  gSwitchWall_group = pg.sprite.Group(
      spr.switchWall((6, 1), "green", False, gameManager),
      spr.switchWall((6, 2), "green", True, gameManager))
  rSwitchWall_group = pg.sprite.Group(
      spr.switchWall((3, 3), "red", True, gameManager))
  switch_group = pg.sprite.Group(
      spr.Switch((5, 1), "green", gSwitchWall_group, gameManager),
      spr.Switch((5, 3), "red", rSwitchWall_group, gameManager))

  all_sprites.add(background, wall_group, gSwitchWall_group, rSwitchWall_group,
                  switch_group, collectible_group, box_group,
                  gameManager.Player, door_group)

  scene_2_b = scn.scene(gameManager, all_sprites, (0,8))

  ######################### c #######################
  all_sprites = pg.sprite.Group()
  wall_group = pg.sprite.Group(spr.Wall((0, 11), False, 22, True, gameManager),
                               spr.Wall((1, 0), False, 10, True, gameManager),
                               spr.Wall((12, 0), False, 10, True, gameManager),
                               spr.Wall((0, 0), True, 12, True, gameManager))

  all_sprites.add(
      background,
      wall_group,
      gameManager.Player,
  )

  scene_2_c = scn.scene(gameManager, all_sprites, (11, 0))

  ######################### d #######################
  all_sprites = pg.sprite.Group()
  wall_group = pg.sprite.Group(spr.Wall((0, 11), False, 22, True, gameManager),
                               spr.Wall((21, 0), True, 12, True, gameManager),
                               spr.Wall((0, 0), False, 12, True, gameManager))

  all_sprites.add(
      background,
      wall_group,
      gameManager.Player,
  )

  scene_2_d = scn.scene(gameManager, all_sprites, (0, 3))

  sceneParts = [[scene_2_a, scene_2_c], [scene_2_b, scene_2_d]]

  return scn.gameLoop(gameManager, sceneParts, [0, 0])
