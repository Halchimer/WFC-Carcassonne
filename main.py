import pygame
import json
import os
import random
import time
from datetime import date

width,height = 900,900
tilew,tileh = 16,16
tilesrules = {}
with open("entropy_rules.json", 'r') as data :
    tilesrules = json.loads(data.read())

screenimg = pygame.Surface((int(width/tilew)*tilew, int(height/tileh)*tileh))

tilesassets = {}
for tile in tilesrules["tiles"] :
    tilesassets[str(tile)] = (pygame.transform.scale(pygame.image.load(os.path.join('assets', f'{tile}.png')), (int(width/tilew), int(height/tileh))))

background_image = pygame.transform.scale(pygame.image.load("background.jpg"), (int(height/tileh)*tileh, int(height/tileh)*tileh))
# grid

collapsedtiles = []
tilegrid = []
for x in range(tilew) :
    tilegrid.append([])
    collapsedtiles.append([])
    for y in range(tileh) :
        tilegrid[x].append([tile for tile in tilesrules["tiles"]])
        collapsedtiles[x].append(False)

def collapse(indx, indy, value) :
    tilegrid[indx][indy] = [value]
    collapsedtiles[indx][indy] = True

def reduceentropy(indx, indy):
    if indx-1 >= 0 and indx-1 < tileh and len(tilegrid[indx-1][indy]) != 0:
        if collapsedtiles[indx-1][indy] == True : tilegrid[indx][indy] = [x for x in tilegrid[indx][indy] if x in tilesrules["faces-tile"][str(tilesrules["tile-faces"][str(tilegrid[indx-1][indy][0])][1])]['3']]
    if indx+1 < tilew and indx+1 >= 0 and len(tilegrid[indx+1][indy]) != 0: 
        if collapsedtiles[indx+1][indy] == True : tilegrid[indx][indy] = [x for x in tilegrid[indx][indy] if x in tilesrules["faces-tile"][str(tilesrules["tile-faces"][str(tilegrid[indx+1][indy][0])][3])]['1']]
    if indy-1 >= 0 and indy-1 < tileh and len(tilegrid[indx][indy-1]) != 0: 
        if collapsedtiles[indx][indy-1] == True : tilegrid[indx][indy] = [x for x in tilegrid[indx][indy] if x in tilesrules["faces-tile"][str(tilesrules["tile-faces"][str(tilegrid[indx][indy-1][0])][2])]['0']]
    if indy+1 < tileh and indy+1 >= 0 and len(tilegrid[indx][indy+1]) != 0: 
        if collapsedtiles[indx][indy+1] == True : tilegrid[indx][indy] = [x for x in tilegrid[indx][indy] if x in tilesrules["faces-tile"][str(tilesrules["tile-faces"][str(tilegrid[indx][indy+1][0])][0])]['2']] 


# pygame setup
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

#Wave Funciton Collapse Algorithme
collapse(random.randint(0, tilew-1), random.randint(0, tileh-1), random.choice(tilesrules["tiles"]))

for i in range(int(width/(int(height/tileh)*tileh))) :
    screenimg.blit(background_image,(i*(int(height/tileh)*tileh), 0))

def gen_image():
    

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return 0

    lastentropy = len(tilesrules["tiles"])
    lastco = (0, 0)



    for x in range(tilew) :
        for y in range(tileh):
            reduceentropy(x, y)
            

    for x in range(tilew) :
        for y in range(tileh):
            if len(tilegrid[x][y]) <= lastentropy and collapsedtiles[x][y] == False:
                lastentropy = len(tilegrid[x][y])
                lastco = (x, y)
            
            if len(tilegrid[x][y]) <= 0 :
                collapsedtiles[x][y] = True
                #return 0
            



    if len(tilegrid[lastco[0]][lastco[1]]) > 0 and collapsedtiles[lastco[0]][lastco[1]] == False : 
        choicelist = []
        for el in tilegrid[lastco[0]][lastco[1]] :
            for i in range(tilesrules["weight"][str(el)]) :
                choicelist.append(el)
        collapse(lastco[0], lastco[1], random.choice(choicelist))

        screenimg.blit(tilesassets[str(tilegrid[lastco[0]][lastco[1]][0])], (int(width/tilew)*lastco[0], int(height/tileh)*lastco[1]))
        screen.blit(screenimg, (0, 0))
        lastentropy = len(tilesrules["tiles"])


            
    for x in range(tilew) :
            for y in range(tileh):
                if collapsedtiles[x][y] == True and len(tilegrid[x][y]) > 0:
                    screenimg.blit(tilesassets[str(tilegrid[x][y][0])], (int(width/tilew)*x, int(height/tileh)*y))

    return 1

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    
    screen.blit(screenimg, (0, 0))

    # RENDER YOUR GAME HERE

    if gen_image() == 0 :
        for i in range(int(width/(int(height/tileh)*tileh))) :
            screenimg.blit(background_image,(i*(int(height/tileh)*tileh), 0))
        collapsedtiles = []
        tilegrid = []
        for x in range(tilew) :
            tilegrid.append([])
            collapsedtiles.append([])
            for y in range(tileh) :
                tilegrid[x].append([tile for tile in tilesrules["tiles"]])
                collapsedtiles[x].append(False)
        collapse(random.randint(0, tilew-1), random.randint(0, tileh-1), random.choice(tilesrules["tiles"]))
        

        
    # flip() the display to put your work on screen
    pygame.display.flip()

    #time.sleep(1)

    clock.tick(120)  # limits FPS to 60

pygame.image.save(screenimg, f'render{date.today()}{random.randint(0,1000)}.png')

pygame.quit()