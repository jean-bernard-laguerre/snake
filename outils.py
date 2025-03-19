import pygame
import random
import time
import json
from ia import *

TAILLE_SNAKE = 20

class Snake():

    def __init__(self, x, y):
        self.image = pygame.image.load("images/assets/spaceship.png")
        self.image = pygame.transform.scale(self.image, (TAILLE_SNAKE, TAILLE_SNAKE))

        self.corpsVert = pygame.image.load("images/assets/trailVertical.png")
        self.corpsVert = pygame.transform.scale(self.corpsVert, (TAILLE_SNAKE, TAILLE_SNAKE))

        self.corpsHor = pygame.image.load("images/assets/trail.png")
        self.corpsHor = pygame.transform.scale(self.corpsHor, (TAILLE_SNAKE, TAILLE_SNAKE))
        
        self.corpsCoin = pygame.image.load("images/assets/trailCorner.png")
        self.corpsCoin = pygame.transform.scale(self.corpsCoin, (TAILLE_SNAKE, TAILLE_SNAKE))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        #Liste contenant les coordonnés du corps du serpent
        self.corps = [[x-TAILLE_SNAKE,y],[x-(TAILLE_SNAKE*2),y],[x-(TAILLE_SNAKE*3),y]]
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

            i-=1
        

        i = len(self.corps)-1
        while i >= 0:
            # Draw each body segment
            if i == len(self.corps) - 1:  # Tail segment
                if i > 0:  # Make sure there's a segment before this one
                    prev_segment = self.corps[i-1]
                    current_segment = self.corps[i]
                    
                    # Determine orientation based on relative positions
                    if prev_segment[0] == current_segment[0]:  # Same X = vertical
                        surface.blit(self.corpsVert, pygame.Rect(self.corps[i][0], self.corps[i][1], TAILLE_SNAKE, TAILLE_SNAKE))
                    else:  # Horizontal
                        surface.blit(self.corpsHor, pygame.Rect(self.corps[i][0], self.corps[i][1], TAILLE_SNAKE, TAILLE_SNAKE))
            elif i == 0:  # First segment (after head)
                next_segment = self.corps[i+1]

                if  (self.direction in [0, 1] and self.corps[i][0] == next_segment[0]) or \
                    (self.direction in [2, 3] and self.corps[i][1] == next_segment[1]):
                        surface.blit(self.corpsCoin, pygame.Rect(self.corps[i][0], self.corps[i][1], TAILLE_SNAKE, TAILLE_SNAKE))
                else:
                    # Base on current direction
                    if self.direction in [0, 1]:  # Right or Left = horizontal
                        surface.blit(self.corpsHor, pygame.Rect(self.corps[i][0], self.corps[i][1], TAILLE_SNAKE, TAILLE_SNAKE))
                    else:  # Up or Down = vertical
                        surface.blit(self.corpsVert, pygame.Rect(self.corps[i][0], self.corps[i][1], TAILLE_SNAKE, TAILLE_SNAKE))
            else:  # Middle segments
                # Just look at current and next segment
                current_segment = self.corps[i]
                prev_segment = self.corps[i-1]
                next_segment = self.corps[i+1]

                horizontal_movement = prev_segment[0] != current_segment[0]
                vertical_movement = prev_segment[1] != current_segment[1]
                next_horizontal_movement = current_segment[0] != next_segment[0]
                next_vertical_movement = current_segment[1] != next_segment[1]

                # If the direction changes (from horizontal to vertical or vice versa), it's a corner
                if  (horizontal_movement and next_vertical_movement) or \
                    (vertical_movement and next_horizontal_movement):
                    surface.blit(self.corpsCoin, pygame.Rect(self.corps[i][0], self.corps[i][1], TAILLE_SNAKE, TAILLE_SNAKE))
                else:
                    # Simply check the alignment between segments
                    if current_segment[0] == next_segment[0]:  # Same X = vertical alignment
                        surface.blit(self.corpsVert, pygame.Rect(self.corps[i][0], self.corps[i][1], TAILLE_SNAKE, TAILLE_SNAKE))
                    else:  # Different X = horizontal alignment
                        surface.blit(self.corpsHor, pygame.Rect(self.corps[i][0], self.corps[i][1], TAILLE_SNAKE, TAILLE_SNAKE))
            
            i-=1
        
        #Avance automatiquement dans la direction actuelle
        match self.direction:
            case 0:
                self.image = pygame.image.load("images/assets/spaceshipRight.png")
                if self.rect.x + self.rect.width < a:
                    self.rect.x += TAILLE_SNAKE
            case 1:
                self.image = pygame.image.load("images/assets/spaceshipLeft.png")
                if self.rect.x > rect.x:
                    self.rect.x -= TAILLE_SNAKE
            case 2:
                self.image = pygame.image.load("images/assets/spaceship.png")
                if self.rect.y > rect.y:
                    self.rect.y -= TAILLE_SNAKE
            case 3:
                self.image = pygame.image.load("images/assets/spaceshipDown.png")
                if self.rect.y + self.rect.height < b:
                    self.rect.y += TAILLE_SNAKE

        #Retourne true en cas de collision avec le corps du serpent
        for x in self.corps:
            if self.rect.colliderect(pygame.Rect(x[0], x[1], TAILLE_SNAKE, TAILLE_SNAKE)):
                return True

        self.image = pygame.transform.scale(self.image, (TAILLE_SNAKE, TAILLE_SNAKE))
        surface.blit(self.image, self.rect)
        time.sleep(.1)

        return False


class Fruit():
    def __init__(self, x, y) -> None:
        self.image = pygame.image.load("images/assets/life.png")
        self.image = pygame.transform.scale(self.image, (TAILLE_SNAKE, TAILLE_SNAKE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def affichage(self, surface):
        surface.blit(self.image, self.rect)


class Jeu():

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 600, 560)
        self.joueur = Snake(self.rect.x+100, self.rect.y+100)
        self.pomme = Fruit(self.rect.x+250, self.rect.y+400)
        self.auto = 0
        self.score = 0

    def affichage(self, surface):

        pygame.draw.rect(surface, 'white', self.rect, 2)

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
            jouer_son("audio/score.wav", 1, .1)
            
        return False
    

class Bouton():
    def __init__(self, message, x, y, police):
        self.texte = police.render(message, 1, 'white')
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
                jouer_son("audio/select.wav", 1)
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

#Joue un son
def jouer_son(titre, canal, volume=1):
    son = pygame.mixer.Sound(titre)
    son.set_volume(volume)
    pygame.mixer.Channel(canal).play(son)