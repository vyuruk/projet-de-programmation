#-*- coding: utf-8 -*-
import blessed, math, os, time, random

term = blessed.Terminal()

def main_game(CPX_file, group_1, type_1, group_2, type_2):
	"""Play a Copixhe game.

	Parameters
	----------
	CPX_file: name of CPX file (str)
	group_1: group of player 1 (str)
	type_1: type of player 1 (str)
	group_2: group of player 2 (str)
	type_2: type of player 2 (str)

	Notes
	-----
	Player type is either human, AI or remote.

	If there is an external referee, set group id to 0 for remote player.

	"""
	data(cpx_file)
	ant_dico = data(cpx_file)[0]
	print(ant_dico)
	anthill_dico = data(cpx_file)[1]
	clod_dico = data(cpx_file)[2]
	#Display_interface(cpx_file,ant_dico,clod_dico,anthill_dico) 
	Turn = 0 
	while not Is_game_over(Clod_number_around_anthill,clod_dico,anthill_dico):
		Display_interface(cpx_file,ant_dico,clod_dico,anthill_dico)
		#Demander ordre 
		order_player_1 = input("Indiquer vos ordres (P1)")
		order_player_2 = input("Indiquer vos ordres (P2) ")
		order = player_order(order_player_1,order_player_2)
		lift_clod(order,ant_dico,clod_dico)
		drop_clod(order,ant_dico,clod_dico)
		Fight(order,ant_dico)
		Ant_movement(order, ant_dico, clod_dico, ant_dico)

		# création nouvelle fourmis 
		Is_ant_dead(ant_dico) 
		New_ant(Turn,ant_dico,anthill_dico,clod_dico,Clod_number_around_anthill)

		Turn += 1
	End_game(Clod_number_around_anthill,clod_dico,anthill_dico) 

def player_order(order_player_1, order_player_2):
	"""the function that will allow players to give orders during the game
	
	parameters
	----------
	order_player_1: the order of the first player during the game(str)
	order_player_2: the order of the second player during the game(str)

	return
	------
	order_p1 : The order of the first player separate in a list (list)
	order_p2 : The order of the second player separate in a list (list)
	
	Version
	-------
	Specification : Yuruk Valentin ( v.1 22/02/21)
	Implémentation : Marchal Tom (v.1 1/03/21)
	"""
	#split the order in list
	order_p1 = order_player_1.split()
	order_p2 = order_player_2.split()
	return order_p1, order_p2

def Is_game_over(Clod_number_around_anthill,clod_dico,anthill_dico):
	"""Verify if the game is over or not.
	parameters
	----------
	Clod_number_around_anthill: Count the number of clods around the anthill(list)

	return
	------
	Is_game_over : If the game is over or not(bool)
	Version
	-------
	Specification : Yuruk Valentin, Antoine Boudjenah ( v.2 15/03/21)
	Implementation : Yuruk Valentin, Antoine Boudjenah (V.1 16/03/21)
	"""
	nbr_cld_b = Clod_number_around_anthill(clod_dico,anthill_dico)[0]
	nbr_cld_r = Clod_number_around_anthill(clod_dico,anthill_dico)[1]
	Is_game_over = False
	if nbr_cld_r == 8 or nbr_cld_b == 8:
		Is_game_over = True

def End_game(Clod_number_around_anthill,clod_dico,anthill_dico): 
	""" Finish the game and display the winner team.
	Parameter
	---------
	Clod_number_around_anthill: Count the number of clods around the anthill(list)
	clod_dico : The dico of the clods (dict)
	anthill_dico : The dico of the anthills (dict)

	Version
	-------
	Specification : Yuruk Valentin, Marchal Tom (v.2 16/32/21)
	Implementation : Yuruk Valentin, Antoine Boudjenah (V.2 16/03/21)
	"""

	#R if red team win, B if bleu team win, E if there's no winner(bool)

	nbr_cld_b = Clod_number_around_anthill(clod_dico,anthill_dico)[0]
	nbr_cld_r = Clod_number_around_anthill(clod_dico,anthill_dico)[1]
	if nbr_cld_r == 8: 
		if nbr_cld_b == 8:
			#No winner
			print("There's no winner")
		else:
			#Blue team win
			print("Blue team is the winner")	
	elif nbr_cld_b == 8:
		#Red team win
		print("Red team is the winner")	

