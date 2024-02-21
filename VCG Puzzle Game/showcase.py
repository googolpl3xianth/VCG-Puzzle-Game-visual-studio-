from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene

  gameManager.Player.rect.x = (1 + .5) * gameManager.tileSize - gameManager.Player.rect.width / 2
  gameManager.Player.rect.y = (6 + .5) * gameManager.tileSize - gameManager.Player.rect.height / 2
  pg.display.set_caption('showcase')
  ##################### a ########################
  all_sprites = pg.sprite.Group()
  background = spr.Background("sprites/BGs/NewBG.png", gameManager)
  wall_group = pg.sprite.Group(spr.Wall(2, 2, gameManager, True, 2, False),
                               spr.Wall(4, 2, gameManager, True, 2, True),
                               spr.Wall(0, 11, gameManager, False, 16, True),
                               spr.Wall(0, 0, gameManager, False, 16, True),
                               spr.Wall(0, 0, gameManager, True, 12, True))
  box_group = pg.sprite.Group(spr.Box(6, 2, gameManager, True),
                              spr.Box(6, 4, gameManager, False),
                              spr.Box(6, 6, gameManager, False))
  shadow_group = pg.sprite.Group()
  enemy_group = pg.sprite.Group(spr.Guard(8, 1, 2, 10, gameManager, False))
  text_group = pg.sprite.Group(spr.text(12, 2, gameManager, "Hello"))
  switchWall_group = pg.sprite.Group(spr.switchWall(14, 3, gameManager, "blue", True),
                                     spr.switchWall(13, 2, gameManager, "blue", False),
                                     spr.switchWall(14, 1, gameManager, "blue", True),
                                     spr.switchWall(15, 2, gameManager, "blue", True))
  switch_group = pg.sprite.Group(
      spr.Switch(14, 2, gameManager, "blue", switchWall_group))

  if not (gameManager.searchInv("keyShowcase")):
    collectible_group = pg.sprite.Group(
        spr.Collectable(10, 2, "key", "keyShowcase",
                        gameManager))
  else:
    collectible_group = pg.sprite.Group()
  all_sprites.add(background, wall_group, switch_group,
                  collectible_group, switchWall_group, box_group, gameManager.Player,
                  enemy_group, shadow_group, text_group)
  scene_1_a = scn.scene(gameManager, all_sprites)

  ######################### b #######################
  all_sprites = pg.sprite.Group()
  wall_group = pg.sprite.Group(spr.Wall(1, 11, gameManager, False, 15, True),
                               spr.Wall(0, 0, gameManager, False, 16, True),
                               spr.Wall(15, 0, gameManager, True, 8, True),
                               spr.Wall(15, 10, gameManager, True, 2, True))
  door_group = pg.sprite.Group(spr.Door(15, 8, "W", 1, "keyShowcase", gameManager))

  all_sprites.add(background, wall_group, gameManager.Player, door_group)

  scene_1_b = scn.scene(gameManager, all_sprites)

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
  door_group = pg.sprite.Group(spr.Door(0, 8, "E", 1, "key", gameManager))
  switchWall_group = pg.sprite.Group(spr.switchWall(1, 3, gameManager, "green", True))
  switch_group = pg.sprite.Group(
      spr.Switch(1, 1, gameManager, "green", switchWall_group))
  box_group = pg.sprite.Group(spr.Box(7, 1, gameManager, True))

  all_sprites.add(background, wall_group, switch_group, box_group,
                  gameManager.Player, door_group)

  scene_1_c = scn.scene(gameManager, all_sprites)

  sceneParts = [[scene_1_a, scene_1_c], [scene_1_b]]

  return scn.gameLoop(gameManager, sceneParts)

