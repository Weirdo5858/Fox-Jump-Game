import os
x = 100
y = 100
# vytvorenie hracej plochy na pozícii x a y na displeji
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

import pygame
import pgzrun
import time
import random

WIDTH = 800
HEIGHT = 600
# farba schodíkov
# Postavička
fox = Actor('jumper-1', (400, 550))
fox_x_velocity = 0
fox_y_velocitya = 0
gravity = 1
jumping = False
jumped = False
timer = []
posledny_schod_y = 550 # y-súradnica posledného vygenerovaného schodu
optimalna_vyska_fox = 200 # súradnica kde sa fox bude stále nachádzať
vyska = 0
prvy_pohyb = False

# (left, top, width, height)


# zobrezenie na dispeji
def draw():
    screen.blit('oblaky', (0, 0)) # pozadie
    # nakreslenie schodíkov s hlavným schodom a s farbou
    for schod in schody:
    	screen.blit('schodík', (schod.x, schod.y))
    fox.draw()
    screen.draw.text("Výška:", center=(50, 540), fontsize=40, shadow=(1, 1), color=(255, 255, 255))
    screen.draw.text(str(vyska)+" m", center=(45, 570), fontsize=40, shadow=(1, 1), color=(255, 255, 255))
    if fox.y > HEIGHT:
    	screen.draw.text("Koniec hry", center=(400, 300), fontsize=40, shadow=(1, 1), color=(255, 255, 255))
    	screen.draw.rect(Rect((330, 330), (140,40)), (0,0,0))
    	screen.draw.text("Hrať znovu", center=(400, 350), fontsize=30, shadow=(1, 1), color=(255, 255, 255))

# keď sa klikne myškou na tlačidlo, reštartuje sa hra
def on_mouse_down(pos, button):
	global schody, vyska, jumping, jumped, posledny_schod_y, prvy_pohyb
	if fox.y > HEIGHT and pos[0] > 330 and pos[0] < 470 and pos[1] > 330 and pos[1] < 370:
		jumping = False
		jumped = False
		schody = []
		posledny_schod_y = 550
		schody = generate_first_schody()
		fox.x = 400
		fox.y = 550
		vyska = 0
		prvy_pohyb = False

# game mechanics:
def update():
	global optimalna_vyska_fox, vyska, prvy_pohyb
	fox_move()
	# posúvanie schodov keď skáče + koniec počítania výšky keď sa skončí hra
	if fox.y < optimalna_vyska_fox:
		rozdiel_vysky = optimalna_vyska_fox - fox.y
		fox.y = optimalna_vyska_fox
		for schod in schody:
			schod.y = schod.y + rozdiel_vysky
			if schod.y > HEIGHT and fox.y < HEIGHT:
				schod.x = random.randrange(15, WIDTH - 315)
				schod.y = 0
				vyska += 1
			

	else:
		rozdiel_vysky = fox.y
	# posúvanie schodov, keď neskáče (automaticky, samo)
	if prvy_pohyb:
		for schod in schody:
			if vyska < 25:
				schod.y = schod.y + 1
			# zrýchlenie schodíkov podľa výšky, keď je fox vyššie
			elif vyska < 50:
				schod.y = schod.y + 2
			else:
				schod.y = schod.y + 3
			if schod.y > HEIGHT and fox.y < HEIGHT:
				schod.x = random.randrange(15, WIDTH - 315)
				schod.y = 0
				vyska += 1 

def fox_move():
	global fox_x_velocity, fox_y_velocity, gravity, jumping, jumped, timer, optimalna_vyska_fox, vyska, prvy_pohyb	
	# obrázok stojaci

	if fox_x_velocity == 0 and not jumped:
		fox.image = 'jumper-1'

	# gravity
	if collidecheck():
		gravity = 1
		fox.y -= 1
		timer = []
	if not collidecheck():
		fox.y += gravity
		if gravity <= 20:
			gravity += 0.5
		timer.append(pygame.time.get_ticks()) # aby sa neskákalo stále
		# obrázok pri padaní
		if len(timer) > 5 and not jumped:
			fox.image = 'jumper-1'
			if len(timer) > 5:
				fox.image = 'jumper-fall'

	# hýbanie s postavičkou doľava a doprava
	# obrázky doprava a doľava a skor doprava a doľava
	# ak prídamé 'and allowx' tak zakážem hýbanie pri padaní 
	if (keyboard.left):
		if (fox.x > 40) and (fox_x_velocity > -8):
			fox_x_velocity -= 2
			fox.image = 'jumper-left'
			if (keyboard.left) and jumped:
				fox.image = 'jumper-jleft'
	if (keyboard.right):
		if (fox.x < 760) and (fox_x_velocity < 8):
			fox_x_velocity += 2	
			fox.image = 'jumper-right'
			if (keyboard.right) and jumped:
				fox.image = 'jumper-jright'

	fox.x += fox_x_velocity

	#rýchlosť
	if fox_x_velocity > 0:
		fox_x_velocity -= 1
	if fox_x_velocity < 0:
		fox_x_velocity += 1

	if fox.x < 50 or fox.x > 750:
		fox_x_velocity = 0

	# skákanie
	if (keyboard.up) and collidecheck() and not jumped:
		jumping = True
		jumped = True
		prvy_pohyb = True
		clock.schedule_unique(jumpedrecently, 0.5)
		fox.image = 'jumper-1'
		fox_y_velocity = 95 # optimálne číslo kvôli gravitácii
	if jumping and fox_y_velocity > 25:
		fox_y_velocity = fox_y_velocity - ((100 - fox_y_velocity)/2)
		fox.y -= fox_y_velocity/3 # výška skoku
	else:
		fox_y_velocity = 0
		jumping = False




def collidecheck():
	collide = False
	for i in schody:
		if fox.colliderect(i):
			collide = True
	return collide

def jumpedrecently():
	global jumped
	jumped = False

# vytvorenie prvých schodíkov na random pozíciách
def generate_first_schody():
	global posledny_schod_y
	vytvorene_schodiky = []

	hl_schod = Rect((250, posledny_schod_y), (300, 2))
	vytvorene_schodiky.append(hl_schod)

	while not (posledny_schod_y < 100):
		schodik_x = random.randrange(15, WIDTH - 315)
		schodik_y = random.randrange(posledny_schod_y - 130, posledny_schod_y - 100)
		jeden_schodik = Rect((schodik_x, schodik_y), (300, 2))
		posledny_schod_y = schodik_y
		vytvorene_schodiky.append(jeden_schodik)

	return vytvorene_schodiky


schody = generate_first_schody()

pgzrun.go()

# na ukazovatele medzier
# "draw_white_space": "all" a ešte čiarka predtým