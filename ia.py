import random

def ia(rect, fruit, joueur):

    a, b = (rect.x + rect.w), (rect.y + rect.h)

    #Collision avec corps

    collision_corps_haut = [joueur.rect.x, joueur.rect.y - 20] in joueur.corps and joueur.direction == 2
    collision_corps_bas = [joueur.rect.x, joueur.rect.y + 20] in joueur.corps and joueur.direction == 3
    collision_corps_droite = [joueur.rect.x + 20, joueur.rect.y] in joueur.corps and joueur.direction == 0
    collision_corps_gauche= [joueur.rect.x - 20, joueur.rect.y] in joueur.corps and joueur.direction == 1

    #Collision Mur

    collision_haut = (joueur.rect.y - 20 < rect.y) and joueur.direction == 2
    collision_bas = (joueur.rect.y + 40 > b) and joueur.direction == 3
    collision_droite = (joueur.rect.x + 40 > a) and joueur.direction == 0
    collision_gauche = (joueur.rect.x - 20 < rect.x) and joueur.direction == 1

    #Gestion collision

    if collision_droite or collision_gauche or collision_corps_droite or collision_corps_gauche:
        if fruit.rect.y > (joueur.rect.y)  and obstruction(joueur, fruit, 3):
            joueur.direction = 3
        else:
            joueur.direction = 2


    if collision_haut or collision_bas or collision_corps_haut or collision_corps_bas:
        if fruit.rect.x > (joueur.rect.x)  and obstruction(joueur, fruit, 0):
            joueur.direction = 0
        else:
            joueur.direction = 1


    #Se deplace vers le fruit
    if fruit.rect.x < (joueur.rect.x-19) and joueur.direction != 0 and obstruction(joueur, fruit, 1):
        if [joueur.rect.x - 20, joueur.rect.y] not in joueur.corps:
            joueur.direction = 1


    elif fruit.rect.x > (joueur.rect.x+19) and joueur.direction != 1 and obstruction(joueur, fruit, 0):
        if [joueur.rect.x + 20, joueur.rect.y] not in joueur.corps:
            joueur.direction = 0
        

    if fruit.rect.y > (joueur.rect.y+19) and joueur.direction != 2 and obstruction(joueur, fruit, 3):
        if [joueur.rect.x, joueur.rect.y + 20] not in joueur.corps:
            joueur.direction = 3


    elif fruit.rect.y < (joueur.rect.y-19) and joueur.direction != 3 and obstruction(joueur, fruit, 2):
        if [joueur.rect.x, joueur.rect.y - 20] not in joueur.corps:
            joueur.direction = 2


#Retourne False si le corps du snake fait obstruction
def obstruction(joueur, fruit, direction):

    for bloc in joueur.corps:

        #Fruit aligné avec le serpent
        fruit_vertical = (joueur.rect.x-20 < fruit.rect.x < joueur.rect.x+20)
        fruit_horizontal = (joueur.rect.y-20 < fruit.rect.y < joueur.rect.y+20)
        #Bloc du corps aligné avec le serpent
        corps_vertical = (joueur.rect.x == bloc[0]) 
        corps_horizontal = (joueur.rect.y == bloc[1])

        #Corps entre serpent et fruit
        fruit_obs_haut = corps_vertical and (fruit.rect.y <= bloc[1] <= joueur.rect.y)
        fruit_obs_bas = corps_vertical and (fruit.rect.y >= bloc[1] >= joueur.rect.y)
        fruit_obs_droite = corps_horizontal and (fruit.rect.x >= bloc[0] >= joueur.rect.x)
        fruit_obs_gauche = corps_horizontal and (fruit.rect.x <= bloc[0] <= joueur.rect.x)

        #bloc du corps en serpent et mur
        corps_obs_haut = corps_vertical and (bloc[1] < joueur.rect.y)
        corps_obs_bas = corps_vertical and (bloc[1] > joueur.rect.y)
        corps_obs_droite = corps_horizontal and (bloc[0] > joueur.rect.x)
        corps_obs_gauche = corps_horizontal and (bloc[0] < joueur.rect.x)

        match direction:

            case 0:
                if corps_obs_droite and (not fruit_obs_droite) and (not fruit_horizontal):
                    return False
                elif fruit_obs_droite:
                    return False

            case 1:
                if corps_obs_gauche and (not fruit_obs_gauche) and (not fruit_horizontal):
                    return False
                elif fruit_obs_gauche:
                    return False

            case 2:
                if corps_obs_haut and (not fruit_obs_haut) and (not fruit_vertical):
                    return False
                elif fruit_obs_haut:
                    return False

            case 3:
                if corps_obs_bas and (not fruit_obs_bas) and (not fruit_vertical):
                    return False
                elif fruit_obs_bas:
                    return False

    return True