def drop_clod(order,ant_dico,clod_dico):
	""" Check if the ant can drop the clod.

	parameter
	---------
	order: The order of the player (str)
	ant_dico: The dico of the ants (dict)
	clod_dico: The dico of the clods (dict)

	version
	-------
	Specification : Marchal Tom (v.1 26/02/21)
	Implémentation : Marchal Tom (v.1 26/03/21)
	"""
	order_p1 = order[0]
	order_p2 = order[1]
	for order in order_p1:
		if 'drop' in order:
			ant = order[:4]
			ant_x = ant[:1]
			ant_y = ant[3:]
			ant = (ant_x,ant_y)
			for clod in clod_dico :
				#check if the ant carry a clod
				if clod[0] == ant[0] and clod[1] == ant[1]:
					#drop the clod
					ant_dico[ant]['team'] = False
	for order in order_p2:
		if 'drop' in order:
			ant = order[:4]
			ant_x = ant[:1]
			ant_y = ant[3:]
			ant = (ant_x,ant_y)
			for clod in clod_dico :
				#check if the ant carry a clod
				if clod[0] == ant[0] and clod[1] == ant[1]:
					#drop the clod
					ant_dico[ant]['team'] = False
def lift_clod(order,ant_dico,clod_dico):
	""" Check if the ant can lift the clod.

	parameter
	---------
	order: The order of the player (str)
	ant_dico: The dico of the ants (dict)
	clod_dico: The dico of the clods (dict)

	version
	-------
	Specification : Marchal Tom (v.1 26/02/21)
	Implémentation : Marchal Tom (v.1 26/03/21)
	"""
	order_p1 = order[0]
	order_p2 = order[1]
	for order in order_p1:
		if 'drop' in order:
			ant = order[:4]
			ant_x = ant[:1]
			ant_y = ant[3:]
			ant = (ant_x,ant_y)
			for clod in clod_dico:
				#check if there is a clod 
				if clod_dico[clod][0] == ant_dico[ant][0] and clod_dico[clod][1] == ant_dico[ant][1]:
					ant_dico[ant][clod] == True
	
	for order in order_p2:
		if 'drop' in order:
			ant = order[:4]
			ant_x = ant[:1]
			ant_y = ant[3:]
			ant = (ant_x,ant_y)
			for clod in clod_dico:
				#check if there is a clod 
				if clod_dico[clod][0] == ant_dico[ant][0] and clod_dico[clod][1] == ant_dico[ant][1]:
					ant_dico[ant][clod] == True
def Fight(order,ant_dico): 
	""" Check if the ant can attack the other one, attack if he can.

	Parameter
	---------
	order : The order of the player (list) 
	ant_dico : The dico of the ants (dict)

	Version
	-------
	Specification : Marchal Tom (v.2 19/03/21)
	Implémentation : Valentin Yuruk, Marchal Tom (v.1 26/03/21)
	"""
	order_p1 = order[0]
	order_p2 = order[1]
	for order in order_p1:
		if '*' in order:
			fighter = order[:4]
			fighter_x = fighter[:1]
			fighter_y = fighter[3:]
			fighter = (fighter_x,fighter_y)
			target = order[7:]
			target_x = target[:1]
			target_y = target[3:]
			target = (target_x,target_y)
			for ant in ant_dico:
				if fighter[0] ==  ant_dico[ant][0] and fighter[1] == ant_dico [ant][1:]:
					for b in ant_dico:
						if target[0]==ant_dico[ant][0] and target[1] == ant_dico[ant][1]:
							distance_x = abs(target[0] - fighter[0])
							distance_y = abs(target[1] - fighter[1])
							if ant_dico[fighter]['scope'] <= distance_x and ant_dico[fighter]['scope'] <= distance_y:
								damage = ant_dico[fighter]['strength']
								ant_dico[target]['life'] -= damage
	for order in order_p2:
		if '*' in order:
			fighter = order[:4]
			fighter_x = fighter[:1]
			fighter_y = fighter[3:]
			fighter = (fighter_x,fighter_y)
			target = order[7:]
			target_x = target[:1]
			target_y = target[3:]
			target = (target_x,target_y)
			for ant in ant_dico:
				if fighter[0] ==  ant_dico[ant][0] and fighter[1] == ant_dico [ant][1:]:
					for b in ant_dico:
						if target[0]==ant_dico[ant][0] and target[1] == ant_dico[ant][1]:
							distance_x = abs(target[0] - fighter[0])
							distance_y = abs(target[1] - fighter[1])
							if ant_dico[fighter]['scope'] <= distance_x and ant_dico[fighter]['scope'] <= distance_y:
								damage = ant_dico[fighter]['strength']
								ant_dico[target]['life'] -= damage

