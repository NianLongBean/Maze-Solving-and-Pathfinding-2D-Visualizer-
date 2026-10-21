import pygame as pg

pg.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Sprite_test')
BG = (50,50,50)

sprite_sheet_image_idle = pg.image.load("assets/Soldier_Idle.png").convert_alpha()
sprite_sheet_image_walk = pg.image.load("assets/Soldier_Walk.png").convert_alpha()


def get_image(sheet, width, height):
    image = pg.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0,0), (0, 0, width, height))

    return image

frame_0 = get_image(sprite_sheet_image_walk, 100, 100)

run = True 
while run:

    screen.fill(BG)

    #display image
    # screen.blit(sprite_sheet_image_idle, (0,0))
    # screen.blit(sprite_sheet_image_walk, (50,50))

    #show frame image
    screen.blit(frame_0,(0,0))

    #event handler 
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.update()

pg.quit()