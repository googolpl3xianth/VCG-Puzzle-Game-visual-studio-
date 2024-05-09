from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene
  pg.display.set_caption('scene_2')
  ##################### a ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((1, 1), gameManager)
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
  switchWall_group = [
      spr.switchWall((7, 1), "red", False, gameManager),
      spr.switchWall((7, 2), "red", False, gameManager)]
  switch_group = (
      spr.Switch((6, 1), switchWall_group, gameManager),
      spr.Switch((6, 2), switchWall_group, gameManager))
  collectible_group = (
      spr.Collectible((9, 9), "key", "key2", gameManager))
  all_sprites.add(background, wall_group, switchWall_group, switch_group,
                  collectible_group, gameManager.Player, door_group, cage)
  scene_2_a = scn.scene(gameManager, all_sprites)

  ######################### b #######################
  all_sprites = pg.sprite.Group()
  cage = (spr.Cage((1, 1), gameManager))
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
  gSwitchWall_group = [
      spr.switchWall((6, 1), "green", False, gameManager),
      spr.switchWall((6, 2), "green", True, gameManager)]
  rSwitchWall_group = [
      spr.switchWall((3, 3), "red", True, gameManager)]
  switch_group = (
      spr.Switch((5, 1), gSwitchWall_group, gameManager),
      spr.Switch((5, 3), rSwitchWall_group, gameManager))
  all_sprites.add(background, wall_group, gSwitchWall_group, rSwitchWall_group,
                  switch_group, collectible_group, box_group,
                  gameManager.Player, door_group, cage)
  scene_2_b = scn.scene(gameManager, all_sprites)

  ######################### c #######################
  all_sprites = pg.sprite.Group()
  wall_group = (spr.Wall((0, 11), False, 22, True, gameManager),
                spr.Wall((1, 0), False, 10, True, gameManager),
                spr.Wall((12, 0), False, 10, True, gameManager),
                spr.Wall((0, 0), True, 13, True, gameManager))
  all_sprites.add(
      background, wall_group, gameManager.Player
  )
  scene_2_c = scn.scene(gameManager, all_sprites)

  ######################### d #######################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((0, 1), gameManager)
  wall_group = (spr.Wall((0, 11), False, 19, True, gameManager),
                spr.Wall((20, 11), False, 2, True, gameManager),
                spr.Wall((21, 0), True, 12, True, gameManager),
                spr.Wall((3, 1), True, 10, False, gameManager),
                spr.Wall((9, 1), True, 6 , False, gameManager),
                spr.Wall((5, 9), False, 16, True, gameManager),
                spr.Wall((5, 7), False, 5, True, gameManager),
                spr.Wall((0, 0), False, 19, True, gameManager))
  box_group = (spr.Box((15, 4), True, gameManager), 
               spr.Box((8, 8), False, gameManager))
  switchWall_group = [spr.switchWall((19, 0), "blue", True, gameManager)]
  switch_group = [spr.Switch((20,10), switchWall_group, gameManager)]
  conveyor = (spr.Conveyor((19, 10), "E", gameManager))
  spike = (spr.Spike((5, 8), gameManager))
  all_sprites.add(
      background,
      wall_group, conveyor, switchWall_group, switch_group, spike, box_group,
      gameManager.Player, cage
  )
  scene_2_d = scn.scene(gameManager, all_sprites)
  
  ######################### e #######################
  all_sprites = pg.sprite.Group()
  background = spr.Background("sprites/BGs/edge.png", gameManager)
  kill_shadow = (
      spr.killShadow((0, 0, gameManager.screenWidth // gameManager.tileSize[0],
                     6),
                     gameManager),
      spr.killShadow((0, 7, gameManager.screenWidth // gameManager.tileSize[0],
                     5),
                     gameManager),
      spr.killShadow((0, 0, 10,
                     gameManager.screenHeight // gameManager.tileSize[1]),
                     gameManager),
      spr.killShadow((11, 0, gameManager.screenWidth // gameManager.tileSize[0],
                     10),
                     gameManager))
  text = (spr.text((10, 6), 20, "As long as there is a physical object, you are anchored to the real world", gameManager))
  all_sprites.add(
      background, kill_shadow, gameManager.Player, text
  )
  scene_2_e = scn.scene(gameManager, all_sprites)
  blankScene = scn.scene(gameManager, pg.sprite.Group(), (0, 0), True)
  sceneParts = [[scene_2_a, scene_2_c, blankScene], [scene_2_b, scene_2_d, scene_2_e]]

  return scn.gameLoop(gameManager, sceneParts, [0, 0])
