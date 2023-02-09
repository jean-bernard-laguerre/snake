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
    if joueur.rect.x + 20 > a and joueur.direction == 0:
        print('Collision Mur Droite')

    if joueur.rect.x - 20 < rect.x and joueur.direction == 1:
        print('Collision Mur Gauche')

    if joueur.rect.y - 20 < rect.y and joueur.direction == 2:
        print('Collision Mur Haut')

    if joueur.rect.y + 20 > b and joueur.direction == 3:
        print('Collision Mur Bas')

    #Se deplace vers le fruit
    if fruit.rect.x < (joueur.rect.x-10) and joueur.direction != 0:
        joueur.direction = 1
    elif fruit.rect.x > (joueur.rect.x+10) and joueur.direction != 1:
        joueur.direction = 0
    elif fruit.rect.y > (joueur.rect.y+10) and joueur.direction != 2:
        joueur.direction = 3
    elif fruit.rect.y < (joueur.rect.y-10) and joueur.direction != 3:
        joueur.direction = 2