def Ant_movement(order, ant_dico, clod_dico, anthill_dico): 
	""" Check if the ant can move where the order indicate.
	Parameter
	---------
	order : The order of the player (list)
	ant_dico : The dico of the ants (dict)
	clod_dico : The dico of the clods(dict)
	anthill_dico = the dico of the anthills(dict)
	Version
	-------
	Specification : Marchal Tom (v.2 19/03/21)
	Implémentation: Marchal Tom (v.1 19/03/21)
	"""
	order_p1 = order[0]
	order_p2 = order[1]
	for order in order_p1:
		if '@' in order:
			coordinate = order[:4]
			target = order[7:]
			coordinate_x = int(coordinate[:1])
			coordinate_y = int(coordinate[3:])
			coordinate = (coordinate_x,coordinate_y)
			target_x = int(target[:1])
			target_y = int(target[3:])
			target = (target_x,target_y)
			#check if the ant exist
			for ant in ant_dico:
				if coordinate[0] == ant_dico[ant][0] and coordinate[1] == ant_dico[ant][1]:
					#check if there is no ant at the destination
					for a in ant_dico:
						if target[0] != ant_dico[a][0] and target[1] != ant_dico[a][1]:
							#check if there is a clod where the ant will move
							for clod in clod_dico:
								if target[0] != clod_dico[clod][0]  and target[1] != clod_dico[clod][1]:
									#check if the ant doesn't move at the rival anthill
									for anthill in anthill_dico:
										if ant_dico[coordinate]['team'] not in anthill:
											if target[0] != anthill_dico[anthill][0]  and target[1] != anthill_dico[anthill][1]:
												ant_dico[coordinate][0] = target[0]
												ant_dico[coordinate][1] = target[1]
												#check if the ant carry a clod
												if ant_dico[coordinate][clod]:
													for clod in clod_dico:
																if clod_dico[clod][0] == ant_dico[coordinate][0] and clod_dico[clod][1] == ant_dico[coordinate][1]:
																	clod_dico[clod][0] = target[0]
																	clod_dico[clod][0] = target[1]
								#check if the ant doesn't carry a clod when there is a clod a the target
								else:
									if ant_dico[coordinate][clod] == False:
										ant_dico[coordinate][0] = target[0]
										ant_dico[coordinate][1] = target[1]
								
	for order in order_p2:
		if '@' in order:
			coordinate = order[:4]
			target = order[7:]
			coordinate_x = int(coordinate[:1])
			coordinate_y = int(coordinate[3:])
			coordinate = (coordinate_x,coordinate_y)
			target_x = int(target[:1])
			target_y = int(target[3:])
			target = (target_x,target_y)
			#check if the ant exist
			for ant in ant_dico:
				if coordinate[0] == ant_dico[ant][0] and coordinate[1] == ant_dico[ant][1]:
					#check if there is no ant at the destination
					for a in ant_dico:
						if target[0] != ant_dico[a][0] and target[1] != ant_dico[a][1]:
							#check if there is a clod where the ant will move
							for clod in clod_dico:
								if target[0] != clod_dico[clod][0]  and target[1] != clod_dico[clod][1]:
									#check if the ant doesn't move at the rival anthill
									for anthill in anthill_dico:
										if ant_dico[coordinate]['team'] not in anthill:
											if target[0] != anthill_dico[anthill][0]  and target[1] != anthill_dico[anthill][1]:
												ant_dico[coordinate][0] = target[0]
												ant_dico[coordinate][1] = target[1]
												#check if the ant carry a clod
												if ant_dico[coordinate][clod]:
													for clod in clod_dico:
																if clod_dico[clod][0] == ant_dico[coordinate][0] and clod_dico[clod][1] == ant_dico[coordinate][1]:
																	clod_dico[clod][0] = target[0]
																	clod_dico[clod][0] = target[1]
								#check if the ant doesn't carry a clod when there is a clod a the target
								else:
									if ant_dico[coordinate][clod] == False:
										ant_dico[coordinate][0] = target[0]
										ant_dico[coordinate][1] = target[1]
							
		
