import requests, json, random
from functions import *

klok = pygame.time.Clock()
scherm_size = schermgrootte((1000, 800))
scherm = pygame.display.set_mode(scherm_size)
kleinetext_size = pygame.font.SysFont(pygame.font.get_default_font(), 50)
grotetext_size = pygame.font.SysFont(pygame.font.get_default_font(), 300)

pygame.display.set_caption("Try to click the button")


vraag = True
muisknop = gekozen = False
kleur_cirkel = rood

def antwoordcirkel(kleur: tuple[int,int,int], i: int):
    global kleur_cirkel, muisknop, antwoordlijst, correct_antwoord, gekozen
    kleur_cirkel = kleur

    if muisknop:
        if kleur == groen:
            gekozen = True
            if antwoordlijst[i] == correct_antwoord:
                return True
            else:
                return False

def antwoordcheck(kleur):
    scherm.fill(kleur)
    if kleur == rood:
        eindtekst = grotetext_size.render("incorrect!", False, wit)
    else:
        eindtekst = grotetext_size.render("correct!", False, wit)
    text_rect = eindtekst.get_rect(center = scherm.get_rect().center)

    infotekst = kleinetext_size.render("nieuwe vragen worden geladen...", False, wit)
    scherm.blit(infotekst, (midden(infotekst), 600))
    scherm.blit(eindtekst, text_rect)
    pygame.display.flip()
            
def get_vraag():
    global data, correct_antwoord, antwoordlijst
    link = "https://opentdb.com/api.php?amount=1&category=22"
    response = requests.get(link) # GET de info van deze website.
    data = json.loads(response.text)
    antwoordlijst = []
    correct_antwoord = data['results'][0]['correct_answer']
    incorrect_antwoord = data['results'][0]['incorrect_answers']
    antwoordlijst.append(correct_antwoord)
    for i in range(len(incorrect_antwoord)):
        antwoordlijst.append(incorrect_antwoord[i])
    randomshuffle = random.randint(1, 100)
    for i in range(randomshuffle):
        random.shuffle(antwoordlijst)
    

while True:
    if vraag:
        get_vraag()
        vraag = False


    while True:
        scherm.fill(wit)
    
        # soortvraag = kleinetext_size.render()
        if len(data['results'][0]['question']) > 50:
            gesteldevraag = data['results'][0]['question'][0:50]
            vraagtekst = kleinetext_size.render(f"{gesteldevraag}", False, zwart)
            scherm.blit(vraagtekst, (10, 10))
            if len(data['results'][0]['question']) > 100:
                gesteldevraag = data['results'][0]['question'][50: 100]
                vraagtekst = kleinetext_size.render(f"{gesteldevraag}", False, zwart)
                scherm.blit(vraagtekst, (10, 60))
                gesteldevraag = data['results'][0]['question'][100: len(data['results'][0]['question'])]
                vraagtekst = kleinetext_size.render(f"{gesteldevraag}", False, zwart)
                scherm.blit(vraagtekst, (10, 110))
            else:
                gesteldevraag = data['results'][0]['question'][50: len(data['results'][0]['question'])]
                vraagtekst = kleinetext_size.render(f"{gesteldevraag}", False, zwart)
                scherm.blit(vraagtekst, (10, 60))
        else:
            gesteldevraag = data['results'][0]['question']
            vraagtekst = kleinetext_size.render(f"{gesteldevraag}", False, zwart)
            scherm.blit(vraagtekst, (10, 10))


        

        for i in range(len(antwoordlijst)):
            if len(antwoordlijst) > 4 and i > 3:
                optietekst = kleinetext_size.render(f"{i + 1}. {antwoordlijst[i]}", False, zwart)
                scherm.blit(optietekst, (600, 130 + i * 60))
            else:
                optietekst = kleinetext_size.render(f"{i + 1}. {antwoordlijst[i]}", False, zwart)
                scherm.blit(optietekst, (100, 130 + i * 60))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                muisknop = True
            if event.type == pygame.MOUSEBUTTONUP:
                muisknop = False

        for i in range(len(antwoordlijst)):
            tellertext = grotetext_size.render(f"{i + 1}", False, (255, 255, 255))
            if len(antwoordlijst) > 4 and i > 3:
                if cirkeldetectie((125 + i * 250, 700), 100, draw=False):
                   antwoord = antwoordcirkel(groen, i)
                else:
                    antwoord = antwoordcirkel(rood, i)
                pygame.draw.circle(scherm, kleur_cirkel, (125 + i * 250, 700), 100)
                scherm.blit(tellertext, ((125 + i * 250) - (tellertext.get_width() / 2), 600))
            else:
                if cirkeldetectie((125 + i * 250, 450), 100, draw=False):
                    antwoord = antwoordcirkel(groen, i)
                else:
                    antwoord = antwoordcirkel(rood, i)
                pygame.draw.circle(scherm, kleur_cirkel, (125 + i * 250, 450), 100)
                scherm.blit(tellertext, ((125 + i * 250) - (tellertext.get_width() / 2), 350))
            if gekozen:
                break
        
        if gekozen:
            break

        pygame.display.flip()

    
    if antwoord:
        antwoordcheck(groen)
        antwoord = gekozen = False
        get_vraag()

    
    else:
        antwoordcheck(rood)
        gekozen = False
        get_vraag()

