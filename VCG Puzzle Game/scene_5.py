from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene

  gameManager.Player.rect.x = (1 + .5) * gameManager.tileSize - gameManager.Player.rect.width / 2
  gameManager.Player.rect.y = (8 + .5) * gameManager.tileSize - gameManager.Player.rect.height / 2
  pg.display.set_caption('???')
  ##################### a ########################
  all_sprites = pg.sprite.Group()

  background = spr.Background("sprites/BGs/NewBlackBG.png", gameManager)

  door_group = pg.sprite.Group(spr.Door(0, 8, "E", 1, "No", gameManager))

  text_group = pg.sprite.Group(spr.text(4, 7, gameManager, "return to the beginning", (0, 255, 255), (0, 255, 0)), spr.text(4, 5, gameManager, "there are more places to go", (0, 255, 255), (0, 255, 0)), spr.text(4, 3, gameManager, "press esc then g", (0, 255, 255), (0, 255, 0)))

  kill_shadow = pg.sprite.Group(spr.killShadow(0, 0, gameManager.screenWidth // gameManager.tileSize, gameManager.screenHeight // gameManager.tileSize, gameManager))

  all_sprites.add(background, kill_shadow, door_group,
                  gameManager.Player, text_group)

  scene_5 = scn.scene(gameManager, all_sprites)

  sceneParts = [[scene_5]]

  return scn.gameLoop(gameManager, sceneParts)

