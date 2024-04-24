from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):
  pg.display.set_caption('scene_3')
  ##################### a ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((1, 10), gameManager)
  background = spr.Background("VCG Puzzle Game/sprites/BGs/edge.png", gameManager)

  wall_group = (spr.Wall((21, .5), True, 3, True, gameManager),
                spr.Wall((21, 4.5), True, 2, True, gameManager),
                spr.Wall((0, 11), False, 22, True, gameManager),
                spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((0, 0), True, 8, True, gameManager),
                spr.Wall((0, 10), True, 2, True, gameManager),
                spr.Wall((21, 6), False, 1, True, gameManager),
                spr.Wall((1, 2), False, 3, True, gameManager),
                spr.Wall((2, 4), True, 4, True, gameManager))
  door_group = (spr.Door((0, 8), "E", (2, [1, 0]), "key2", gameManager))
  switchWall_group = [
      spr.switchWall((19, 1), "green", True, gameManager),
      spr.switchWall((20, 2), "green", True, gameManager)]
  switch_group = (
      spr.Switch((1, 1), switchWall_group, gameManager))
  
  spike_group = (spr.Spike((2,1), gameManager))
  
  conveyor_group = (spr.Conveyor((3, 1), "W", gameManager), 
                    spr.Conveyor((1, 3), "E", gameManager),
                    spr.Conveyor((1, 5), "N", gameManager),
                    spr.Conveyor((1, 6), "N", gameManager),
                    spr.Conveyor((1, 7), "N", gameManager),
                    spr.Conveyor((15, 10), "N", gameManager))
  
  box_group = (spr.Box((2, 3), True, gameManager), spr.Box((3, 10), True, gameManager))
  collectible_group = (
      spr.Collectible((20, 1), "key", "key3", gameManager))

  all_sprites.add(background, wall_group, conveyor_group, switchWall_group, switch_group, spike_group, box_group,
                  gameManager.Player, collectible_group, door_group, cage)

  scene_3_a = scn.scene(gameManager, all_sprites)

  ######################### b #######################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((0, 7), gameManager)
  wall_group = (spr.Wall((1, 7), True, 2, True, gameManager),
                               spr.Wall((1, 9), False, 7, True, gameManager),
                               spr.Wall((9, 9), False, 12, True, gameManager),
                               spr.Wall((21, 9), True, 2, True, gameManager),
                               spr.Wall((0, 6), False, 22, True, gameManager),
                               spr.Wall((0, 11), False, 22, True, gameManager))
  door_group = (spr.Door((21, 7), "W", (4, [0, 3]), "key3", gameManager))
  
  GSwitchWall_group = [
      spr.switchWall((9, 7), "green", True, gameManager),
      spr.switchWall((9, 8), "green", True, gameManager),
      spr.switchWall((7, 10), "green", False, gameManager)]
  BSwitchWall_group = [
      spr.switchWall((8, 8), "blue", False, gameManager)]
  switch_group = (
      spr.Switch((8, 10), GSwitchWall_group, gameManager),
      spr.Switch((9, 10), GSwitchWall_group, gameManager),
      spr.Switch((10, 10), GSwitchWall_group, gameManager),
      spr.Switch((11, 10), GSwitchWall_group, gameManager),
      spr.Switch((12, 10), GSwitchWall_group, gameManager),
      spr.Switch((13, 10), GSwitchWall_group, gameManager),
      spr.Switch((14, 10), GSwitchWall_group, gameManager),
      spr.Switch((15, 10), GSwitchWall_group, gameManager),
      spr.Switch((16, 10), GSwitchWall_group, gameManager),
      spr.Switch((17, 10), GSwitchWall_group, gameManager),
      spr.Switch((18, 10), GSwitchWall_group, gameManager),
      spr.Switch((19, 10), GSwitchWall_group, gameManager),
      spr.Switch((20, 10), GSwitchWall_group, gameManager),
      spr.Switch((10, 7), GSwitchWall_group, gameManager),
      spr.Switch((10, 8), GSwitchWall_group, gameManager),
      spr.Switch((8, 9), BSwitchWall_group, gameManager))

  kill_shadow = (
      spr.killShadow(
          (0, 0, gameManager.screenWidth / gameManager.tileSize[0], 6),
          gameManager))
  
  conveyor = (spr.Conveyor((21, 4), "E", gameManager), spr.Conveyor((20, 3), "S", gameManager))
  
  all_sprites.add(background, wall_group, kill_shadow, conveyor, 
                  GSwitchWall_group, BSwitchWall_group, switch_group,
                  gameManager.Player, door_group, cage)

  scene_3_b = scn.scene(gameManager, all_sprites)
  
  ##################### c ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((2, 6), gameManager)
  background = spr.Background("VCG Puzzle Game/sprites/BGs/edge.png", gameManager)

  wall_group = (
                spr.Wall((0, 11), False, 22, True, gameManager),
                spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((0, 3), False, 4, True, gameManager),
                spr.Wall((0, 5), False, 4, True, gameManager),
                spr.Wall((3, 6), True, 2, True, gameManager),
                spr.Wall((3, 9), True, 2, True, gameManager),
                spr.Wall((3, 1), True, 2, True, gameManager),
                spr.Wall((5, 6), True, 3, True, gameManager),
                spr.Wall((5, 1), True, 2, True, gameManager),
                spr.Wall((5, 3), False, 4, True, gameManager),
                spr.Wall((5, 5), False, 4, True, gameManager),
                spr.Wall((10, 1), True, 6, True, gameManager),
                spr.Wall((10, 7), False, 1, True, gameManager),
                spr.Wall((11, 7), True, 2, True, gameManager),
                spr.Wall((11, 9), False, 3, True, gameManager),
                spr.Wall((0, 7), True, 3, True, gameManager),
                spr.Wall((8, 6), True, 1, True, gameManager))

  RSwitchWall_group = [
      spr.switchWall((6, 4), "red", False, gameManager),
      spr.switchWall((8, 4), "red", False, gameManager)]
  BSwitchWall_group = [
      spr.switchWall((4, 7), "blue", False, gameManager),
      spr.switchWall((9, 2), "blue", True, gameManager),
      spr.switchWall((9, 6), "blue", False, gameManager)]
  GSwitchWall_group = [
      spr.switchWall((5, 9), "green", True, gameManager),
      spr.switchWall((5, 10), "green", True, gameManager),
      spr.switchWall((11, 10), "green", True, gameManager),
      spr.switchWall((13, 10), "green", True, gameManager)]
  switch_group = (
      spr.Switch((7, 4), RSwitchWall_group, gameManager),
      spr.Switch((4, 1), BSwitchWall_group, gameManager),
      spr.Switch((6, 7), GSwitchWall_group, gameManager),
      spr.Switch((12, 10), GSwitchWall_group, gameManager))
  
  box_group = (spr.Box((4, 2), False, gameManager), 
               spr.Box((4, 6), False, gameManager), 
               spr.Box((8, 2), True, gameManager))

  all_sprites.add(background, wall_group, RSwitchWall_group, BSwitchWall_group, GSwitchWall_group, switch_group, box_group,
                  gameManager.Player, cage)

  scene_3_c = scn.scene(gameManager, all_sprites)
  
  ######################### d #######################
  all_sprites = pg.sprite.Group()
  
  cage = (spr.Cage((12, 6), gameManager))
  wall_group = (spr.Wall((0, 11), False, 22, True, gameManager),
                spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((21, 1), True, 2, True, gameManager))

  spike = spr.Spike((10, 6), gameManager)

  all_sprites.add(background, wall_group, gameManager.Player,
                  spike, cage)

  scene_3_d = scn.scene(gameManager, all_sprites)
  
  ######################### e #######################
  all_sprites = pg.sprite.Group()
  wall_group = (spr.Wall((0, 11), False, 22, True, gameManager),
                spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((21, 1), True, 10, True, gameManager),
                spr.Wall((1, 1), True, 1, True, gameManager),
                spr.Wall((1, 2), False, 1, True, gameManager),
                spr.Wall((0, 2), False, 1, True, gameManager))
  
  spike = (spr.Spike((10, 6), gameManager))

  collectible_group = (
      spr.Collectible((0, 1), "coin", "coin3", gameManager))
  
  all_sprites.add(background, wall_group, spike, gameManager.Player, collectible_group)

  scene_3_e = scn.scene(gameManager, all_sprites)

  sceneParts = [[scene_3_a], [scene_3_b], [scene_3_c], [scene_3_d], [scene_3_e]]

  return scn.gameLoop(gameManager, sceneParts, [0, 0])
