import pygame
from outils import *

pygame.init()

fenetre = pygame.display.set_mode((800,600))
tdr = pygame.time.Clock()
police_snake = pygame.font.SysFont('Verdana', 16)

statut_partie = 0

def ecran_menu():

    global statut_partie

    if Bouton("Jouer", 250, 350, police_snake).affichage(fenetre):

        nouvelle_partie()
        statut_partie = 1
    
    if Bouton("Partie Auto", 450, 350, police_snake).affichage(fenetre):

        nouvelle_partie()
        jeu.auto = 1
        statut_partie = 1
    
    if Bouton("Scores", 100, 500, police_snake).affichage(fenetre):

        statut_partie = 3


def ecran_jeu():

    global statut_partie

    score = police_snake.render(f"Score: {jeu.score}", 1 ,'black')

    if jeu.affichage(fenetre):
        statut_partie = 2
        enregistrer(jeu.score)

    fenetre.blit(score, (10, 25))
                
                
def ecran_fin():
    global statut_partie
    
    score = police_snake.render(f"Score: {jeu.score}", 1, 'black')
    
    if Bouton("Retour Menu", 600, 500, police_snake).affichage(fenetre):

        statut_partie = 0

    if Bouton("Scores", 100, 500, police_snake).affichage(fenetre):

        statut_partie = 3
        
    fenetre.blit(score,(350,275))


def ecran_score():
    global statut_partie

    lbl_score = police_snake.render("Meilleurs scores", 1, 'black')
    fenetre.blit(lbl_score, (325, 50))

    for i,score in enumerate(recuperer()):
        texte = police_snake.render(f"{score}", 1, 'black')
        fenetre.blit(texte, (380, (100+(i*40))))

    if Bouton("Retour Menu", 600, 500, police_snake).affichage(fenetre):

        statut_partie = 0


def nouvelle_partie():
    global jeu

    jeu = Jeu(100, 20)


en_cours = True
while en_cours:

    tdr.tick(60)
    fenetre.fill((255,255,255))

    match statut_partie:
        case 0:
            ecran_menu()
        case 1:
            ecran_jeu()
        case 2:
            ecran_fin()
        case 3:
            ecran_score()
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
    

    pygame.display.update()

pygame.quit()