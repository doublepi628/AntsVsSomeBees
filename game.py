import sys
from objects import *
from animate import *

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('AntsVsSomeBees')
pygame.display.set_icon(pygame.image.load('images/logo.png'))

# initialize clock
clock = pygame.time.Clock()

# load background images
start_background = pygame.transform.scale(pygame.image.load('images/splash.png'), (1280, 720))
game_background = pygame.transform.scale(pygame.image.load("images/main-background.png"), (1280, 720))
help1_background = pygame.transform.scale(pygame.image.load('images/help1.png'), (1280, 720))
help2_background = pygame.transform.scale(pygame.image.load('images/help2.png'), (1280, 720))

# load ground images
groundlist = [pygame.transform.scale(pygame.image.load("images/tiles/ground/" + str(i + 1) + ".png"),
                                     (60, 60)) for i in range(3)]
skylist = [pygame.transform.scale(pygame.image.load("images/tiles/sky/" + str(i + 1) + ".png"),
                                  (60, 60)) for i in range(3)]
imagemap = [[[random.choice(skylist), random.choice(groundlist)] for j in range(5)] for i in range(10)]

xindex, yindex = [60, 130, 200, 270, 340, 410, 480, 550, 620, 690], [150, 260, 370, 480, 590]
beesyindex = [800, 870, 940, 1010, 1080, 1150]
xlen, ylen = len(xindex), len(yindex)

game_mode = 0
game_difficulty = 1
all_difficulty = ['Easy', 'Medium', 'Hard', 'Challenge']
tot_num = [1, 2, 3, 3]  # bees total num (*30)
num_per_time = [{6: 1, 12: 2, 14: 3, 16: 3, 18: 5, 20: 5, 22: 5, 23: 6},
                {6: 1, 12: 2, 15: 3, 18: 3, 21: 4, 24: 5, 26: 5, 28: 5, 29: 5, 30: 5, 31: 5, 32: 5, 33: 2, 34: 5,
                 35: 5},
                {5: 1, 10: 2, 14: 3, 17: 4, 23: 5, 24: 5, 25: 5, 26: 5, 30: 10, 31: 10, 32: 10, 33: 10, 34: 10,
                 35: 10},
                {5: 1, 10: 2, 14: 3, 17: 4, 18: 5, 19: 5, 20: 5, 25: 5, 26: 5, 27: 5, 28: 5, 29: 5, 30: 5, 31: 5,
                 36: 10, 37: 10, 38: 10}]

# load font
font = pygame.font.Font('font/Pixeltype.ttf', 55)
font_num = pygame.font.Font('font/Pixeltype.ttf', 36)
font_little = pygame.font.Font('font/Pixeltype.ttf', 24)
guide_text = ShiningText(font, "Press SPACE to continue...", (640, 630))
guide_text1 = ShiningText(font, "Press ENTER to switch difficulty...", (640, 590))
guide_text2 = ShiningText(font, "Press TAB to find some help...", (640, 670))

# initialize shining objects
shining_objects = ShiningObjects()
shining_objects.add_object(guide_text)
shining_objects.add_object(guide_text1)
shining_objects.add_object(guide_text2)

# initialize fading objects
fading_objects = FadingObjects()

# initialize music
pygame.mixer.init()
pygame.mixer.music.load("music/start.mp3")
pygame.mixer.music.play(-1)

# initialize ants
have_laser_ant = 0
ants_types = [HarvesterAnt(), ThrowerAnt(), BodyguardAnt(), TankAnt(), FireAnt(), HungryAnt(), WallAnt(), NinjaAnt(),
              QueenAnt(), SlowThrower()]
ants_images = []
for type0 in ants_types:
    ants_images.append(pygame.transform.scale(pygame.image.load("images/insects/ant_" + type0.name + ".gif"), (70, 70)))
ants_types.append(AntRemover())
ants_images.append(pygame.transform.scale(pygame.image.load("images/insects/ant_remover.png"), (70, 70)))

gamestate = 2
mode0_mode = 0
GAMESTATE_LOOP = pygame.USEREVENT + 1
pygame.time.set_timer(GAMESTATE_LOOP, 2000)

