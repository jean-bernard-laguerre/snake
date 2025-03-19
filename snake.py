import pygame
from outils import *

pygame.init()

fenetre = pygame.display.set_mode((800,600))
pygame.display.set_caption("Snake")
tdr = pygame.time.Clock()

pygame.mixer.music.load("audio/musique/Audiorezout - Subterranean.mp3")
pygame.mixer.music.set_volume(.5)
pygame.mixer.music.play(-1)

police_snake = pygame.font.Font('polices/Orbitron-Regular.ttf', 16)
police_titre = pygame.font.Font('polices\Monoton-Regular.ttf', 128)

bg_menu = pygame.image.load("images/bg_menu.png")
bg_menu_rect = bg_menu.get_rect()

bg_jeu = pygame.image.load("images/bg_jeu.png")
bg_jeu_rect = bg_jeu.get_rect()

bg_fin = pygame.image.load("images/bg_fin.png")
bg_fin_rect = bg_fin.get_rect()

statut_partie = 0

def ecran_menu():

    global statut_partie
    titre = police_titre.render("SNAKE", 1 ,'white')
    fenetre.blit(bg_menu, bg_menu_rect)
    fenetre.blit(titre, (140, 100))

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
    fenetre.blit(bg_jeu, bg_jeu_rect)

    score = police_snake.render(f"Score: {jeu.score}", 1 ,'white')

    if jeu.affichage(fenetre):
        statut_partie = 2
        enregistrer(jeu.score)

    fenetre.blit(score, (10, 25))
                
                
def ecran_fin():
    global statut_partie
    fenetre.blit(bg_fin, bg_fin_rect)
    
    score = police_snake.render(f"Score: {jeu.score}", 1, 'white')
    
    if Bouton("Retour Menu", 600, 500, police_snake).affichage(fenetre):

        statut_partie = 0

    if Bouton("Scores", 100, 500, police_snake).affichage(fenetre):

        statut_partie = 3
        
    fenetre.blit(score,(350,275))


def ecran_score():
    global statut_partie
    fenetre.blit(bg_menu, bg_menu_rect)

    lbl_score = police_snake.render("Meilleurs scores", 1, 'white')
    fenetre.blit(lbl_score, (325, 50))

    for i,score in enumerate(recuperer()):
        texte = police_snake.render(f"{score}", 1, 'white')
        fenetre.blit(texte, (380, (100+(i*40))))

    if Bouton("Retour Menu", 600, 500, police_snake).affichage(fenetre):

        statut_partie = 0


def nouvelle_partie():
    global jeu

    jeu = Jeu(100, 20)


en_cours = True
while en_cours:

    tdr.tick(60)
    fenetre.fill((40,40,40))

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