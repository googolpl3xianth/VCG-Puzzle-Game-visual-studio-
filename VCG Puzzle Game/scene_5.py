from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene
  pg.display.set_caption('scene_5')
  ##################### a ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((1, 1), gameManager)
  background = spr.Background("VCG Puzzle Game/sprites/BGs/edge.png", gameManager)

  wall_group = (spr.Wall((0, 11), False, 22, True, gameManager),
                spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((0, 0), True, 8, True, gameManager),
                spr.Wall((0, 10), True, 2, True, gameManager))
  door_group = (spr.Door((0, 8), "E", (4, [1, 3]), "key4", gameManager))

  all_sprites.add(background, wall_group, gameManager.Player, door_group, cage)

  scene_5_a = scn.scene(gameManager, all_sprites)

  ######################### b #######################
  all_sprites = pg.sprite.Group()
  wall_group = (spr.Wall((1, 11), False, 21, True, gameManager),
                spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((21, 0), True, 8, True, gameManager),
                spr.Wall((21, 10), True, 2, True, gameManager))
  door_group = (spr.Door((21, 8), "W", (6, [0, 0]), "key5", gameManager))

  brokenWall = (spr.Sprite(pg.transform.scale(pg.image.load("VCG Puzzle Game/sprites/Walls/brokenWall.png").convert_alpha(), (gameManager.tileSize[0], gameManager.tileSize[1])), (0, 11), gameManager))

  text = [spr.text((10, 6), 16, "The periods of transition are always wrought with struggles", gameManager)]
  all_sprites.add(background, wall_group, brokenWall, gameManager.Player, text,
                  door_group)

  scene_5_b = scn.scene(gameManager, all_sprites)

  ############# c #######################
  all_sprites = pg.sprite.Group()

  kill_shadow = (
      spr.killShadow(
          (0, 0, (gameManager.screenWidth / gameManager.tileSize[0]) - 3,
           gameManager.screenHeight / gameManager.tileSize[1]), gameManager),
      spr.killShadow(
          (gameManager.screenWidth / gameManager.tileSize[0] - 4, 2, 4,
           (gameManager.screenHeight / gameManager.tileSize[1]) - 2),
          gameManager))

  wall_group = (spr.Wall((19, 0), True, 1, True, gameManager),
                               spr.Wall((19, 1), False, 3, True, gameManager))

  collectible_group = (
      spr.Collectible((20, 0), "key", "key5", gameManager))

  all_sprites.add(background, wall_group, kill_shadow, collectible_group,
                  gameManager.Player)

  scene_5_c = scn.scene(gameManager, all_sprites)
  
  ############################### intermediate #########################
  all_sprites = pg.sprite.Group()
  kill_shadow = (
      spr.killShadow(
          (0, 0, (gameManager.screenWidth / gameManager.tileSize[0]) - 2,
           gameManager.screenHeight / gameManager.tileSize[1]), gameManager),
      spr.killShadow(
          (gameManager.screenWidth / gameManager.tileSize[0] - 4, 2, 4,
           (gameManager.screenHeight / gameManager.tileSize[1]) - 2),
          gameManager))

  wall_group = (spr.Wall((20, 0), True, 1, True, gameManager),
                               spr.Wall((20, 1), False, 2, True, gameManager))


  all_sprites.add(background, wall_group, kill_shadow,
                  gameManager.Player)

  scene_5_left = scn.scene(gameManager, all_sprites)
  
  all_sprites = pg.sprite.Group()
  kill_shadow = (
    spr.killShadow(
        (0, 0, (gameManager.screenWidth / gameManager.tileSize[0]), gameManager.screenHeight / gameManager.tileSize[1] - 2), 
        gameManager),
    spr.killShadow(
        (2, 0, (gameManager.screenWidth / gameManager.tileSize[0]) - 2,
        (gameManager.screenHeight / gameManager.tileSize[1])),
        gameManager))

  wall_group = (spr.Wall((1, 11), True, 1, True, gameManager),
                               spr.Wall((0, 10), False, 2, True, gameManager))
  
  all_sprites.add(background, wall_group, kill_shadow,
                  gameManager.Player)
  scene_5_up = scn.scene(gameManager, all_sprites)
  
  ##################### coin ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((21, 11), gameManager)
  background = spr.Background("VCG Puzzle Game/sprites/BGs/edge.png", gameManager)

  wall_group = (spr.Wall((21, 1), True, 9, True, gameManager),
                spr.Wall((0, 0), False, 19, True, gameManager),
                spr.Wall((21, 0), False, 1, True, gameManager),
                spr.Wall((0, 0), True, 12, True, gameManager),
                spr.Wall((20, 10), False, 2, True, gameManager),
                spr.Wall((18, 9), True, 2, False, gameManager),
                spr.Wall((18, 1), True, 8, True, gameManager),
                spr.Wall((2, 10), False, 16, True, gameManager),
                spr.Wall((2, 3), False, 12, True, gameManager),
                spr.Wall((2, 4), True, 4, False, gameManager),
                spr.Wall((2, 8), True, 2, True, gameManager),
                spr.Wall((16, 8), True, 2, False, gameManager),
                spr.Wall((16, 1), True, 5, True, gameManager),
                spr.Wall((14, 5), False, 2, False, gameManager),
                spr.Wall((4, 7), False, 13, True, gameManager),
                spr.Wall((4, 5), False, 10, True, gameManager))
  
  RSwitchWall_group = [spr.switchWall((16, 11), "red", True, gameManager),
                      spr.switchWall((18, 11), "red", True, gameManager)]
  GSwitchWall_group = [spr.switchWall((17, 5), "green", False, gameManager),
                       spr.switchWall((17, 7), "green", False, gameManager),
                       spr.switchWall((16, 6), "green", False, gameManager)]
  BSwitchWall_group = [spr.switchWall((1, 8), "blue", False, gameManager),
                       spr.switchWall((1, 10), "blue", False, gameManager)]
  
  switch_group = (spr.Switch((17, 1), RSwitchWall_group, gameManager),
                  spr.Switch((17, 11), RSwitchWall_group, gameManager),
                  spr.Switch((17, 6), GSwitchWall_group, gameManager),
                  spr.Switch((1, 9), BSwitchWall_group, gameManager))
  
  spike_group = (spr.Spike((20, 9), gameManager))
  guard_group = (spr.Guard((5, 6), 10, 25, gameManager))

  conveyor_group = (spr.Conveyor((19, 9), "E", gameManager),
                    spr.Conveyor((19, 11), "N", gameManager),
                    spr.Conveyor((6, 2), "N", gameManager),
                    spr.Conveyor((1, 11), "E", gameManager))
  
  box_group = (spr.Box((7, 2), False, gameManager),
               spr.Box((8, 2), False, gameManager),
               spr.Box((9, 2), False, gameManager),
               spr.Box((17, 8), False, gameManager),
               spr.Box((17, 2), False, gameManager),
               spr.Box((4, 6), True, gameManager))

  all_sprites.add(background, wall_group, spike_group, conveyor_group, switch_group, 
                  RSwitchWall_group, GSwitchWall_group, BSwitchWall_group, guard_group, box_group, 
                  gameManager.Player, cage)

  scene_5_coin = scn.scene(gameManager, all_sprites)

  ##################### d ########################
  all_sprites = pg.sprite.Group()
  
  cage = spr.Cage((1, 1), gameManager)
  
  background = spr.Background("VCG Puzzle Game/sprites/BGs/edge.png", gameManager)

  wall_group = (spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((0, 1), True, 11, True, gameManager),
                spr.Wall((21, 1), True, 11, True, gameManager),
                spr.Wall((15, 2), False, 3, True, gameManager),
                spr.Wall((15, 6), False, 3, True, gameManager),
                spr.Wall((14, 2), True, 5, True, gameManager),
                spr.Wall((18, 2), True, 5, True, gameManager))
  
  kill_shadow = (spr.killShadow((15, 3, 3, 3), gameManager),
                 spr.killShadow((12, 4, 1, 1), gameManager))
  
  coin = spr.Collectible((16, 4), "coin", "coin5", gameManager)

  all_sprites.add(background, wall_group, kill_shadow, gameManager.Player, cage, coin)

  scene_5_d = scn.scene(gameManager, all_sprites)
     
  blankScene = scn.scene(gameManager, pg.sprite.Group(), (0, 0), True)

  sceneParts = [[scene_5_d, scene_5_coin, scene_5_a, scene_5_c], [blankScene, scene_5_up, scene_5_b, blankScene]]

  return scn.gameLoop(gameManager, sceneParts, [0, 2])
