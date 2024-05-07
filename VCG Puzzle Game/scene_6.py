from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene
  pg.display.set_caption('???')
  ##################### a ########################
  all_sprites = pg.sprite.Group()
  background = spr.Background("sprites/BGs/blackBG.png", gameManager)
  NPC = spr.NPC(pg.transform.scale(pg.image.load("sprites/NPCs/Mentor.png").convert_alpha(), (int(gameManager.tileSize[0]), int(gameManager.tileSize[1]) * 2)), (4, 6), (["Are you trying to escape?", "If you give me 5 coins I'll help you out", "What? You don't have 5 coins?", "Tough luck", "What? You asking for help?", "Well I know there is a coin in each floor before", "Just think outside the box", "or as far out as you can at least"], ["here is the map", "I wish you good luck"]), len(gameManager.inventoryImage.coins.names) >= 5, gameManager)
  door_group = (spr.Door((0, 8), "E", (5, [1, 2]), "key5", gameManager))
  kill_shadow = (
      spr.killShadow((0, 0, gameManager.screenWidth / gameManager.tileSize[0],
                     gameManager.screenHeight / gameManager.tileSize[1]),
                     gameManager))
  all_sprites.add(background, kill_shadow, door_group, NPC, gameManager.Player,)
  scene_6 = scn.scene(gameManager, all_sprites)

 ##################### b ########################
  all_sprites = pg.sprite.Group()
  background = spr.Background("sprites/BGs/blackBG.png", gameManager)
  door_group = (spr.Door((21, 7), "W", (7, [0, 0]), "key6", gameManager))
  kill_shadow = (
      spr.killShadow((0, 0, gameManager.screenWidth / gameManager.tileSize[0],
                     gameManager.screenHeight / gameManager.tileSize[1]),
                     gameManager))
  all_sprites.add(background, kill_shadow, door_group, gameManager.Player)
  scene_6_exit = scn.scene(gameManager, all_sprites)


  blankScene = scn.scene(gameManager, pg.sprite.Group(), (0, 0), True)


  sceneParts = [[scene_6], [blankScene], [scene_6_exit]]

  return scn.gameLoop(gameManager, sceneParts, [0, 0])
