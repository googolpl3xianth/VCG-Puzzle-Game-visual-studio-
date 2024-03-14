from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene
  pg.display.set_caption('scene_5')
  ##################### a ########################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/edge.png", gameManager)

  wall_group = pg.sprite.Group(spr.Wall((0, 11), False, 22, True, gameManager),
                               spr.Wall((0, 0), False, 22, True, gameManager),
                               spr.Wall((0, 0), True, 8, True, gameManager),
                               spr.Wall((0, 10), True, 2, True, gameManager))
  door_group = pg.sprite.Group(spr.Door((0, 8), "E", (4, [1, 1]), "key5", gameManager))

  all_sprites.add(background, wall_group, gameManager.Player, door_group)

  scene_5_a = scn.scene(gameManager, all_sprites, (1, 8))

  ######################### b #######################
  all_sprites = pg.sprite.Group()
  wall_group = pg.sprite.Group(spr.Wall((1, 11), False, 21, True, gameManager),
                               spr.Wall((0, 0), False, 22, True, gameManager),
                               spr.Wall((21, 0), True, 8, True, gameManager),
                               spr.Wall((21, 10), True, 2, True, gameManager))
  door_group = pg.sprite.Group(spr.Door((21, 8), "W", (6, [0, 0]), "key6", gameManager))

  brokenWall = pg.sprite.Group(spr.Sprite(pg.transform.scale(pg.image.load("sprites/Walls/brokenWall.png").convert_alpha(), (gameManager.tileSize[0], gameManager.tileSize[1])), (0, 11), gameManager))

  all_sprites.add(background, wall_group, brokenWall, gameManager.Player,
                  door_group)

  scene_5_b = scn.scene(gameManager, all_sprites, (0, 8))

  ############# c #######################
  all_sprites = pg.sprite.Group()

  kill_shadow = pg.sprite.Group(
      spr.killShadow(
          (0, 0, (gameManager.screenWidth / gameManager.tileSize[0]) - 3,
           gameManager.screenHeight / gameManager.tileSize[1]), gameManager),
      spr.killShadow(
          (gameManager.screenWidth / gameManager.tileSize[0] - 4, 2, 4,
           (gameManager.screenHeight / gameManager.tileSize[1]) - 2),
          gameManager))

  wall_group = pg.sprite.Group(spr.Wall((19, 0), True, 1, True, gameManager),
                               spr.Wall((19, 1), False, 3, True, gameManager))

  if not (gameManager.inventoryImage.searchInv("key6")):
    collectible_group = pg.sprite.Group(
        spr.Collectible((20, 0), "key", "key6", gameManager))
  else:
    collectible_group = pg.sprite.Group()

  all_sprites.add(background, wall_group, kill_shadow, collectible_group,
                  gameManager.Player)

  scene_5_c = scn.scene(gameManager, all_sprites, (21, 0))

  sceneParts = [[scene_5_a, scene_5_c], [scene_5_b]]

  return scn.gameLoop(gameManager, sceneParts, [0, 0])
