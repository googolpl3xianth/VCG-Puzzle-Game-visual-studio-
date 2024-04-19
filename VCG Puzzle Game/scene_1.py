from PIL import Image
import pygame as pg
import sprites as spr
import scenes as scn


def main(gameManager):  # first scene

  pg.display.set_caption('scene_1')
  ##################### a ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((9, 1), gameManager)
  background = spr.Background("sprites/BGs/edge.png", gameManager)

  mentorImage = Image.open("sprites/NPCs/Mentor.png").crop((100, 80, 332, 590)).save("sprites/NPCs/NMentor.png")
  mentorImage = pg.transform.scale(pg.image.load("sprites/NPCs/NMentor.png").convert_alpha(), (int(gameManager.tileSize[0]), int(gameManager.tileSize[1]) * 2))
  mentor = spr.Sprite(mentorImage, (2, 3.5), gameManager, True)

  text_group = (
      spr.text((3, 3), 4, "Use 'SPACE' to enter shadow mode", gameManager),
      spr.text((11, 1), 5, "Press 'R' to reset", gameManager))

  wall_group = (spr.Wall((6, 0), True, 12, False, gameManager),
                spr.Wall((11, 2), False, 1, True, gameManager),
                spr.Wall((12, 4), False, 10, True, gameManager),
                spr.Wall((10, 0), True, 5, True, gameManager),
                spr.Wall((21, 0), True, 4, True, gameManager),
                spr.Wall((0, 11), False, 22, True, gameManager),
                spr.Wall((0, 0), False, 22, True, gameManager),
                spr.Wall((0, 0), True, 12, True, gameManager))
  box_group = (spr.Box((11, 4), False, gameManager))
  
  conveyor = [spr.Conveyor((12, 1), "W", gameManager)]

  collectible_group = (
      spr.Collectible((15, 2), "key", "key1", gameManager))
  
  

  all_sprites.add(background, wall_group, conveyor, box_group, collectible_group, mentor,
                  gameManager.Player, text_group, cage)

  scene_1_a = scn.scene(gameManager, all_sprites)

  ######################### b #######################

  all_sprites = pg.sprite.Group()
  cage = spr.Cage((1, 1), gameManager)
  wall_group = (spr.Wall((4, 5), True, 6, True, gameManager),
                spr.Wall((7, 7), False, 14, True, gameManager),
                spr.Wall((7, 1), True, 6, True, gameManager),
                spr.Wall((0, 4), False, 1, True, gameManager),
                spr.Wall((0, 0), True, 4, True, gameManager),
                spr.Wall((0, 0), False, 8, True, gameManager),
                spr.Wall((4, 11), False, 18, True, gameManager),
                spr.Wall((21, 7), True, 1, True, gameManager),
                spr.Wall((21, 10), True, 1, True, gameManager))
  kill_shadow = [spr.killShadow((8, 0, 14, 7), gameManager)]
  box_group = (spr.Box((5, 5), True, gameManager),
               spr.Box((6, 5), True, gameManager))
  door_group = (spr.Door((21, 8), "W", (2, [0, 0]), "key1", gameManager))
  
  enemy_group = (spr.Guard((6, 8), 2, 8, gameManager))
  text_group = (
      spr.text((4, 3), 12, "be careful of the guard", gameManager),
      spr.text((4, 2), 12, "press SHIFT to sprint", gameManager))

  all_sprites.add(background, kill_shadow, wall_group, box_group, gameManager.Player,
                  door_group, enemy_group, text_group, cage)

  scene_1_b = scn.scene(gameManager, all_sprites)

  ##################### c ########################
  all_sprites = pg.sprite.Group()
  cage = spr.Cage((15, 4), gameManager)
  wall_group = (
                spr.Wall((6, 7.5), True, 1, True, gameManager),
                spr.Wall((6, 9.5), True, 2, True, gameManager),
                spr.Wall((18, 0), False, 1, True, gameManager),
                spr.Wall((2, 3), True, 3, True, gameManager),
                spr.Wall((2, 7), True, 4, True, gameManager),
                spr.Wall((3, 5), False, 4, True, gameManager),
                spr.Wall((3, 7), False, 4, True, gameManager),
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
  rSwitchWall_group = [
      spr.switchWall((2, 1), "red", False, gameManager),
      spr.switchWall((1, 2), "red", False, gameManager)]
  bSwitchWall_group = [
      spr.switchWall((20, 6), "blue", False, gameManager),
      spr.switchWall((19, 10), "blue", True, gameManager)]
  gSwitchWall_group = [
      spr.switchWall((14, 9), "green", True, gameManager),
      spr.switchWall((14, 10), "green", True, gameManager)]
  switch_group = (
      spr.Switch((1, 1), rSwitchWall_group, gameManager),
      spr.Switch((20, 7), bSwitchWall_group, gameManager),
      spr.Switch((20, 8), bSwitchWall_group, gameManager),
      spr.Switch((20, 9), bSwitchWall_group, gameManager),
      spr.Switch((20, 10), bSwitchWall_group, gameManager),
      spr.Switch((20, 11), bSwitchWall_group, gameManager),
      spr.Switch((16, 10), bSwitchWall_group, gameManager),
      spr.Switch((17, 10), gSwitchWall_group, gameManager))

  collectible_group = (
      spr.Collectible((4, 9), "coin", "coin1", gameManager))

  conveyor_group = (spr.Conveyor((15, 9), "S", gameManager), spr.Conveyor((15,10), "N", gameManager))

  all_sprites.add(background, wall_group, conveyor_group, rSwitchWall_group, bSwitchWall_group,
                  gSwitchWall_group, switch_group, collectible_group,
                  spike_group, box_group, gameManager.Player, cage)

  scene_1_c = scn.scene(gameManager, all_sprites)

  ##################### d ########################
  all_sprites = pg.sprite.Group()

  killShadow_group = (
      spr.killShadow((4, 0, 18, gameManager.screenHeight // gameManager.tileSize[1]), gameManager),
      spr.killShadow((0, 5, gameManager.screenWidth // gameManager.tileSize [0], 7), gameManager),
      spr.killShadow((2, 2, 1, 1), gameManager),
      spr.killShadow((2, 4, 3, 1), gameManager),
      spr.killShadow((0, 3, 1, 1), gameManager))
  
  text_group = (spr.text((2, 1), 12, "turn back or be lost to the void", gameManager))

  all_sprites.add(background, killShadow_group, gameManager.Player, text_group)

  scene_1_d = scn.scene(gameManager, all_sprites)

  sceneParts = [[scene_1_a, scene_1_c], [scene_1_b, scene_1_d]]

  return scn.gameLoop(gameManager, sceneParts, gameManager.sceneIndex[1])