def New_ant(turn, ant_dico, anthill_dico, clod_dico,Clod_number_around_anthill): 
	""" Create an ant every 5 turns if there is nothing on the spawn coordinate and adapt the level of the ant with the number of clod around the anthill.

	Parameter
	---------
	turn: The number of turn (int)
	ant_dico: The dico of the ants (dict)
	anthill_dico : The dico of the anthills(dict)
	clod_dico : The dico of the clods (dict)
	Clod_number_around_anthill : Count the number of clods around the anthills (list)

	Version
	-------
	Specification : Marchal Tom (v.1 20/02/21)
	Implémentation : Marchal Tom (v.1 19/03/21)
	"""
	clods = Clod_number_around_anthill(clod_dico,anthill_dico)
	clods_blue = clods[0]
	clods_red = clods[1]
	if turn % 5 == 0:
		for ant in ant_dico:
			if ant_dico[ant][0] != anthill_dico['anthill_blue'][0] and ant_dico[ant][0] != anthill_dico['anthill_blue'][1]:
				if clods_blue <= 2:
					ant_dico['key'] = (anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['life'] = 3
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['scope'] = 3
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['strength'] = 1
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['clod'] = False
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['team'] = 'blue'
				if clods_blue <= 5 and clods_blue > 3:
					ant_dico['key'] = (anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['life'] = 5
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['scope'] = 3
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['strength'] = 2
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['clod'] = False
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['team'] = 'blue'
				if clods_blue <= 8 and clods_blue > 6:
					ant_dico['key'] = (anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['life'] = 7
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['scope'] = 3
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['strength'] = 3
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['clod'] = False
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['team'] = 'blue'
			if ant_dico[ant][0] != anthill_dico['anthill_red'][0] and ant_dico[ant][0] != anthill_dico['anthill_red'][1]:
				if clods_red <= 2:
					ant_dico['key'] = (anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['life'] = 3
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['scope'] = 3
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['strength'] = 1
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['clod'] = False
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['team'] = 'blue'
				if clods_red <= 5 and clods_red > 3:
					ant_dico['key'] = (anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['life'] = 5
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['scope'] = 3
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['strength'] = 2
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['clod'] = False
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['team'] = 'blue'
				if clods_red <= 8 and clods_red > 6:
					ant_dico['key'] = (anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['life'] = 7
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['scope'] = 3
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['strength'] = 3
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['clod'] = False
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['team'] = 'blue'
def Is_ant_dead(Ant_dico):
	"""verify if a ant is dead or not.
	parameters
	----------
	Ant_dico: dictionary of ant (dict)
	
	Version
	------- 
	Specification : Antoine Boudjenah (v.1 22/02/21)
	"""
def Clod_number_around_anthill(clod_dico, anthill_dico):
	"""the function that will count clods around the anthills.
	parameters
	----------
	clod_dico: dictionary of the clod (dict)
	anthill_dico: dictionary of anthill (dict)

	return
	------
	nbr_cld_r: the number of clod around the red anthill(int)
	nbr_cld_b: the number of clod around the blue anthill(int)
	
	Version
	------- 
	Specification : Antoine Boudjenah, Marchal Tom (v.1 22/02/21)
	Implémentation : Marchal Tom (v.1 26/03/21)
	"""
	#count the clods for the blue anthill
	anthill_b_x = anthill_dico['anthill_blue'][0]
	anthill_b_y = anthill_dico['anthill_blue'][1]
	nbr_cld_b = 0
	for clod in clod_dico:
		#check if there is a clod up or under the anthill
		if clod[0] == anthill_b_x:
			if clod[1] == (anthill_b_y + 1) or clod[1] == (anthill_b_y - 1):
				nbr_cld_b += 1
		#check if there is a clod on the left or the right of the anthill
		if clod[1] == anthill_b_y:
			if clod[0] == (anthill_b_x + 1) or clod[0] == (anthill_b_x - 1):
				nbr_cld_b += 1
		#check if there is a clod up-left or up_right the anthill
		if clod[1] == (anthill_b_y + 1):
			if clod[0] == (anthill_b_x + 1) or clod[0] == (anthill_b_x - 1):
				nbr_cld_b += 1
		#check if there is a clod down-left or down-right the anthill
		if clod[1] == (anthill_b_y - 1):
			if clod[0] == (anthill_b_x + 1) or clod[0] == (anthill_b_x - 1):
				nbr_cld_b += 1
	
	#count the clods for the red anthill
	anthill_r_x = anthill_dico['anthill_red'][0]
	anthill_r_y = anthill_dico['anthill_red'][1]
	nbr_cld_r = 0
	for clod in clod_dico:
		#check if there is a clod up or under the anthill
		if clod[0] == anthill_r_x:
			if clod[1] == (anthill_r_y + 1) or clod[1] == (anthill_r_y - 1):
				nbr_cld_r += 1
		#check if there is a clod on the left or the right of the anthill
		if clod[1] == anthill_r_y:
			if clod[0] == (anthill_r_x + 1) or clod[0] == (anthill_r_x - 1):
				nbr_cld_r += 1
		#check if there is a clod up-left or up_right the anthill
		if clod[1] == (anthill_r_y + 1):
			if clod[0] == (anthill_r_x + 1) or clod[0] == (anthill_r_x - 1):
				nbr_cld_r += 1
		#check if there is a clod down-left or down-right the anthill
		if clod[1] == (anthill_r_y - 1):
			if clod[0] == (anthill_r_x + 1) or clod[0] == (anthill_r_x - 1):
				nbr_cld_r += 1
	return nbr_cld_b, nbr_cld_r

def Display_interface(cpx_file, ant_dico, clod_dico, anthill_dico):
	"""display the interface at the start of the game till the end. 
	parameters
	----------
	cpx_file : The file with the data (file)
	clod_dico: dictionary of the clod (dict)
	anthill_dico: dictionary of anthill (dict)
	ant_dico: dictionary of ant (dict)

	Version
	------- 
	Specification : Antoine Boudjenah (v.1 22/02/21)
	Implémentation : Marchal Tom (v.1 12/03/21)
	""" 
	fh=open(".\data_game.txt",'r')
	lines = fh.readlines()
	fh.close()
	map = lines[1]
	map = map.split()
	rows = int(map[0]) * 2
	columns = int(map[1]) * 2
	print(term.home + term.clear)
	nrow = 1
	ncol = 1
	for row in range (0,rows+1):
		print(term.move_yx(row,columns) + term.black + term.on_green + "|" + term.normal, end='', flush=True)
		print(nrow)
		nrow +=1
		for col in range(0, columns+1):
			if col %2 == 0:
				print(term.move_yx(row,col) + term.black + term.on_green + "_" + term.normal, end='', flush=True)
			else:
				print(term.move_yx(row,col) + term.black + term.on_green + "|" + term.normal, end='', flush=True)
	for ant in ant_dico:
		x = ant[0]
		y = ant[1]
		if ant_dico[ant]['team'] == 'blue':
			if ant_dico[ant]['clod']:
				print(term.move_yx(x,y) + term.brown + term.on_blue + ":" + term.normal, end='', flush=True)
			else:
				print(term.move_yx(x,y) + term.brown + term.on_blue + "." + term.normal, end='', flush=True)
		else:
			if ant_dico[ant]['clod']:
				print(term.move_yx(x,y) + term.brown + term.on_red + ":" + term.normal, end='', flush=True)
			else:
				print(term.move_yx(x,y) + term.brown + term.on_red + "." + term.normal, end='', flush=True)
	for clod in clod_dico:
		x = clod[0]
		y = clod[1]
		for ant in ant_dico:
			if clod_dico[clod] != ant_dico[ant]:
				print(term.move_yx(x,y) + term.brown + term.on_red + "" + term.normal, end='', flush=True)
	for anthill in anthill_dico:
		x = anthill[0]
		y = anthill[1]
		if anthill == 'anthill_blue':
			print(term.move_yx(row, col) + term.blue + term.on_green + u"\u25A0" + term.normal, end='', flush=True)
		else:
			print(term.move_yx(row, col) + term.red + term.on_green + u"\u25A0" + term.normal, end='', flush=True)
def data(cpx_file):
	""" Create all the dictionnaries for the data structure.

	Parameters
	----------
	cpx_file: name of cpx file(str)
	
	return
	------
	Clod_dico: The clod dico (dict)
	Anthill_dico: The anthill dico(dict)
	ant_dico: The ant dico (dict)

	version
	-------
	Specification: Marchal Tom (v.1 26/02/21)
	Implémentation: Marchal Tom (v.1 12/03/21)
	"""
	fh = open('.\data_game.txt', 'r')
	lines = fh.readlines()
	fh.close()
	clod_dico = {}
	anthill_dico = {}
	ant_dico = {}
	nb_lines = 0
	for line in lines:
		if 'anthills' in line:
			anthill_blue = lines[nb_lines + 1]
			anthill_blue = anthill_blue.split()
			anthill_blue = (int(anthill_blue[0]), int(anthill_blue[1]))
			anthill_dico['anthill_blue'] = anthill_blue
			anthill_red = lines[nb_lines + 2]
			anthill_red = anthill_red.split()
			anthill_red = (int(anthill_red[0]), int(anthill_red[1]))
			anthill_dico['anthill_red'] = anthill_red
		if 'clods' in line:
			for clod in range(nb_lines + 1, len(lines)):
				clod = lines[clod]
				clod = clod.split()
				coordinate = (int(clod[0]), int(clod[1]))
				weight = int(clod[2])
				clod_dico[coordinate] = weight
		nb_lines += 1
	return ant_dico, anthill_dico, clod_dico

def cpx_file():
	"""Create the file with all the data.
	
	Version 
	-------
	Spécification : Marchal Tom (v.1 26/03/21)
	Implémentation : Marchal Tom (v.1 06/03/21)
	"""
	#create coordinate of the map
	map_x = random.randint(20,60)
	map_y = random.randint(20,60)
	#create the coordinate of the anthills
	anthill_blue= [random.randint(1,map_x),  random.randint(1,map_y)]
	anthill_red= [random.randint(1,map_x),  random.randint(1,map_y)]
	#create the number of clods
	clods_number = random.randint(15,int(((map_x+map_y)/2)))
	#create the coordinate of the clods
	clods = []
	for clod in range (0,clods_number+1):
		clod = [random.randint(0,map_x),  random.randint(0,map_y)]
		#verify if the coordinate != the anthills coordinates
		while clod[0] == anthill_blue[0] or clod[0] == anthill_red[0] and clod[1] == anthill_blue[1] or clod[1] == anthill_red[1]:
			clod = [random.randint(0,map_x),  random.randint(0,map_y)]
		#append the weight of the clod
		clod.append(random.randint(1,3))
		clods.append(clod)

	#create txt file
	fh = open('.\data_game.txt', 'w')
	fh.write('map : \n%d %d \n'%(map_x,map_y))
	fh.write('anthills : \n%d %d \n%d %d \n'%(anthill_red[0],anthill_red[1],anthill_blue[0],anthill_blue[1]))
	fh.write('clods : \n')
	for clod in clods:
		fh.write('%d %d %d \n'%(clod[0],clod[1],clod[2]))
	fh.close()

main_game(cpx_file,'gr_38','player','gr_2', 'player')
