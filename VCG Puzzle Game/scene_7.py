from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene
  pg.display.set_caption('???')
  ##################### a ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((20, 9), gameManager)
  background = spr.Background("sprites/BGs/edge.png", gameManager)
  door_group = (spr.Door((0, 8), "E", (6, [2, 0]), "key6", gameManager))
  wall_group = (spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((0, 1), False, 22, True, gameManager),
                spr.Wall((0, 2), False, 22, True, gameManager),
                spr.Wall((0, 3), False, 22, True, gameManager),
                spr.Wall((0, 4), False, 22, True, gameManager),
                spr.Wall((0, 5), False, 22, True, gameManager),
                spr.Wall((0, 6), False, 22, True, gameManager),
                spr.Wall((0, 7), False, 22, True, gameManager),
                spr.Wall((0, 10), False, 21, True, gameManager),
                spr.Wall((0, 11), False, 22, True, gameManager),
                spr.Wall((21, 9), True, 2, True, gameManager))
  all_sprites.add(background, wall_group, door_group, gameManager.Player, cage)
  scene_7_a = scn.scene(gameManager, all_sprites)

  ##################### b ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((1, 8), gameManager)
  background = spr.Background("sprites/BGs/edge.png", gameManager)
  wall_group = (spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((0, 1), False, 22, True, gameManager),
                spr.Wall((0, 2), False, 22, True, gameManager),
                spr.Wall((0, 3), False, 22, True, gameManager),
                spr.Wall((0, 4), False, 22, True, gameManager),
                spr.Wall((0, 5), False, 22, True, gameManager),
                spr.Wall((0, 6), False, 22, True, gameManager),
                spr.Wall((0, 7), False, 22, True, gameManager),
                spr.Wall((0, 9), False, 22, True, gameManager),
                spr.Wall((0, 10), False, 22, True, gameManager),
                spr.Wall((0, 11), False, 22, True, gameManager),
                spr.Wall((10, 8), True, 1, True, gameManager))
  kill_shadow = (
      spr.killShadow((5, 8, 1, 1), gameManager),
      spr.killShadow((16, 8, 1, 1), gameManager))
  all_sprites.add(background, kill_shadow, wall_group, gameManager.Player, cage)
  scene_7_b = scn.scene(gameManager, all_sprites)

  ##################### c ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((1, 8), gameManager)
  background = spr.Background("sprites/BGs/edge.png", gameManager)
  wall_group = (spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((0, 1), False, 22, True, gameManager),
                spr.Wall((0, 2), False, 22, True, gameManager),
                spr.Wall((0, 3), False, 22, True, gameManager),
                spr.Wall((0, 4), False, 22, True, gameManager),
                spr.Wall((0, 5), False, 22, True, gameManager),
                spr.Wall((0, 6), False, 22, True, gameManager),
                spr.Wall((0, 7), False, 22, True, gameManager),
                spr.Wall((0, 9), False, 22, True, gameManager),
                spr.Wall((0, 10), False, 22, True, gameManager),
                spr.Wall((0, 11), False, 22, True, gameManager))
  kill_shadow = (
      spr.killShadow((5, 8, 1, 1), gameManager),
      spr.killShadow((16, 8, 1, 1), gameManager))
  guard_group = spr.Guard((21, 8), 21, 100, gameManager, True, True)
  all_sprites.add(background, kill_shadow, wall_group, gameManager.Player, guard_group, cage)
  scene_7_c = scn.scene(gameManager, all_sprites)

  ##################### d ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((0, 8), gameManager)
  background = spr.Background("sprites/BGs/edge.png", gameManager)
  wall_group = (spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((0, 1), False, 22, True, gameManager),
                spr.Wall((0, 2), False, 10, True, gameManager),
                spr.Wall((13, 2), False, 9, True, gameManager),
                spr.Wall((0, 3), False, 10, True, gameManager),
                spr.Wall((13, 3), False, 9, True, gameManager),
                spr.Wall((0, 4), False, 10, True, gameManager),
                spr.Wall((13, 4), False, 9, True, gameManager),
                spr.Wall((0, 5), False, 22, True, gameManager),
                spr.Wall((0, 6), False, 22, True, gameManager),
                spr.Wall((0, 7), False, 22, True, gameManager),
                spr.Wall((0, 9), False, 22, True, gameManager),
                spr.Wall((0, 10), False, 22, True, gameManager),
                spr.Wall((0, 11), False, 22, True, gameManager),
                spr.Wall((10, 2), False, 3, True, gameManager),
                spr.Wall((10, 3), True, 1, True, gameManager),
                spr.Wall((10, 4), False, 3, True, gameManager),
                spr.Wall((12, 3), True, 1, True, gameManager))
  kill_shadow = (
      spr.killShadow((11, 3, 1, 1), gameManager),
      spr.killShadow((0, 8, 1, 1), gameManager),
      spr.killShadow((16, 8, 1, 1), gameManager))
  switchWall_group = [spr.switchWall((21, 8), "red", True, gameManager)]
  switch_group = [spr.Switch((11, 3), switchWall_group, gameManager)]
  guard_group = spr.Guard((4, 8), 21, 100, gameManager, True, True)
  all_sprites.add(background, kill_shadow, wall_group, switchWall_group, switch_group, gameManager.Player, guard_group, cage)
  scene_7_d = scn.scene(gameManager, all_sprites)

  ##################### e ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((0, 8), gameManager)
  background = spr.Background("sprites/BGs/edge.png", gameManager)
  wall_group = (spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((0, 1), False, 22, True, gameManager),
                spr.Wall((0, 2), False, 22, True, gameManager),
                spr.Wall((0, 3), False, 22, True, gameManager),
                spr.Wall((0, 4), False, 9, True, gameManager),
                spr.Wall((12, 4), False, 10, True, gameManager),
                spr.Wall((0, 5), False, 9, True, gameManager),
                spr.Wall((12, 5), False, 10, True, gameManager),
                spr.Wall((0, 6), False, 9, True, gameManager),
                spr.Wall((12, 6), False, 10, True, gameManager),
                spr.Wall((0, 7), False, 9, True, gameManager),
                spr.Wall((12, 7), False, 10, True, gameManager),
                spr.Wall((9, 4), True, 4, True, gameManager),
                spr.Wall((11, 4), True, 4, True, gameManager),
                spr.Wall((10, 4), False, 1, True, gameManager),
                spr.Wall((0, 9), False, 22, True, gameManager),
                spr.Wall((0, 10), False, 22, True, gameManager),
                spr.Wall((0, 11), False, 22, True, gameManager))
  kill_shadow = (
      spr.killShadow((10, 5, 1, 1), gameManager),
      spr.killShadow((3, 8, 1, 1), gameManager))
  switchWall_group = [spr.switchWall((9, 8), "red", False, gameManager),
                      spr.switchWall((11, 8), "red", False, gameManager),
                      spr.switchWall((10, 7), "red", False, gameManager)]
  switch_group = [spr.Switch((10, 8), switchWall_group, gameManager)]
  box_group = spr.Box((10, 6), False, gameManager)
  all_sprites.add(background, kill_shadow, wall_group, switchWall_group, switch_group, box_group, gameManager.Player, cage)
  scene_7_e = scn.scene(gameManager, all_sprites)

  ##################### f ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((0, 8), gameManager)
  background = spr.Background("sprites/BGs/edge.png", gameManager)
  wall_group = (spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((0, 1), False, 22, True, gameManager),
                spr.Wall((0, 2), False, 22, True, gameManager),
                spr.Wall((0, 3), False, 22, True, gameManager),
                spr.Wall((0, 4), False, 22, True, gameManager),
                spr.Wall((0, 5), False, 22, True, gameManager),
                spr.Wall((0, 6), False, 22, True, gameManager),
                spr.Wall((0, 7), False, 22, True, gameManager),
                spr.Wall((0, 9), False, 22, True, gameManager),
                spr.Wall((0, 10), False, 22, True, gameManager),
                spr.Wall((0, 11), False, 22, True, gameManager))
  kill_shadow = (
      spr.killShadow((2, 8, 1, 1), gameManager),
      spr.killShadow((8, 8, 1, 1), gameManager))
  switchWall_group = [spr.switchWall((9, 8), "red", False, gameManager),
                      spr.switchWall((11, 8), "red", False, gameManager)]
  switch_group = [spr.Switch((10, 8), switchWall_group, gameManager)]
  box_group = [spr.Box((6, 8), False, gameManager),
               spr.Box((5, 8), True, gameManager)]
  all_sprites.add(background, kill_shadow, wall_group, switchWall_group, switch_group, box_group, gameManager.Player, cage)
  scene_7_f = scn.scene(gameManager, all_sprites)

  ##################### g ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((0, 8), gameManager)
  background = spr.Background("sprites/BGs/edge.png", gameManager)
  wall_group = (spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((0, 1), False, 22, True, gameManager),
                spr.Wall((0, 2), False, 22, True, gameManager),
                spr.Wall((0, 3), False, 22, True, gameManager),
                spr.Wall((0, 4), False, 22, True, gameManager),
                spr.Wall((0, 5), False, 22, True, gameManager),
                spr.Wall((0, 6), False, 22, True, gameManager),
                spr.Wall((0, 7), False, 22, True, gameManager),
                spr.Wall((0, 9), False, 22, True, gameManager),
                spr.Wall((0, 10), False, 22, True, gameManager),
                spr.Wall((0, 11), False, 22, True, gameManager))
  all_sprites.add(background, wall_group, gameManager.Player, cage)
  scene_7_g = scn.scene(gameManager, all_sprites)

  ##################### h ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((0, 8), gameManager)
  background = spr.Background("sprites/BGs/edge.png", gameManager)
  wall_group = (spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((0, 1), False, 22, True, gameManager),
                spr.Wall((0, 2), False, 22, True, gameManager),
                spr.Wall((0, 3), False, 22, True, gameManager),
                spr.Wall((0, 4), False, 22, True, gameManager),
                spr.Wall((0, 5), False, 22, True, gameManager),
                spr.Wall((0, 6), False, 22, True, gameManager),
                spr.Wall((0, 7), False, 22, True, gameManager),
                spr.Wall((0, 9), False, 22, True, gameManager),
                spr.Wall((0, 10), False, 22, True, gameManager),
                spr.Wall((0, 11), False, 22, True, gameManager))
  all_sprites.add(background, wall_group, gameManager.Player, cage)
  scene_7_h = scn.scene(gameManager, all_sprites)

  ##################### i ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((0, 8), gameManager)
  background = spr.Background("sprites/BGs/edge.png", gameManager)
  wall_group = (spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((0, 1), False, 22, True, gameManager),
                spr.Wall((0, 2), False, 22, True, gameManager),
                spr.Wall((0, 3), False, 22, True, gameManager),
                spr.Wall((0, 4), False, 22, True, gameManager),
                spr.Wall((0, 5), False, 22, True, gameManager),
                spr.Wall((0, 6), False, 22, True, gameManager),
                spr.Wall((0, 7), False, 22, True, gameManager),
                spr.Wall((0, 9), False, 22, True, gameManager),
                spr.Wall((0, 10), False, 22, True, gameManager),
                spr.Wall((0, 11), False, 22, True, gameManager))
  all_sprites.add(background, wall_group, gameManager.Player, cage)
  scene_7_i = scn.scene(gameManager, all_sprites)

  ##################### j ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((0, 8), gameManager)
  background = spr.Background("sprites/BGs/edge.png", gameManager)
  wall_group = (spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((0, 1), False, 22, True, gameManager),
                spr.Wall((0, 2), False, 22, True, gameManager),
                spr.Wall((0, 3), False, 22, True, gameManager),
                spr.Wall((0, 4), False, 22, True, gameManager),
                spr.Wall((0, 5), False, 22, True, gameManager),
                spr.Wall((0, 6), False, 22, True, gameManager),
                spr.Wall((0, 7), False, 22, True, gameManager),
                spr.Wall((0, 9), False, 22, True, gameManager),
                spr.Wall((0, 10), False, 22, True, gameManager),
                spr.Wall((0, 11), False, 22, True, gameManager))
  all_sprites.add(background, wall_group, gameManager.Player, cage)
  scene_7_j = scn.scene(gameManager, all_sprites)

  ##################### k ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((1, 1), gameManager)
  background = spr.Background("sprites/BGs/edge.png", gameManager)
  wall_group = (spr.Wall((0, 1), True, 7, True, gameManager),
                spr.Wall((0, 9), True, 2, True, gameManager),
                spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((21, 1), True, 10, True, gameManager),
                spr.Wall((0, 11), False, 22, True, gameManager))
  text_group = (spr.text((2,8), 5, "Thank you for playing", gameManager),
                spr.text((4,8), 5, "credits to:", gameManager),
                spr.text((6,8), 5, "Video Game Creation Club", gameManager),
                spr.text((8,8), 5, "Playtesters: Prem Krishna, Riday Bhatrai, Jason Xie", gameManager))
  all_sprites.add(background, wall_group, gameManager.Player, text_group, cage)
  scene_7_k = scn.scene(gameManager, all_sprites)


  sceneParts = [[scene_7_a], [scene_7_b], [scene_7_c], [scene_7_d], [scene_7_e], [scene_7_f], [scene_7_g], [scene_7_h], [scene_7_i], [scene_7_j], [scene_7_k]]

  return scn.gameLoop(gameManager, sceneParts, [0, 0])
