import random

def ia(rect, fruit, joueur):

    a, b = (rect.x + rect.w), (rect.y + rect.h)

    #Collision avec corps
    if [joueur.rect.x + 20, joueur.rect.y] in joueur.corps and joueur.direction == 0:
        print('Collision Corps Droite')

    if [joueur.rect.x - 20, joueur.rect.y] in joueur.corps and joueur.direction == 1:
        print('Collision Corps Gauche')
    
    if [joueur.rect.x, joueur.rect.y - 20] in joueur.corps and joueur.direction == 2:
        print('Collision Corps Haut')

    if [joueur.rect.x, joueur.rect.y + 20] in joueur.corps and joueur.direction == 3:
        print('Collision Corps Bas')

    #Collision Mur

    collision_haut = (joueur.rect.y - 20 < rect.y) and joueur.direction == 2
    collision_bas = (joueur.rect.y + 40 > b) and joueur.direction == 3
    collision_droite = (joueur.rect.x + 40 > a) and joueur.direction == 0
    collision_gauche = (joueur.rect.x - 20 < rect.x) and joueur.direction == 1

    if collision_droite or collision_gauche:
        if fruit.rect.y > (joueur.rect.y):
            joueur.direction = 3
        else:
            joueur.direction = 2


    if collision_haut or collision_bas:
        if fruit.rect.x > (joueur.rect.x):
            joueur.direction = 0
        else:
            joueur.direction = 1


    #Se deplace vers le fruit
    if fruit.rect.x < (joueur.rect.x-19) and joueur.direction != 0 and chemin(joueur, fruit, 1):
        if [joueur.rect.x - 20, joueur.rect.y] not in joueur.corps:
            joueur.direction = 1


    elif fruit.rect.x > (joueur.rect.x+19) and joueur.direction != 1 and chemin(joueur, fruit, 0):
        if [joueur.rect.x + 20, joueur.rect.y] not in joueur.corps:
            joueur.direction = 0
        

    if fruit.rect.y > (joueur.rect.y+19) and joueur.direction != 2 and chemin(joueur, fruit, 3):
        if [joueur.rect.x, joueur.rect.y + 20] not in joueur.corps:
            joueur.direction = 3


    elif fruit.rect.y < (joueur.rect.y-19) and joueur.direction != 3 and chemin(joueur, fruit, 2):
        if [joueur.rect.x, joueur.rect.y - 20] not in joueur.corps:
            joueur.direction = 2



def chemin(joueur, fruit, direction):

    for bloc in joueur.corps:

        vertical = (joueur.rect.x-19 < fruit.rect.x < joueur.rect.x+19) and (joueur.rect.x-19 < bloc[0] < joueur.rect.x+19) 
        horizontal = (joueur.rect.y-19 < fruit.rect.y < joueur.rect.y+19) and (joueur.rect.y-19 < bloc[1] < joueur.rect.y+19)

        bloc_haut = vertical and (fruit.rect.y <= bloc[1]+40 <= joueur.rect.y)
        bloc_bas = vertical and (fruit.rect.y >= bloc[1]-40 >= joueur.rect.y)
        bloc_droite = horizontal and (fruit.rect.x >= bloc[0]-40 >= joueur.rect.x)
        bloc_gauche = horizontal and (fruit.rect.x <= bloc[0]+40 <= joueur.rect.x)

        if bloc_haut and direction == 2:
            return False
            
        if bloc_bas and direction == 3:
            return False

        if bloc_droite and direction == 0:
            return False

        if bloc_gauche and direction == 1:
            return False

    return True