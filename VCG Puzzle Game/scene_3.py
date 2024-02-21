
from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene

  gameManager.Player.rect.x = (
      1 + .5) * gameManager.tileSize - gameManager.Player.rect.width / 2
  gameManager.Player.rect.y = (
      8 + .5) * gameManager.tileSize - gameManager.Player.rect.height / 2
  pg.display.set_caption('scene_3')
  ##################### a ########################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/NewBG.png", gameManager)

  wall_group = pg.sprite.Group(spr.Wall(0, 11, gameManager, False, 16, True),
                               spr.Wall(0, 0, gameManager, False, 16, True),
                               spr.Wall(0, 0, gameManager, True, 8, True),
                               spr.Wall(0, 10, gameManager, True, 2, True),
                               spr.Wall(15, 0, gameManager, True, 6, True),
                               spr.Wall(15, 6, gameManager, False, 1, True))
  door_group = pg.sprite.Group(spr.Door(0, 8, "E", 1, "No", gameManager))
  switchWall_group = pg.sprite.Group(
      spr.switchWall(5, 2, gameManager, "green", True),
      spr.switchWall(5, 4, gameManager, "green", True),
      spr.switchWall(5, 6, gameManager, "green", True),
      spr.switchWall(5, 8, gameManager, "green", True),
      spr.switchWall(5, 10, gameManager, "green", True),
      spr.switchWall(6, 1, gameManager, "green", False),
      spr.switchWall(6, 3, gameManager, "green", False),
      spr.switchWall(6, 5, gameManager, "green", False),
      spr.switchWall(6, 7, gameManager, "green", False),
      spr.switchWall(6, 9, gameManager, "green", False),
      spr.switchWall(7, 2, gameManager, "green", True),
      spr.switchWall(7, 4, gameManager, "green", True),
      spr.switchWall(7, 6, gameManager, "green", True),
      spr.switchWall(7, 8, gameManager, "green", True),
      spr.switchWall(7, 10, gameManager, "green", True),
      spr.switchWall(8, 1, gameManager, "green", False),
      spr.switchWall(8, 2, gameManager, "green", False),
      spr.switchWall(8, 3, gameManager, "green", False),
      spr.switchWall(8, 4, gameManager, "green", False),
      spr.switchWall(8, 5, gameManager, "green", False),
      spr.switchWall(8, 6, gameManager, "green", False),
      spr.switchWall(8, 7, gameManager, "green", False),
      spr.switchWall(8, 8, gameManager, "green", False),
      spr.switchWall(8, 9, gameManager, "green", False),
      spr.switchWall(8, 10, gameManager, "green", False))
  switch_group = pg.sprite.Group(
      spr.Switch(5, 3, gameManager, "green", switchWall_group),
      spr.Switch(5, 1, gameManager, "green", switchWall_group),
      spr.Switch(5, 5, gameManager, "green", switchWall_group),
      spr.Switch(5, 7, gameManager, "green", switchWall_group),
      spr.Switch(5, 9, gameManager, "green", switchWall_group),
      spr.Switch(6, 2, gameManager, "green", switchWall_group),
      spr.Switch(6, 4, gameManager, "green", switchWall_group),
      spr.Switch(6, 6, gameManager, "green", switchWall_group),
      spr.Switch(6, 8, gameManager, "green", switchWall_group),
      spr.Switch(6, 10, gameManager, "green", switchWall_group),
      spr.Switch(7, 3, gameManager, "green", switchWall_group),
      spr.Switch(7, 1, gameManager, "green", switchWall_group),
      spr.Switch(7, 5, gameManager, "green", switchWall_group),
      spr.Switch(7, 7, gameManager, "green", switchWall_group),
      spr.Switch(7, 9, gameManager, "green", switchWall_group))
  if not (gameManager.searchInv("key3")):
    collectible_group = pg.sprite.Group(
        spr.Collectable(10, 9, "key", "key3",
                        gameManager))
  else:
    collectible_group = pg.sprite.Group()

  all_sprites.add(background, wall_group, switchWall_group, switch_group,
                  collectible_group, gameManager.Player, door_group)

  scene_3_a = scn.scene(gameManager, all_sprites)

  ######################### b #######################
  all_sprites = pg.sprite.Group()
  wall_group = pg.sprite.Group(spr.Wall(1, 7, gameManager, True, 2, True),
                               spr.Wall(1, 9, gameManager, False, 7, True),
                               spr.Wall(9, 9, gameManager, False, 6, True),
                               spr.Wall(15, 9, gameManager, True, 2, True),
                               spr.Wall(0, 6, gameManager, False, 16, True),
                               spr.Wall(0, 11, gameManager, False, 16, True))
  door_group = pg.sprite.Group(spr.Door(15, 7, "W", 4, "key3", gameManager))

  GSwitchWall_group = pg.sprite.Group(
      spr.switchWall(9, 7, gameManager, "green", True),
      spr.switchWall(9, 8, gameManager, "green", True),
      spr.switchWall(7, 10, gameManager, "green", False),
      spr.switchWall(10, 10, gameManager, "green", False))
  GSwitch_group = pg.sprite.Group(
      spr.Switch(8, 10, gameManager, "green", GSwitchWall_group),
      spr.Switch(9, 10, gameManager, "green", GSwitchWall_group))
  BSwitchWall_group = pg.sprite.Group(
      spr.switchWall(8, 8, gameManager, "blue", False))
  BSwitch_group = pg.sprite.Group(
      spr.Switch(8, 9, gameManager, "blue", BSwitchWall_group))

  kill_shadow = pg.sprite.Group(
      spr.killShadow(0, 0, gameManager.screenWidth // gameManager.tileSize, 6,
                     gameManager))
  all_sprites.add(background, wall_group, GSwitchWall_group, BSwitchWall_group,
                  GSwitch_group, BSwitch_group, kill_shadow,
                  gameManager.Player, door_group)

  scene_3_b = scn.scene(gameManager, all_sprites)

  ############# c #######################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/NewBG.png", gameManager)

  wall_group = pg.sprite.Group(spr.Wall(8, 6, gameManager, False, 4, False),
                               spr.Wall(12, 6, gameManager, True, 10, False),
                               spr.Wall(7, 2, gameManager, True, 14, True),
                               spr.Wall(0, 11, gameManager, False, 16, True),
                               spr.Wall(0, 0, gameManager, False, 16, True),
                               spr.Wall(0, 0, gameManager, True, 8, True),
                               spr.Wall(0, 10, gameManager, True, 2, True))
  box_group = pg.sprite.Group(spr.Box(9, 4, gameManager, True))
  door_group = pg.sprite.Group(spr.Door(0, 8, "E", 1, "key3", gameManager))
  switchWall_group = pg.sprite.Group(
      spr.switchWall(1, 3, gameManager, "red", True))
  switch_group = pg.sprite.Group(
      spr.Switch(1, 1, gameManager, "red", switchWall_group))
  box_group = pg.sprite.Group(spr.Box(7, 1, gameManager, True))

  all_sprites.add(background, wall_group, switch_group, box_group,
                  gameManager.Player, door_group)

  scene_3_c = scn.scene(gameManager, all_sprites)

  sceneParts = [[scene_3_a, scene_3_c], [scene_3_b]]

  return scn.gameLoop(gameManager, sceneParts)