while True:
    # checking events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.key == pygame.K_SPACE and game_mode == 0 and mode0_mode == 0:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("music/gaming.mp3")
                pygame.mixer.music.play(-1)
                gamestate = GameState(ants_types, yindex, xindex, beesyindex,
                                      tot_num[game_difficulty], num_per_time[game_difficulty])
                game_mode = 1
                shining_objects.remove_object(guide_text)
                shining_objects.remove_object(guide_text1)
                shining_objects.remove_object(guide_text2)
            elif event.key == pygame.K_RETURN and game_mode == 0 and mode0_mode == 0:
                game_difficulty = (game_difficulty + 1) % 4
            elif event.key == pygame.K_TAB and game_mode == 0 and mode0_mode == 0:
                mode0_mode = 1
                shining_objects.remove_object(guide_text)
                shining_objects.remove_object(guide_text1)
            elif event.key == pygame.K_TAB and game_mode == 0 and mode0_mode == 1:
                mode0_mode = 2
            elif event.key == pygame.K_TAB and game_mode == 0 and mode0_mode == 2:
                mode0_mode = 0
                shining_objects.add_object(guide_text)
                shining_objects.add_object(guide_text1)
            elif event.key == pygame.K_SPACE and (game_mode == 2 or game_mode == 3):
                game_mode = 0
                pygame.mixer.music.stop()
                pygame.mixer.music.load("music/start.mp3")
                pygame.mixer.music.play(-1)
                shining_objects = ShiningObjects()
                shining_objects.add_object(guide_text)
                shining_objects.add_object(guide_text1)
                shining_objects.add_object(guide_text2)
                fading_objects = FadingObjects()
            elif event.key == pygame.K_0 and game_mode == 1:
                for i in range(0, xlen):
                    if xindex[i] <= mouse_x <= xindex[i] + 60:
                        for j in range(0, ylen):
                            if yindex[j] <= mouse_y <= yindex[j] + 100:
                                gamestate.add_ants(j, i, HarvesterAnt())
            elif event.key == pygame.K_1 and game_mode == 1:
                for i in range(0, xlen):
                    if xindex[i] <= mouse_x <= xindex[i] + 60:
                        for j in range(0, ylen):
                            if yindex[j] <= mouse_y <= yindex[j] + 100:
                                gamestate.add_ants(j, i, ThrowerAnt())
            elif event.key == pygame.K_2 and game_mode == 1:
                for i in range(0, xlen):
                    if xindex[i] <= mouse_x <= xindex[i] + 60:
                        for j in range(0, ylen):
                            if yindex[j] <= mouse_y <= yindex[j] + 100:
                                gamestate.add_ants(j, i, BodyguardAnt())
            elif event.key == pygame.K_3 and game_mode == 1:
                for i in range(0, xlen):
                    if xindex[i] <= mouse_x <= xindex[i] + 60:
                        for j in range(0, ylen):
                            if yindex[j] <= mouse_y <= yindex[j] + 100:
                                gamestate.add_ants(j, i, TankAnt())
            elif event.key == pygame.K_4 and game_mode == 1:
                for i in range(0, xlen):
                    if xindex[i] <= mouse_x <= xindex[i] + 60:
                        for j in range(0, ylen):
                            if yindex[j] <= mouse_y <= yindex[j] + 100:
                                gamestate.add_ants(j, i, FireAnt())
            elif event.key == pygame.K_5 and game_mode == 1:
                for i in range(0, xlen):
                    if xindex[i] <= mouse_x <= xindex[i] + 60:
                        for j in range(0, ylen):
                            if yindex[j] <= mouse_y <= yindex[j] + 100:
                                gamestate.add_ants(j, i, HungryAnt())
            elif event.key == pygame.K_6 and game_mode == 1:
                for i in range(0, xlen):
                    if xindex[i] <= mouse_x <= xindex[i] + 60:
                        for j in range(0, ylen):
                            if yindex[j] <= mouse_y <= yindex[j] + 100:
                                gamestate.add_ants(j, i, WallAnt())
            elif event.key == pygame.K_7 and game_mode == 1:
                for i in range(0, xlen):
                    if xindex[i] <= mouse_x <= xindex[i] + 60:
                        for j in range(0, ylen):
                            if yindex[j] <= mouse_y <= yindex[j] + 100:
                                gamestate.add_ants(j, i, NinjaAnt())
            elif event.key == pygame.K_8 and game_mode == 1:
                for i in range(0, xlen):
                    if xindex[i] <= mouse_x <= xindex[i] + 60:
                        for j in range(0, ylen):
                            if yindex[j] <= mouse_y <= yindex[j] + 100:
                                gamestate.add_ants(j, i, QueenAnt())
            elif event.key == pygame.K_9 and game_mode == 1:
                for i in range(0, xlen):
                    if xindex[i] <= mouse_x <= xindex[i] + 60:
                        for j in range(0, ylen):
                            if yindex[j] <= mouse_y <= yindex[j] + 100:
                                gamestate.add_ants(j, i, SlowThrower())
            elif event.key == pygame.K_BACKSPACE and game_mode == 1:
                for i in range(0, xlen):
                    if xindex[i] <= mouse_x <= xindex[i] + 60:
                        for j in range(0, ylen):
                            if yindex[j] <= mouse_y <= yindex[j] + 100:
                                gamestate.remove_ants(j, i)
            elif (event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL) and game_mode == 1 and have_laser_ant:
                for i in range(0, xlen):
                    if xindex[i] <= mouse_x <= xindex[i] + 60:
                        for j in range(0, ylen):
                            if yindex[j] <= mouse_y <= yindex[j] + 100:
                                gamestate.add_ants(j, i, LaserAnt())
        elif event.type == GAMESTATE_LOOP and game_mode == 1:
            gamestate.loop()

    if game_mode == 0 and mode0_mode == 0:
        screen.blit(start_background, (0, 0))
        render = font.render("Difficulty: " + all_difficulty[game_difficulty], True, (255, 255, 255))
        rect = render.get_rect()
        rect.center = (640, 550)
        screen.blit(render, rect)
    elif game_mode == 0 and mode0_mode == 1:
        screen.blit(help1_background, (0, 0))
    elif game_mode == 0 and mode0_mode == 2:
        screen.blit(help2_background, (0, 0))
    elif game_mode == 1:
        screen.blit(game_background, (0, 0))
        for i in range(xlen):
            for j in range(ylen):
                screen.blit(imagemap[i][j][0], (xindex[i], yindex[j]))
                screen.blit(imagemap[i][j][1], (xindex[i], yindex[j] + 40))
        x, i = 50, 0
        for i in range(10):
            screen.blit(ants_images[i], (x, 50))
            screen.blit(font_little.render(str(i), True, (255, 255, 255)), (x - 5, 50))
            screen.blit(font_little.render(" cost:" + str(ants_types[i].food_cost),
                                           True, (255, 255, 255)), (x - 5, 115))
            x += 70
            i += 1
        screen.blit(ants_images[i], (x, 50))
        screen.blit(font_little.render("backspace", True, (255, 255, 255)), (x - 5, 50))
        screen.blit(font_little.render(" cost:" + str(ants_types[i].food_cost), True, (255, 255, 255)), (x - 5, 115))
        if have_laser_ant == 1:
            x += 70
            i += 1
            screen.blit(ants_images[i], (x, 50))
            screen.blit(font_little.render("     ctrl", True, (255, 255, 255)), (x - 5, 50))
            screen.blit(font_little.render(" cost:" + str(ants_types[i].food_cost), True, (255, 255, 255)),
                        (x - 5, 115))
        for i in range(ylen):
            for j in range(xlen):
                ant = gamestate.places[i][j].ant
                if ant is not None:
                    if ant.is_container:
                        if ant.ant_contained is not None:
                            image_name = "images/insects/ant_" + ant.ant_contained.name + ".gif"
                            screen.blit(pygame.transform.scale(pygame.image.load(image_name),
                                                               (70, 70)), (xindex[j], yindex[i]))
                        screen.blit(pygame.transform.scale(pygame.image.load("images/insects/ant_" + ant.name + ".gif"),
                                                           (70, 70)), (xindex[j], yindex[i]))
                    else:
                        screen.blit(pygame.transform.scale(pygame.image.load("images/insects/ant_" + ant.name + ".gif"),
                                                           (70, 70)), (xindex[j], yindex[i]))
        for bee in gamestate.beehive.bees:
            bee.update()
            screen.blit(pygame.transform.scale(pygame.image.load("images/insects/bee.gif"), (70, 70)), (bee.y, bee.x))
        for bee in gamestate.activebees:
            if bee.health <= 0:
                fading_objects.add_object(FadingImage("images/insects/bee.gif", (bee.y, bee.x), (70, 70)))
                gamestate.activebees.remove(bee)
            bee.update()
            screen.blit(pygame.transform.scale(pygame.image.load("images/insects/bee.gif"), (70, 70)), (bee.y, bee.x))
        for leaf in gamestate.leafs:
            if leaf.current == leaf.end:
                gamestate.leafs.remove(leaf)
            else:
                leaf.update()
                screen.blit(pygame.transform.scale(pygame.image.load("images/leaf/" + leaf.type + ".png"),
                                                   (40, 40)), (leaf.current[1], leaf.current[0]))
        for effect in gamestate.effects:
            if effect.time == 0:
                gamestate.effects.remove(effect)
            else:
                effect.update()
                screen.blit(pygame.transform.scale(pygame.image.load("images/leaf/" + effect.type + ".png"),
                                                   (70, 70)), (effect.position[1], effect.position[0]))
        screen.blit(font.render("food:" + str(gamestate.food), True, (255, 255, 255)), (950, 70))
        game_mode = gamestate.gamemode
    elif game_mode >= 2:
        transparent_image = pygame.Surface((1280, 720), pygame.SRCALPHA)
        pygame.draw.rect(transparent_image, (0, 0, 0, 150), transparent_image.get_rect())
        screen.blit(game_background, (0, 0))
        screen.blit(transparent_image, (0, 0))
        if game_mode == 2 and game_difficulty == 3:
            screen.blit(font.render("You win!", True, (255, 255, 255)), (570, 250))
            screen.blit(pygame.transform.scale(pygame.image.load("images/insects/ant_laser.gif"),
                                               (100, 100)), (575, 300))
            screen.blit(font.render("A special gift for you!", True, (255, 255, 255)), (470, 450))
            if have_laser_ant == 0:
                ants_types.append(LaserAnt())
                ants_images.append(pygame.transform.scale(pygame.image.load("images/insects/ant_laser.gif"), (70, 70)))
                have_laser_ant = 1
        elif game_mode == 2:
            screen.blit(font.render("You win!", True, (255, 255, 255)), (570, 340))
        elif game_mode == 3:
            screen.blit(font.render("You lost...", True, (255, 255, 255)), (565, 340))
        if len(shining_objects.all_objects) == 0:
            shining_objects.add_object(guide_text)
    shining_objects.draw_all(screen)
    fading_objects.draw_all(screen)
    pygame.display.flip()
    clock.tick(60)
