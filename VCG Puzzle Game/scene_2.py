from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene

  gameManager.Player.rect.x = (1 + .5) * gameManager.tileSize - gameManager.Player.rect.width / 2
  gameManager.Player.rect.y = (8 + .5) * gameManager.tileSize - gameManager.Player.rect.height / 2
  pg.display.set_caption('scene_2')
  ##################### a ########################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/NewBG.png", gameManager)

  wall_group = pg.sprite.Group(spr.Wall(8, 7, gameManager, False, 4, False),
                               spr.Wall(11, 7, gameManager, True, 5, False),
                               spr.Wall(0, 11, gameManager, False, 11, True),
                               spr.Wall(12, 11, gameManager, False, 4, True),
                               spr.Wall(7, 2, gameManager, True, 10, True),
                               spr.Wall(0, 0, gameManager, False, 16, True),
                               spr.Wall(0, 0, gameManager, True, 8, True),
                               spr.Wall(0, 10, gameManager, True, 2, True))
  door_group = pg.sprite.Group(spr.Door(0, 8, "E", 1, "No", gameManager))
  switchWall_group = pg.sprite.Group(spr.switchWall(7, 1, gameManager, "red", False))
  switch_group = pg.sprite.Group(spr.Switch(6, 1, gameManager, "red", switchWall_group))

  if not (gameManager.searchInv("key2")):
    collectible_group = pg.sprite.Group(spr.Collectable(9, 9, "key", "key2", gameManager))
  else:
    collectible_group = pg.sprite.Group()
  all_sprites.add(background, wall_group, switchWall_group, switch_group,
                  collectible_group, gameManager.Player, door_group)

  scene_2_a = scn.scene(gameManager, all_sprites)

  ######################### b #######################
  all_sprites = pg.sprite.Group()
  wall_group = pg.sprite.Group(spr.Wall(3, 1, gameManager, True, 2, True),
                               spr.Wall(4, 2, gameManager, False, 2, True),
                               spr.Wall(7, 2, gameManager, True, 2, True),
                               spr.Wall(3, 4, gameManager, False, 7, True),
                               spr.Wall(7, 4, gameManager, True, 6, True),
                               spr.Wall(0, 11, gameManager, False, 16, True),
                               spr.Wall(0, 0, gameManager, False, 16, True),
                               spr.Wall(15, 0, gameManager, True, 8, True),
                               spr.Wall(15, 10, gameManager, True, 2, True))
  box_group = pg.sprite.Group(spr.Box(7, 10, gameManager, False))
  door_group = pg.sprite.Group(spr.Door(15, 8, "W", 3, "key2", gameManager))

  if not (gameManager.searchInv("coin2")):
    collectible_group = pg.sprite.Group(spr.Collectable(6, 3, "coin", "coin2", gameManager))
  else:
    collectible_group = pg.sprite.Group()

  gSwitchWall_group = pg.sprite.Group(
    spr.switchWall(6, 1, gameManager, "green", False),
    spr.switchWall(6, 2, gameManager, "green", True))
  rSwitchWall_group = pg.sprite.Group(
    spr.switchWall(3, 3, gameManager, "red", True))
  switch_group = pg.sprite.Group(
    spr.Switch(5, 1, gameManager, "green", gSwitchWall_group),
    spr.Switch(5, 3, gameManager, "red", rSwitchWall_group))

  all_sprites.add(background, wall_group, gSwitchWall_group, rSwitchWall_group, switch_group, collectible_group, box_group, gameManager.Player,
                  door_group)

  scene_2_b = scn.scene(gameManager, all_sprites)

  ######################### c #######################
  all_sprites = pg.sprite.Group()
  wall_group = pg.sprite.Group(spr.Wall(0, 11, gameManager, False, 16, True),
                               spr.Wall(1, 0, gameManager, False, 10, True),
                               spr.Wall(12, 0, gameManager, False, 4, True),
                               spr.Wall(0, 0, gameManager, True, 12, True))

  all_sprites.add(background, wall_group, gameManager.Player,)

  scene_2_c = scn.scene(gameManager, all_sprites)

  ######################### d #######################
  all_sprites = pg.sprite.Group()
  wall_group = pg.sprite.Group(spr.Wall(0, 11, gameManager, False, 16, True),
                               spr.Wall(15, 0, gameManager, True, 12, True),
                               spr.Wall(0, 0, gameManager, True, 12, True))

  all_sprites.add(background, wall_group, gameManager.Player,)

  scene_2_d = scn.scene(gameManager, all_sprites)

  sceneParts = [[scene_2_a, scene_2_c], [scene_2_b, scene_2_d]]

  return scn.gameLoop(gameManager, sceneParts)

