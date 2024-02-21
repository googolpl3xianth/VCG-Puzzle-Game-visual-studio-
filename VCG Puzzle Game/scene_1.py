from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene

  gameManager.Player.rect.x = (2 + .5) * gameManager.tileSize - gameManager.Player.rect.width / 2
  gameManager.Player.rect.y = (6 + .5) * gameManager.tileSize - gameManager.Player.rect.height / 2

  pg.display.set_caption('scene_1')
  ##################### a ########################
  all_sprites = pg.sprite.Group()
  background = spr.Background("sprites/BGs/NewBG.png", gameManager)

  mentor = spr.Sprite("sprites/NPCs/NMentor.png", 37.5, 100, gameManager, False, False)

  text_group = pg.sprite.Group(spr.text(5, 3, gameManager, "Use shift to enter shadow mode", (0, 255, 255), (0, 255, 0)))

  wall_group = pg.sprite.Group(
      spr.Wall(4, 0, gameManager, True, 12, False),
      spr.Wall(10, 4, gameManager, False, 7, True),
      spr.Wall(8, 0, gameManager, True, 5, True),
      spr.Wall(15, 0, gameManager, True, 5, True),
      spr.Wall(0, 11, gameManager, False, 16, True),
      spr.Wall(0, 0, gameManager, False, 16, True),
      spr.Wall(0, 0, gameManager, True, 12, True))
  box_group = pg.sprite.Group(spr.Box(9, 4, gameManager, True))
  
  if not (gameManager.searchInv("key1")):
    collectible_group = pg.sprite.Group(
        spr.Collectable(13, 2, "key", "key1",
                       gameManager))
  else:
    collectible_group = pg.sprite.Group()

  all_sprites.add(background, wall_group, box_group, collectible_group, mentor, gameManager.Player, text_group)

  scene_1_a = scn.scene(gameManager, all_sprites)


  ######################### b #######################

  all_sprites = pg.sprite.Group()
  wall_group = pg.sprite.Group(
    spr.Wall(4, 4, gameManager, True, 8, True),
    spr.Wall(7, 0, gameManager, True, 8, True),
    spr.Wall(0, 4, gameManager, False, 1, True),
    spr.Wall(0, 0, gameManager, True, 4, True),
    spr.Wall(0, 12, gameManager, False, 16, True),
    spr.Wall(0, 0, gameManager, False, 16, True),
    spr.Wall(4, 11, gameManager, False, 12, True),
    spr.Wall(15, 0, gameManager, True, 8, True),
    spr.Wall(15, 10, gameManager, True, 1, True))
  box_group = pg.sprite.Group(spr.Box(5, 4, gameManager, True),
                            spr.Box(6, 4, gameManager, True))
  door_group = pg.sprite.Group(
    spr.Door(15, 8, "W", 2, "key1", gameManager))
  enemy_group = pg.sprite.Group(spr.Guard(6, 9, 6, 10, gameManager))
  text_group = pg.sprite.Group(
    spr.text(4, 3, gameManager, "be careful of the guard"))

  all_sprites.add(background, wall_group, box_group, gameManager.Player, door_group, enemy_group, text_group)

  scene_1_b = scn.scene(gameManager, all_sprites)

  ##################### c ########################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/NewBG.png", gameManager)

  wall_group = pg.sprite.Group(
                               spr.Wall(12, 0, gameManager, False, 1, True),
                               spr.Wall(2, 3, gameManager, True, 3, True),
                               spr.Wall(2, 7, gameManager, True, 4, True),
                               spr.Wall(3, 5, gameManager, False, 3, True),
                               spr.Wall(3, 7, gameManager, False, 3, True),
                               spr.Wall(12, 2, gameManager, False, 1, True),
                               spr.Wall(10, 3, gameManager, True, 1, True),
                               spr.Wall(13, 7, gameManager, True, 3, True),
                               spr.Wall(10, 4, gameManager, False, 2, True),
                               spr.Wall(13, 4, gameManager, False, 2, True),
                               spr.Wall(13, 0, gameManager, True, 3, True),
                               spr.Wall(0, 11, gameManager, False, 11, True),
                               spr.Wall(2, 2, gameManager, False, 9, True),
                               spr.Wall(0, 11, gameManager, False, 14, True),
                               spr.Wall(0, 0, gameManager, False, 11, True),
                               spr.Wall(0, 0, gameManager, True, 12, True),
                               spr.Wall(15, 1, gameManager, True, 11, True),
                               spr.Wall(10, 9, gameManager, False, 3, True))      

  box_group = pg.sprite.Group(spr.Box(11, 1, gameManager, False), spr.Box(2, 6, gameManager, True))
  rSwitchWall_group = pg.sprite.Group(spr.switchWall(2, 1, gameManager, "red", False), spr.switchWall(1, 2, gameManager, "red", False))
  bSwitchWall_group = pg.sprite.Group(spr.switchWall(12, 3, gameManager, "blue", False), spr.switchWall(12, 5, gameManager, "blue", True), spr.switchWall(14, 6, gameManager, "blue", False), spr.switchWall(13, 10, gameManager, "blue", True))
  gSwitchWall_group = pg.sprite.Group(spr.switchWall(10, 10, gameManager, "green", True))
  switch_group = pg.sprite.Group(spr.Switch(1, 1, gameManager, "red", rSwitchWall_group), spr.Switch(12, 4, gameManager, "blue", bSwitchWall_group), spr.Switch(14, 7, gameManager, "blue", bSwitchWall_group), spr.Switch(14, 8, gameManager, "blue", bSwitchWall_group), spr.Switch(14, 9, gameManager, "blue", bSwitchWall_group), spr.Switch(14, 10, gameManager, "blue", bSwitchWall_group), spr.Switch(14, 11, gameManager, "blue", bSwitchWall_group), spr.Switch(11, 10, gameManager, "green", gSwitchWall_group))

  if not (gameManager.searchInv("coin1")):
    collectible_group = pg.sprite.Group(spr.Collectable(12, 10, "coin", "coin1", gameManager))
  else:
    collectible_group = pg.sprite.Group()

  all_sprites.add(background, wall_group, rSwitchWall_group, bSwitchWall_group, gSwitchWall_group, switch_group, collectible_group, box_group, gameManager.Player)

  scene_1_c = scn.scene(gameManager, all_sprites)
  

  sceneParts = [[scene_1_a, scene_1_c], [scene_1_b]]


  return scn.gameLoop(gameManager, sceneParts)

