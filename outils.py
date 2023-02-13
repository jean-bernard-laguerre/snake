import pygame
import random
import time
import json
from ia import *

TAILLE_SNAKE = 20

class Snake():

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TAILLE_SNAKE, TAILLE_SNAKE)

        #Liste contenant les coordonnés du corps du serpent
        self.corps = [[x-TAILLE_SNAKE,y],[x-40,y],[x-60,y]]
        self.direction = 0

    def affichage(self, surface, rect):
        
        a, b = (rect.x + rect.w), (rect.y + rect.h)
        touche = pygame.key.get_pressed()
        
        #Changement de direction avec les fleches
        if touche[pygame.K_RIGHT] and self.direction != 1:
            self.direction = 0
        if touche[pygame.K_LEFT] and self.direction != 0:
            self.direction = 1
        if touche[pygame.K_UP] and self.direction != 3:
            self.direction = 2
        if touche[pygame.K_DOWN] and self.direction != 2:
            self.direction = 3

        #Boucle mettant a jour la position de chaque segment du corps du serpent
        i = len(self.corps)-1
        while i >= 0:

            if i == 0:
                self.corps[i][0] = self.rect.x
                self.corps[i][1] = self.rect.y
            else:
                self.corps[i][0] = self.corps[i-1][0]
                self.corps[i][1] = self.corps[i-1][1]

            pygame.draw.rect(surface, 'red', pygame.Rect(self.corps[i][0], self.corps[i][1], TAILLE_SNAKE, TAILLE_SNAKE))
            
            i-=1
        
        #Avance automatiquement dans la direction actuelle
        match self.direction:
            case 0:
                if self.rect.x + self.rect.width < a:
                    self.rect.x += TAILLE_SNAKE
            case 1:
                if self.rect.x > rect.x:
                    self.rect.x -= TAILLE_SNAKE
            case 2:
                if self.rect.y > rect.y:
                    self.rect.y -= TAILLE_SNAKE
            case 3:
                if self.rect.y + self.rect.height < b:
                    self.rect.y += TAILLE_SNAKE

        #Retourne true en cas de collision avec le corps du serpent
        for x in self.corps:
            if self.rect.colliderect(pygame.Rect(x[0], x[1], TAILLE_SNAKE, TAILLE_SNAKE)):
                return True

        pygame.draw.rect(surface, 'brown', self.rect)
        time.sleep(.07)

        return False


class Fruit():
    def __init__(self, x, y) -> None:
        self.rect = pygame.Rect(x, y, TAILLE_SNAKE, TAILLE_SNAKE)

    def affichage(self, surface):
        pygame.draw.rect(surface, 'green', self.rect)


class Jeu():

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 600, 560)
        self.joueur = Snake(self.rect.x+100, self.rect.y+100)
        self.pomme = Fruit(self.rect.x+250, self.rect.y+400)
        self.auto = 0
        self.score = 0

    def affichage(self, surface):

        pygame.draw.rect(surface, 'blue', self.rect, 2)

        #L'ia choisis la direction du serpent lorsqu'elle est active
        if self.auto == 1:
            ia(self.rect, self.pomme, self.joueur)

        if self.joueur.affichage(surface, self.rect):
            return True

        self.pomme.affichage(surface)

        #Lorsque le serpent et le fruit entre en contact, ajoute 1 point allonge le serpent et change la position de la pomme
        if self.pomme.rect.colliderect(self.joueur.rect):

            self.joueur.corps.insert(0,[self.joueur.rect.x, self.joueur.rect.y])
            self.pomme.rect.x = random.randint(self.rect.x, self.rect.w)
            self.pomme.rect.y = random.randint(self.rect.y, self.rect.h)
            self.score += 1
            
        return False
    

class Bouton():
    def __init__(self, message, x, y, police):
        self.texte = police.render(message, 1, 'black')
        self.rect = self.texte.get_rect()
        self.rect.topleft = (x, y)
        self.rect.w = self.texte.get_width()+20
        self.rect.h = self.texte.get_height()+20

    #Affiche le bouton retourne True lorsque l'on clique a l'interieur
    def affichage(self, surface):
        
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):

            if (pygame.mouse.get_pressed()[0] == 1):
                action = True

        pygame.draw.rect(surface, 'red', self.rect, 2)
        surface.blit(self.texte, ( self.rect.x+10, self.rect.y+10))

        return action

#Ajoute le score dans scores.json
def enregistrer(score):

    f = open("scores.json", "r+")
    scores = json.load(f)

    if "Scores" not in scores:
        scores[f"Scores"] = []

    if score > 0:
        scores["Scores"].append(score)

    f.seek(0)
    json.dump(scores, f, indent=4)

    f.close()

#Recupere les dix meilleurs scores
def recuperer():

    f = open("scores.json", "r+")
    scores = json.load(f)

    f.close()
    
    return sorted(scores["Scores"], reverse=True)[:10]