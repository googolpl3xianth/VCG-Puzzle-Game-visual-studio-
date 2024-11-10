from os import truncate
from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):
  pg.display.set_caption('scene_4')
  ##################### a ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((2, 2), gameManager)
  background = spr.Background("sprites/BGs/edge.png", gameManager)
  wall_group = (spr.Wall((4, 1), True, 5, True, gameManager),
                spr.Wall((4, 7), True, 4, True, gameManager),
                spr.Wall((1, 6), False, 6, False, gameManager),
                spr.Wall((8, 6), False, 14, False, gameManager),
                spr.Wall((10, 1), True, 5, True, gameManager),
                spr.Wall((10, 7), True, 4, True, gameManager),
                spr.Wall((0, 11), False, 22, True, gameManager),
                spr.Wall((0, 0), False, 5, True, gameManager),
                spr.Wall((10, 0), False, 12, True, gameManager),
                spr.Wall((0, 0), True, 7, True, gameManager),
                spr.Wall((0, 9), True, 3, True, gameManager))
  door_group = (spr.Door((0, 7), "E", (3, [1, 0]), "key3", gameManager))
  kill_shadow = (spr.killShadow((7, 6, 1, 1), gameManager))
  collectible_group = (
      spr.Collectible((7, 2), "key", "key4", gameManager))
  all_sprites.add(background, wall_group, collectible_group, kill_shadow,
                  gameManager.Player, door_group, cage)
  scene_4_a = scn.scene(gameManager, all_sprites)

  ######################### b #######################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((0, 10), gameManager)
  wall_group = (spr.Wall((0, 6), False, 21, False, gameManager),
                               spr.Wall((1, 7), False, 20, True, gameManager),
                               spr.Wall((1, 9), False, 15, True, gameManager),
                               spr.Wall((0, 11), False, 22, True, gameManager),
                               spr.Wall((0, 0), False, 22, True, gameManager),
                               spr.Wall((21, 0), True, 8, True, gameManager),
                               spr.Wall((1, 10), True, 1, True, gameManager),
                               spr.Wall((21, 10), True, 2, True, gameManager))
  door_group = (spr.Door((21, 8), "W", (5, [0, 2]), "key4", gameManager))
  gaurd = (spr.Guard((3, 8), 15, 7, gameManager))
  box_group = (spr.Box((1, 8), False, gameManager))
  all_sprites.add(background, wall_group, gaurd, box_group, gameManager.Player, door_group, cage)
  scene_4_b = scn.scene(gameManager, all_sprites)

  ############# c #######################
  all_sprites = pg.sprite.Group()
  background = spr.Background("sprites/BGs/edge.png", gameManager)
  kill_shadow = (
      spr.killShadow((0, 0, (gameManager.screenWidth / gameManager.tileSize[0]),
                      (gameManager.screenHeight // gameManager.tileSize[1]) - 5),
                     gameManager),
      spr.killShadow(
          (0, (gameManager.screenHeight // gameManager.tileSize[1]) - 5, 3, 5),
          gameManager),
      spr.killShadow(
          (0, (gameManager.screenHeight // gameManager.tileSize[1]) - 2, 1, 1),
          gameManager),
      spr.killShadow(
          (4, (gameManager.screenHeight // gameManager.tileSize[1]) - 2, 2, 1),
          gameManager),
      spr.killShadow(
          (3, (gameManager.screenHeight // gameManager.tileSize[1]) - 5, 3, 3),
          gameManager),
      spr.killShadow(
          (5, (gameManager.screenHeight // gameManager.tileSize[1]) - 4, 3, 2),
          gameManager),
      spr.killShadow(
          (7, (gameManager.screenHeight // gameManager.tileSize[1]) - 5, 5, 2),
          gameManager),
      spr.killShadow(
          (13, (gameManager.screenHeight // gameManager.tileSize[1]) - 5, 9, 5),
          gameManager),
      spr.killShadow(
          (12, (gameManager.screenHeight // gameManager.tileSize[1]) - 4, 4, 2),
          gameManager),
      spr.killShadow(
          (10, (gameManager.screenHeight // gameManager.tileSize[1]) - 1, 3, 1),
          gameManager),
      spr.killShadow(
          (10, (gameManager.screenHeight // gameManager.tileSize[1]) - 3, 1, 1),
          gameManager),
      spr.killShadow(
          (11, (gameManager.screenHeight // gameManager.tileSize[1]) - 2, 1, 1),
          gameManager),
      spr.killShadow(
          (13, (gameManager.screenHeight // gameManager.tileSize[1]) - 2, 3, 2),
          gameManager),
      spr.killShadow(
          (3, (gameManager.screenHeight // gameManager.tileSize[1]) - 1, 2, 1),
          gameManager))
  text_group = (spr.text((8, 10), 12, "turn back or be lost to the void", gameManager))
  all_sprites.add(background, kill_shadow, gameManager.Player, text_group)
  scene_4_c = scn.scene(gameManager, all_sprites)
  
  ################### scene_4_path ###################
  all_sprites = pg.sprite.Group()
  tempImage = pg.transform.scale(pg.image.load("sprites/BGs/edge.png").convert_alpha(), (gameManager.tileSize[0], gameManager.tileSize[1]))
  killShadow = (spr.killShadow((0,0,gameManager.screenWidth / gameManager.tileSize[0], 5), gameManager),
                spr.killShadow((0,0,2,gameManager.screenHeight / gameManager.tileSize[1]), gameManager),
                spr.killShadow((0,6,gameManager.screenWidth / gameManager.tileSize[0],6), gameManager),
                spr.killShadow((3,0,19,gameManager.screenHeight / gameManager.tileSize[1]), gameManager))
  all_sprites.add(killShadow, spr.Sprite(tempImage, (2,5), gameManager), gameManager.Player)
  scene_4_path1 = scn.scene(gameManager, all_sprites)
  all_sprites = pg.sprite.Group()
  tempImage = pg.transform.scale(pg.image.load("sprites/BGs/edge.png").convert_alpha(), (gameManager.tileSize[0], gameManager.tileSize[1]))
  killShadow = (spr.killShadow((0,0,gameManager.screenWidth / gameManager.tileSize[0], 9), gameManager),
                spr.killShadow((0,0,15,gameManager.screenHeight / gameManager.tileSize[1]), gameManager),
                spr.killShadow((0,10,gameManager.screenWidth / gameManager.tileSize[0],2), gameManager),
                spr.killShadow((16,0,6,gameManager.screenHeight / gameManager.tileSize[1]), gameManager))
  all_sprites.add(killShadow, spr.Sprite(tempImage, (15,9), gameManager), gameManager.Player)
  scene_4_path2 = scn.scene(gameManager, all_sprites)
  all_sprites = pg.sprite.Group()
  tempImage = pg.transform.scale(pg.image.load("sprites/BGs/edge.png").convert_alpha(), (gameManager.tileSize[0], gameManager.tileSize[1]))
  killShadow = (spr.killShadow((0,0,gameManager.screenWidth / gameManager.tileSize[0], 1), gameManager),
                spr.killShadow((0,0,7,gameManager.screenHeight / gameManager.tileSize[1]), gameManager),
                spr.killShadow((0,2,gameManager.screenWidth / gameManager.tileSize[0],10), gameManager),
                spr.killShadow((8,0,14,gameManager.screenHeight / gameManager.tileSize[1]), gameManager))
  all_sprites.add(killShadow, spr.Sprite(tempImage, (7,1), gameManager), gameManager.Player)
  scene_4_path3 = scn.scene(gameManager, all_sprites)
  all_sprites = pg.sprite.Group()
  killShadow = (spr.killShadow((0,0,gameManager.screenWidth / gameManager.tileSize[0], 7), gameManager),
                spr.killShadow((0,0,21,gameManager.screenHeight / gameManager.tileSize[1]), gameManager),
                spr.killShadow((0,8,gameManager.screenWidth / gameManager.tileSize[0],4), gameManager))
  conveyor = spr.Conveyor((21, 7), "E", gameManager)
  all_sprites.add(killShadow, conveyor, gameManager.Player)
  scene_4_path4 = scn.scene(gameManager, all_sprites)
  
  ######################### coin #######################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((0, 7), gameManager)
  wall_group = (spr.Wall((18, 11), False, 4, True, gameManager),
                spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((21, 1), True, 10, True, gameManager),
                spr.Wall((0, 6), False, 20, True, gameManager),
                spr.Wall((0, 8), False, 19, True, gameManager),
                spr.Wall((18, 9), True, 2, True, gameManager))
  box_group = spr.Box((2, 7), False, gameManager)
  conveyor_group = (spr.Conveyor((20, 7), "N", gameManager),
                    spr.Conveyor((20, 6), "N", gameManager),
                    spr.Conveyor((20, 5), "N", gameManager),
                    spr.Conveyor((0, 4), "N", gameManager),
                    spr.Conveyor((0, 3), "N", gameManager),
                    spr.Conveyor((0, 2), "N", gameManager))
  guard = spr.Guard((3, 7), 5, 5, gameManager)
  RSwitchWall_group = [spr.switchWall((19, 8), "red", True, gameManager),
                       spr.switchWall((1, 7), "red", False, gameManager)]
  GSwitchWall_group = [spr.switchWall((13, 4), "green", True, gameManager),
                       spr.switchWall((3, 1), "green", True, gameManager),
                       spr.switchWall((6, 1), "green", True, gameManager),
                       spr.switchWall((9, 4), "green", True, gameManager),
                       spr.switchWall((13, 1), "green", True, gameManager)]
  BSwitchWall_group = [spr.switchWall((15, 4), "blue", True, gameManager),
                       spr.switchWall((8, 4), "blue", True, gameManager),
                       spr.switchWall((4, 4), "blue", True, gameManager),
                       spr.switchWall((10, 1), "blue", True, gameManager),
                       spr.switchWall((16, 1), "blue", True, gameManager)]
  switch_group = (spr.Switch((20, 1), RSwitchWall_group, gameManager),
                  spr.Switch((15, 7), GSwitchWall_group, gameManager),
                  spr.Switch((16, 7), BSwitchWall_group, gameManager))
  kill_shadow = (spr.killShadow((0, 9, 18, 3), gameManager))
  collectible_group = (
      spr.Collectible((20, 8), "coin", "coin4", gameManager))
  all_sprites.add(background, wall_group, kill_shadow, conveyor_group, RSwitchWall_group, 
                  GSwitchWall_group, BSwitchWall_group, switch_group, 
                  box_group, gameManager.Player, collectible_group, guard, cage)
  scene_4_coin = scn.scene(gameManager, all_sprites)
  blankScene = scn.scene(gameManager, pg.sprite.Group(), (0, 0), True)
  
  # 0 0 1 1
  # 1 1 1 0
  # 1 0 0 0
  # 1 1 0 0

  sceneParts = [[blankScene, scene_4_path1, scene_4_c, scene_4_a], 
                [blankScene, scene_4_path2, blankScene, scene_4_b], 
                [scene_4_path4, scene_4_path3, blankScene, blankScene], 
                [scene_4_coin, blankScene, blankScene, blankScene]]

  return scn.gameLoop(gameManager, sceneParts, [0, 3])
