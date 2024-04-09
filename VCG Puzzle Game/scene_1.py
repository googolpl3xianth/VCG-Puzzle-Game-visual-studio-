from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene

  pg.display.set_caption('scene_1')
  ##################### a ########################
  all_sprites = pg.sprite.Group()
  background = spr.Background("sprites/BGs/edge.png", gameManager)

  mentorImage = Image.open("sprites/NPCs/Mentor.png").crop((100, 80, 332, 590)).save("sprites/NPCs/NMentor.png")
  mentorImage = pg.transform.scale(pg.image.load("sprites/NPCs/NMentor.png").convert_alpha(), (int(gameManager.tileSize[0]), int(gameManager.tileSize[1]) * 2))
  mentor = spr.Sprite(mentorImage, (2, 3.5), gameManager, True)

  text_group = (
      spr.text((3, 3), 8, "Use SPACE to enter shadow mode", gameManager, 1))

  wall_group = (spr.Wall((6, 0), True, 12, False, gameManager),
                               spr.Wall((11, 2), False, 1, True, gameManager),
                               spr.Wall((12, 4), False, 9, True, gameManager),
                               spr.Wall((10, 0), True, 5, True, gameManager),
                               spr.Wall((21, 0), True, 5, True, gameManager),
                               spr.Wall((0, 11), False, 22, True, gameManager),
                               spr.Wall((0, 0), False, 22, True, gameManager),
                               spr.Wall((0, 0), True, 12, True, gameManager))
  box_group = (spr.Box((11, 4), False, gameManager))

  collectible_group = (
      spr.Collectible((15, 2), "key", "key1", gameManager))
  
  

  all_sprites.add(background, wall_group, box_group, collectible_group, mentor,
                  gameManager.Player, text_group)

  scene_1_a = scn.scene(gameManager, all_sprites, (2, 6))

  ######################### b #######################

  all_sprites = pg.sprite.Group()
  wall_group = (               spr.Wall((4, 5), True, 6, True, gameManager),
                               spr.Wall((7, 7), False, 14, True, gameManager),
                               spr.Wall((7, 1), True, 6, True, gameManager),
                               spr.Wall((0, 4), False, 1, True, gameManager),
                               spr.Wall((0, 0), True, 4, True, gameManager),
                               spr.Wall((0, 0), False, 22, True, gameManager),
                               spr.Wall((4, 11), False, 18, True, gameManager),
                               spr.Wall((21, 0), True, 8, True, gameManager),
                               spr.Wall((21, 10), True, 1, True, gameManager))
  box_group = (spr.Box((5, 5), True, gameManager),
               spr.Box((6, 5), True, gameManager))
  door_group = (spr.Door((21, 8), "W", (2, [0, 0]), "key1", gameManager))
  
  enemy_group = (spr.Guard((6, 8), 3, 8, gameManager))
  text_group = (
      spr.text((4, 3), 4, "be careful of the guard", gameManager, 1))

  all_sprites.add(background, wall_group, box_group, gameManager.Player,
                  door_group, enemy_group, text_group)

  scene_1_b = scn.scene(gameManager, all_sprites, (0, 7))

  ##################### c ########################
  all_sprites = pg.sprite.Group()

  wall_group = (spr.Wall((18, 0), False, 1, True, gameManager),
                               spr.Wall((2, 3), True, 3, True, gameManager),
                               spr.Wall((2, 7), True, 4, True, gameManager),
                               spr.Wall((3, 5), False, 3, True, gameManager),
                               spr.Wall((3, 7), False, 3, True, gameManager),
                               spr.Wall((18, 2), False, 1, True, gameManager),
                               spr.Wall((16, 3), True, 1, True, gameManager),
                               spr.Wall((19, 7), True, 3, True, gameManager),
                               spr.Wall((16, 4), False, 4, True, gameManager),
                               spr.Wall((19, 0), True, 3, True, gameManager),
                               spr.Wall((2, 2), False, 15, True, gameManager),
                               spr.Wall((0, 11), False, 20, True, gameManager),
                               spr.Wall((0, 0), False, 17, True, gameManager),
                               spr.Wall((0, 0), True, 12, True, gameManager),
                               spr.Wall((21, 0), True, 7, True, gameManager),
                               spr.Wall((17, 9), False, 2, True, gameManager),
                               spr.Wall((16, 8), True, 2, True, gameManager),
                               spr.Wall((14, 8), False, 2, True, gameManager))

  spike_group = (spr.Spike((21, 7), gameManager),
                                spr.Spike((21, 8), gameManager),
                                spr.Spike((21, 9), gameManager),
                                spr.Spike((21, 10), gameManager),
                                spr.Spike((21, 11), gameManager))
  box_group = (spr.Box((17, 1), False, gameManager),
                              spr.Box((2, 6), True, gameManager))
  rSwitchWall_group = (
      spr.switchWall((2, 1), "red", False, gameManager),
      spr.switchWall((1, 2), "red", False, gameManager))
  bSwitchWall_group = (
      spr.switchWall((20, 6), "blue", False, gameManager),
      spr.switchWall((19, 10), "blue", True, gameManager))
  gSwitchWall_group = (
      spr.switchWall((14, 9), "green", True, gameManager),
      spr.switchWall((14, 10), "green", True, gameManager))
  switch_group = (
      spr.Switch((1, 1), "red", rSwitchWall_group, gameManager),
      spr.Switch((20, 7), "blue", bSwitchWall_group, gameManager),
      spr.Switch((20, 8), "blue", bSwitchWall_group, gameManager),
      spr.Switch((20, 9), "blue", bSwitchWall_group, gameManager),
      spr.Switch((20, 10), "blue", bSwitchWall_group, gameManager),
      spr.Switch((20, 11), "blue", bSwitchWall_group, gameManager),
      spr.Switch((16, 10), "blue", bSwitchWall_group, gameManager),
      spr.Switch((17, 10), "green", gSwitchWall_group, gameManager))

  collectible_group = (
      spr.Collectible((18, 10), "coin", "coin1", gameManager))

  conveyor_group = (spr.Conveyor((15,9), "S", gameManager), spr.Conveyor((15,10), "N", gameManager))

  all_sprites.add(background, wall_group, conveyor_group, rSwitchWall_group, bSwitchWall_group,
                  gSwitchWall_group, switch_group, collectible_group,
                  spike_group, box_group, gameManager.Player)

  scene_1_c = scn.scene(gameManager, all_sprites, (20, 0))

  ##################### d ########################
  all_sprites = pg.sprite.Group()

  killShadow_group = (
      spr.killShadow((4, 0, 18, gameManager.screenHeight // gameManager.tileSize[1]), gameManager),
      spr.killShadow((0, 5, gameManager.screenWidth // gameManager.tileSize [0], 7), gameManager),
      spr.killShadow((2, 2, 1, 1), gameManager),
      spr.killShadow((2, 4, 3, 1), gameManager),
      spr.killShadow((0, 3, 1, 1), gameManager))

  text_group = (spr.text((5, 1), 200, "turn back or be lost to the void", gameManager, 1, (0, 255, 0)))

  all_sprites.add(background, killShadow_group, gameManager.Player, text_group)

  scene_1_d = scn.scene(gameManager, all_sprites, (2, 0))

  sceneParts = [[scene_1_a, scene_1_c], [scene_1_b, scene_1_d]]

  return scn.gameLoop(gameManager, sceneParts, gameManager.sceneIndex[1])
