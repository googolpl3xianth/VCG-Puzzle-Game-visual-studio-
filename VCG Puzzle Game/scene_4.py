from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene

  gameManager.Player.rect.x = (1 + .5) * gameManager.tileSize - gameManager.Player.rect.width / 2
  gameManager.Player.rect.y = (8 + .5) * gameManager.tileSize - gameManager.Player.rect.height / 2
  pg.display.set_caption('scene_4')
  ##################### a ########################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/NewBG.png", gameManager)

  wall_group = pg.sprite.Group(
                               spr.Wall(0, 11, gameManager, False, 16, True),
                               spr.Wall(0, 0, gameManager, False, 16, True),
                               spr.Wall(0, 0, gameManager, True, 8, True),
                               spr.Wall(0, 10, gameManager, True, 2, True))
  door_group = pg.sprite.Group(spr.Door(0, 8, "E", 1, "No", gameManager))

  all_sprites.add(background, wall_group, gameManager.Player, door_group)

  scene_4_a = scn.scene(gameManager, all_sprites)

  ######################### b #######################
  all_sprites = pg.sprite.Group()
  wall_group = pg.sprite.Group(spr.Wall(1, 11, gameManager, False, 15, True),
                               spr.Wall(0, 0, gameManager, False, 16, True),
                               spr.Wall(15, 0, gameManager, True, 8, True),
                               spr.Wall(15, 10, gameManager, True, 2, True))
  door_group = pg.sprite.Group(spr.Door(15, 8, "W", 5, "key4", gameManager))

  all_sprites.add(background, wall_group, gameManager.Player, door_group)

  scene_4_b = scn.scene(gameManager, all_sprites)

  ############# c #######################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/NewBG.png", gameManager)

  kill_shadow = pg.sprite.Group(spr.killShadow(0, 0, (gameManager.screenWidth // gameManager.tileSize) - 3, gameManager.screenHeight // gameManager.tileSize, gameManager),
                                spr.killShadow(gameManager.screenWidth // gameManager.tileSize - 3, 2, 3, (gameManager.screenHeight // gameManager.tileSize) - 2, gameManager))

  wall_group = pg.sprite.Group(spr.Wall(13, 0, gameManager, True, 1, True),
                               spr.Wall(13, 1, gameManager, False, 3, True))

  if not (gameManager.searchInv("key4")):
    collectible_group = pg.sprite.Group(
        spr.Collectable(14, 0, "key", "key4",
                        gameManager))
  else:
    collectible_group = pg.sprite.Group()

  all_sprites.add(background, wall_group, kill_shadow, collectible_group,
                  gameManager.Player)

  scene_4_c = scn.scene(gameManager, all_sprites)

  sceneParts = [[scene_4_a, scene_4_c], [scene_4_b]]

  return scn.gameLoop(gameManager, sceneParts)
