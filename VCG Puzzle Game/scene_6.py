from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene
  pg.display.set_caption('???')
  ##################### a ########################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/blackBG.png", gameManager)

  door_group = (spr.Door((0, 8), "E", (5, [1, 2]), "key5", gameManager))

  text_group = (
      spr.text((4, 7), 12, "there are 5 coins to collect",
               gameManager),
      spr.text((4, 5), 12, "scattered at the edges of each past scene", gameManager))

  kill_shadow = (
      spr.killShadow((0, 0, gameManager.screenWidth / gameManager.tileSize[0],
                     gameManager.screenHeight / gameManager.tileSize[1]),
                     gameManager))

  all_sprites.add(background, kill_shadow, door_group, gameManager.Player,
                  text_group)

  scene_6 = scn.scene(gameManager, all_sprites)

 ##################### b ########################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/blackBG.png", gameManager)

  collectible_group = (
      spr.Collectible((11, 6), "key", "key6", gameManager))
  door_group = (spr.Door((21, 6), "W", (6, [0, 0]), "key6", gameManager))
  kill_shadow = (
      spr.killShadow((0, 0, gameManager.screenWidth / gameManager.tileSize[0],
                     gameManager.screenHeight / gameManager.tileSize[1]),
                     gameManager))

  all_sprites.add(background, kill_shadow, collectible_group, door_group, gameManager.Player)
  scene_6_exit = scn.scene(gameManager, all_sprites)


  blankScene = scn.scene(gameManager, pg.sprite.Group(), (0, 0), True)


  sceneParts = [[scene_6], [blankScene], [scene_6_exit]]

  return scn.gameLoop(gameManager, sceneParts, [0, 0])
