from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene
  pg.display.set_caption('scene_2')
  ##################### a ########################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/edge.png", gameManager)

  wall_group = (spr.Wall((8, 7), False, 4, False, gameManager),
                spr.Wall((11, 7), True, 5, False, gameManager),
                spr.Wall((0, 11), False, 11, True, gameManager),
                spr.Wall((12, 11), False, 10, True, gameManager),
                spr.Wall((7, 3), True, 9, True, gameManager),
                spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((0, 0), True, 8, True, gameManager),
                spr.Wall((0, 10), True, 2, True, gameManager))
  door_group = (spr.Door((0, 8), "E", (1, [1, 0]), "key1", gameManager))
  switchWall_group = (
      spr.switchWall((7, 1), "red", False, gameManager),
      spr.switchWall((7, 2), "red", False, gameManager))
  switch_group = (
      spr.Switch((6, 1), "red", switchWall_group, gameManager),
      spr.Switch((6, 2), "red", switchWall_group, gameManager))

  collectible_group = (
      spr.Collectible((9, 9), "key", "key2", gameManager))
  all_sprites.add(background, wall_group, switchWall_group, switch_group,
                  collectible_group, gameManager.Player, door_group)

  scene_2_a = scn.scene(gameManager, all_sprites, (1, 8))

  ######################### b #######################
  all_sprites = pg.sprite.Group()
  wall_group = (spr.Wall((3, 1), True, 2, True, gameManager),
                               spr.Wall((4, 2), False, 2, True, gameManager),
                               spr.Wall((7, 2), True, 2, True, gameManager),
                               spr.Wall((3, 4), False, 7, True, gameManager),
                               spr.Wall((7, 4), True, 6, True, gameManager),
                               spr.Wall((0, 11), False, 22, True, gameManager),
                               spr.Wall((0, 0), False, 22, True, gameManager),
                               spr.Wall((21, 0), True, 8, True, gameManager),
                               spr.Wall((21, 10), True, 2, True, gameManager))
  box_group = (spr.Box((7, 10), False, gameManager))
  door_group = (spr.Door((21, 8), "W", (3, [0, 0]), "key2", gameManager))

  collectible_group = (
      spr.Collectible((6, 3), "coin", "coin2", gameManager))

  gSwitchWall_group = (
      spr.switchWall((6, 1), "green", False, gameManager),
      spr.switchWall((6, 2), "green", True, gameManager))
  rSwitchWall_group = (
      spr.switchWall((3, 3), "red", True, gameManager))
  switch_group = (
      spr.Switch((5, 1), "green", gSwitchWall_group, gameManager),
      spr.Switch((5, 3), "red", rSwitchWall_group, gameManager))

  all_sprites.add(background, wall_group, gSwitchWall_group, rSwitchWall_group,
                  switch_group, collectible_group, box_group,
                  gameManager.Player, door_group)

  scene_2_b = scn.scene(gameManager, all_sprites, (0,8))

  ######################### c #######################
  all_sprites = pg.sprite.Group()
  wall_group = (spr.Wall((0, 11), False, 22, True, gameManager),
                spr.Wall((1, 0), False, 9, True, gameManager),
                spr.Wall((12, 0), False, 10, True, gameManager),
                spr.Wall((0, 0), True, 12, True, gameManager),
                spr.Wall((13, 1), True, 8, True, gameManager))
  
  conveyor_group = (spr.Conveyor((12, 1), "S", gameManager),
                    spr.Conveyor((12, 3), "N", gameManager),
                    spr.Conveyor((11, 2), "W", gameManager),
                    spr.Conveyor((10, 2), "W", gameManager),
                    spr.Conveyor((9, 2), "W", gameManager),
                    spr.Conveyor((8, 2), "W", gameManager),
                    spr.Conveyor((7, 2), "W", gameManager),
                    spr.Conveyor((6, 2), "W", gameManager),
                    spr.Conveyor((5, 2), "W", gameManager),
                    spr.Conveyor((4, 2), "W", gameManager),
                    spr.Conveyor((3, 2), "W", gameManager),
                    spr.Conveyor((2, 2), "W", gameManager),
                    spr.Conveyor((1, 3), "S", gameManager),
                    spr.Conveyor((1, 5), "N", gameManager),
                    spr.Conveyor((2, 4), "E", gameManager),
                    spr.Conveyor((3, 4), "E", gameManager),
                    spr.Conveyor((4, 4), "E", gameManager),
                    spr.Conveyor((5, 4), "E", gameManager),
                    spr.Conveyor((6, 4), "E", gameManager),
                    spr.Conveyor((7, 4), "E", gameManager),
                    spr.Conveyor((8, 4), "E", gameManager),
                    spr.Conveyor((9, 4), "E", gameManager),
                    spr.Conveyor((10, 4), "E", gameManager),
                    spr.Conveyor((11, 4), "E", gameManager),
                    spr.Conveyor((12, 5), "S", gameManager),
                    spr.Conveyor((12, 7), "N", gameManager),
                    spr.Conveyor((11, 6), "W", gameManager),
                    spr.Conveyor((10, 6), "W", gameManager),
                    spr.Conveyor((9, 6), "W", gameManager),
                    spr.Conveyor((8, 6), "W", gameManager),
                    spr.Conveyor((7, 6), "W", gameManager),
                    spr.Conveyor((6, 6), "W", gameManager),
                    spr.Conveyor((5, 6), "W", gameManager),
                    spr.Conveyor((4, 6), "W", gameManager),
                    spr.Conveyor((3, 6), "W", gameManager),
                    spr.Conveyor((2, 6), "W", gameManager),
                    spr.Conveyor((1, 7), "S", gameManager),
                    spr.Conveyor((2, 8), "E", gameManager),
                    spr.Conveyor((3, 8), "E", gameManager),
                    spr.Conveyor((4, 8), "E", gameManager),
                    spr.Conveyor((5, 8), "E", gameManager),
                    spr.Conveyor((6, 8), "E", gameManager),
                    spr.Conveyor((7, 8), "E", gameManager),
                    spr.Conveyor((8, 8), "E", gameManager),
                    spr.Conveyor((9, 8), "E", gameManager),
                    spr.Conveyor((10, 8), "E", gameManager),
                    spr.Conveyor((11, 8), "E", gameManager),
                    spr.Conveyor((12, 10), "E", gameManager))

  all_sprites.add(
      background,
      wall_group,
      conveyor_group,
      gameManager.Player,
  )

  scene_2_c = scn.scene(gameManager, all_sprites, (11, 0))

  ######################### d #######################
  all_sprites = pg.sprite.Group()
  wall_group = (spr.Wall((0, 11), False, 22, True, gameManager),
                               spr.Wall((21, 0), True, 12, True, gameManager),
                               spr.Wall((3, 1), True, 10, False, gameManager),
                               spr.Wall((9, 1), True, 6 , False, gameManager),
                               spr.Wall((5, 9), False, 16, True, gameManager),
                               spr.Wall((5, 7), False, 5, True, gameManager),
                               spr.Wall((0, 0), False, 19, True, gameManager))
  box_group = (spr.Box((15, 4), True, gameManager), 
               spr.Box((8, 8), False, gameManager))
  switchWall_group = (spr.switchWall((19, 0), "blue", True, gameManager))
  switch_group = (spr.Switch((20,10), "blue", switchWall_group, gameManager))
  conveyor = (spr.Conveyor((19, 10), "E", gameManager))
  spike = (spr.Spike((5, 8), gameManager))
  all_sprites.add(
      background,
      wall_group, conveyor, switchWall_group, switch_group, spike, box_group,
      gameManager.Player,
  )

  scene_2_d = scn.scene(gameManager, all_sprites, (0, 3))

  sceneParts = [[scene_2_a, scene_2_c], [scene_2_b, scene_2_d]]

  return scn.gameLoop(gameManager, sceneParts, [0, 0])
