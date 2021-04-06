import blessed, math, os, time, random, socket, time, remote_play

term = blessed.Terminal()

def main_game(cpx_file, group_1, type_1, group_2, type_2):
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
	cpx_file()
	ant_dico = data(cpx_file)[0]
	anthill_dico = data(cpx_file)[1]
	clod_dico = data(cpx_file)[2]
	map = data(cpx_file)[3]
	turn = 1
	shift = 3
	
	#Display_interface(map,ant_dico,clod_dico,anthill_dico,shift)
	
	while not Is_game_over(Clod_number_around_anthill,clod_dico,anthill_dico,turn):
		#Changer display interface par une fonction qui affiche à chaque tour
		Display_interface(map,ant_dico,clod_dico,anthill_dico,shift)
		print(ant_dico)
		if type_1 == "human" and type_2 == "human":
			order_player_1 = input("\n Indiquer vos ordres (P1)")
			order_player_2 = input("Indiquer vos ordres (P2) ")
			order = player_order(order_player_1,order_player_2)
		if type_1 == "IA" and type_2 == "IA":
			order_player_1 = IA_naive(ant_dico,"p1")
			order_player_2 = IA_naive(ant_dico,"p2")
			order = player_order(order_player_1,order_player_2)
		# create connection
		if type_1 == 'remote':
			connection = remote_play.create_connection(group_2, group_1, verbose=True)
		if type_2 == 'remote':
			connection = remote_play.create_connection(group_1, group_2, verbose=True)

		# get player types
		types = {1:type_1, 2:type_2}

		# main loop (until one of both players says "stop")
		sentences = {1:'', 2:''}
		while sentences[1] != 'Stop' and sentences[2] != 'Stop':
			# get player sentences
			for player_id in (1, 2):
				# get player sentence
				if types[player_id] == 'AI':
					sentences[player_id] = get_AI_sentence()
				else:
					sentences[player_id] = remote_play.get_remote_orders(connection)

				# notify other player, if necessary
				if types[3-player_id] == 'remote':
					remote_play.notify_remote_orders(connection, sentences[player_id])
				
			# use player sentences
			for player_id in (1, 2):
				print('Player %d said "%s".' % (player_id, sentences[player_id]))
				
			# wait 3 seconds
			time.sleep(3)
			print('\n------------------------\n')
			
		# close connection
		remote_play.close_connection(connection)

		lift_clod(order,ant_dico,clod_dico)
		drop_clod(order,ant_dico,clod_dico)
		Fight(order,ant_dico)
		Ant_movement(order, ant_dico, clod_dico, ant_dico)
		
		# création nouvelle fourmis 
		Is_ant_dead(ant_dico) 
		New_ant(turn,ant_dico,anthill_dico,clod_dico,Clod_number_around_anthill)

		turn += 1
		time.sleep(1.00)
	End_game(Clod_number_around_anthill,clod_dico,anthill_dico,turn)
	#disconnect
	"""remote_play.close_connection(connection)"""

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

def Is_game_over(Clod_number_around_anthill,clod_dico,anthill_dico,turn):
	"""Verify if the game is over or not.
	parameters
	----------
	Clod_number_around_anthill: Count the number of clods around the anthill(list)
	turn : the number of turn

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
	if turn == 200:
		Is_game_over = True
	return Is_game_over

def End_game(Clod_number_around_anthill,clod_dico,anthill_dico,turn): 
	""" Finish the game and display the winner team.
	Parameter
	---------
	Clod_number_around_anthill: Count the number of clods around the anthill(list)
	clod_dico : The dico of the clods (dict)
	anthill_dico : The dico of the anthills (dict)
	turn : the number of turn (int)
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
	elif turn == 200:
			print("There's no winner")

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
				if clod[0] == ant[0] and clod[1] == ant[1]:
					ant_dico[ant]['clod'] = True

	for order in order_p2:
		if 'drop' in order:
			ant = order[:4]
			ant_x = ant[:1]
			ant_y = ant[3:]
			ant = (ant_x,ant_y)
			for clod in clod_dico:
				#check if there is a clod 
				if clod[0] == ant[0] and clod[1] == ant[1]:
					ant_dico[ant]['clod'] = True
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
				if fighter[0] ==  ant[0] and fighter[1] == ant[1]:
					for b in ant_dico:
						if target[0]== b[0] and target[1] == b[1]:
							distance_x = abs(target[0] - fighter[0])
							distance_y = abs(target[1] - fighter[1])
							if ant_dico[ant]['scope'] <= distance_x and ant_dico[ant]['scope'] <= distance_y:
								damage = ant_dico[ant]['strength']
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
				if fighter[0] ==  ant[0] and fighter[1] == ant[1]:
					for b in ant_dico:
						if target[0]== b[0] and target[1] == b[1]:
							distance_x = abs(target[0] - fighter[0])
							distance_y = abs(target[1] - fighter[1])
							if ant_dico[ant]['scope'] <= distance_x and ant_dico[ant]['scope'] <= distance_y:
								damage = ant_dico[ant]['strength']
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
	Implémentation: Marchal Tom (v.2 02/04/21)
	"""
	order_p1 = order[0]
	order_p2 = order[1]
	for order in order_p1:
		is_there_new_ant = False
		if '@' in order:
			order = order.split(':@')
			coordinate = order[0]
			target = order[1]
			coordinate = coordinate.split('-')
			coordinate_x = int(coordinate[0])
			coordinate_y = int(coordinate[1])
			coordinate = (coordinate_x,coordinate_y)
			target = target.split('-')
			target_x = int(target[0])
			target_y = int(target[1])
			target = (target_x,target_y)
			#check if the ant exist
			for ant in ant_dico:
				if coordinate[0] == ant[0] and coordinate[1] == ant[1]:
					#check if there is no ant at the destination
					for a in ant_dico:
						if target[0] != a[0] and target[1] != a[1]:
							#check if there is a clod where the ant will move
							for clod in clod_dico:
								if target[0] != clod[0]  and target[1] != clod[1]:
									#check if the ant doesn't move at the rival anthill
									for anthill in anthill_dico:
										if ant in ant_dico:
											if ant_dico[ant]['team'] not in anthill:
												if target[0] != anthill[0]  and target[1] != anthill[1]:
													#check if the ant carry a clod
													if ant_dico[ant]['clod'] == True:
														for clod in clod_dico:
																	if clod[0] == ant[0] and clod[1] == ant[1]:
																		clod[0] = target[0]
																		clod[0] = target[1]
													ant = list(ant)
													ant[0] = target[0]
													ant[1] = target[1]
													ant = tuple(ant)
													new_ant = ant
													is_there_new_ant = True
						
								#check if the ant doesn't carry a clod when there is a clod a the target
								else:
									if target not in ant_dico:
										if ant_dico[coordinate]['clod'] == False:
											ant = list(ant)
											ant[0] = target[0]
											ant[1] = target[1]
											ant = tuple(ant)
											new_ant = ant
											is_there_new_ant = True
	if is_there_new_ant:
		ant_dico[new_ant] = ant_dico[coordinate]
		ant_dico.pop(coordinate)
					
										
								
	for order in order_p2:
		if '@' in order:
			order = order.split(':@')
			coordinate = order[0]
			target = order[1]
			coordinate = coordinate.split('-')
			coordinate_x = int(coordinate[0])
			coordinate_y = int(coordinate[1])
			coordinate = (coordinate_x,coordinate_y)
			target = target.split('-')
			target_x = int(target[0])
			target_y = int(target[1])
			target = (target_x,target_y)
			is_there_new_ant = False
			#check if the ant exist
			for ant in ant_dico:
				if coordinate[0] == ant[0] and coordinate[1] == ant[1]:
					#check if there is no ant at the destination
					for a in ant_dico:
						if target[0] != a[0] and target[1] != a[1]:
							#check if there is a clod where the ant will move
							for clod in clod_dico:
								if target[0] != clod[0]  and target[1] != clod[1]:
									#check if the ant doesn't move at the rival anthill
									for anthill in anthill_dico:
										if ant in ant_dico:
											if ant_dico[ant]['team'] not in anthill:
												if target[0] != anthill[0]  and target[1] != anthill[1]:
													#check if the ant carry a clod
													if ant_dico[ant]['clod'] == True:
														for clod in clod_dico:
																	if clod[0] == ant[0] and clod[1] == ant[1]:
																		clod[0] = target[0]
																		clod[0] = target[1]
													ant = list(ant)
													ant[0] = target[0]
													ant[1] = target[1]
													ant = tuple(ant)
													new_ant = ant
													is_there_new_ant = True
						
								#check if the ant doesn't carry a clod when there is a clod a the target
								else:
									if target not in ant_dico:
										if ant_dico[coordinate]['clod'] == False:
											ant = list(ant)
											ant[0] = target[0]
											ant[1] = target[1]
											ant = tuple(ant)
											new_ant = ant
											is_there_new_ant = True
	if is_there_new_ant:
		ant_dico[new_ant] = ant_dico[coordinate]
		ant_dico.pop(coordinate)

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
	Implémentation : Marchal Tom (v.2 02/04/21)
	"""
	#collect the number of clods around the anthills
	clods = Clod_number_around_anthill(clod_dico,anthill_dico)
	if clods == None:
		clods = [0,0]
	clods_blue = clods[0]
	clods_red = clods[1]
	if turn % 5 == 0:
		#create an ant
		for anthill in anthill_dico:
			if anthill == 'anthill_blue':
				if (anthill[0],anthill[1]) not in ant_dico:
					if clods_blue <= 2:
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])] = {}
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['life'] = 3
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['scope'] = 3
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['strength'] = 1
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['clod'] = False
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['team'] = 'blue'
					if clods_blue <= 5 and clods_blue > 3:
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])] = {}
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['life'] = 5
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['scope'] = 3
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['strength'] = 2
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['clod'] = False
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['team'] = 'blue'		
					if clods_blue <= 8 and clods_blue > 6:
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])] = {}
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['life'] = 7
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['scope'] = 3
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['strength'] = 3
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['clod'] = False
						ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['team'] = 'blue'
			if anthill == 'anthill_red':
				if (anthill[0],anthill[1]) not in ant_dico:
					if clods_red <= 2:
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])] = {}
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['life'] = 3
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['scope'] = 3
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['strength'] = 1
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['clod'] = False
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['team'] = 'red'
					if clods_red <= 5 and clods_red > 3:
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])] = {}
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['life'] = 5
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['scope'] = 3
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['strength'] = 2
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['clod'] = False
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['team'] = 'red'
					if clods_red <= 8 and clods_red > 6:
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])] = {}
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['life'] = 7
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['scope'] = 3
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['strength'] = 3
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['clod'] = False
						ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['team'] = 'red'
def Is_ant_dead(ant_dico):
	"""verify if a ant is dead or not.
	parameters
	----------
	ant_dico: dictionary of ant (dict)

	Version
	-------
	Specification : Antoine Boudjenah (v.1 22/02/21)
	Implementation: Antoine Boudjenah (V.1 15/03/21)
	"""

	for cle in ant_dico:
		life = ant_dico[cle]['life']
		if life == 0:
			ant_dico.pop[cle]

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

def Display_interface(map, ant_dico, clod_dico, anthill_dico, shift):
	"""display the interface at the start of the game till the end. 
	parameters
	----------
	cpx_file : The file with the data (file)
	clod_dico: dictionary of the clod (dict)
	anthill_dico: dictionary of anthill (dict)
	ant_dico: dictionary of ant (dict)

	Version
	------- 
	Specification : Antoine Boudjenah (v.2 6/04/21)
	Implémentation : Antoine Boudjenah, Marchal Tom (v.2 6/04/21)
	""" 
	
	#Clear terminal
	print(term.home + term.clear)

	
	row = 0
	col = 0
	line = 0
	line2 = 0
	display_line = 1
	number_grid = 0

	

	#determine the number of columns and rows
	
	columns = int(map[0])
	rows = int(map[1])


	print(columns)
	print(rows)
	print(clod_dico)
	
	#Columns number (cell number) * 4 = pixel number
	#Rows number (cell number) * 2 = pixel number

	pixel_rows = shift + rows * 2
	pixel_columns = shift + columns * 4

	#print the map
	for row in range (shift,pixel_rows+1):
		line = 0
		number_grid += 1/2
		for col in range(shift, pixel_columns+1):
			#Ligne du haut + numérotation
			if row == shift:
				if shift >= 3:
					if line2 == 3:
						print(term.move_xy(col-2, row-1), display_line)
						display_line +=1
						line2 = 0
					else:
						line2 +=1
				#Coin gauche
				if col == shift:
					print(term.move_xy(col, row) + term.red + term.on_black + '┏' + term.normal, end='', flush=True)
				#Coin droit
				elif col == pixel_columns:
					print(term.move_xy(col, row) + term.red + term.on_black + '┓' + term.normal, end='', flush=True)
				#Chars intermédiaires
				elif line != 3:
					print(term.move_xy(col, row) + term.red + term.on_black + '━' + term.normal, end='', flush=True)
					line +=1
				elif line == 3:
					print(term.move_xy(col, row) + term.red + term.on_black + '┳' + term.normal, end='', flush=True)
					line = 0

			#Lignes intermédiaires
			#Soit une ligne d'affichage du jeu avec séparation verticale, soit une ligne de séparation des cases horizontale
			elif (row > shift) and (row < pixel_rows):
				#Lignes paires
				if (row-shift) % 2 == 0:
					#Premier char
					if col == shift:
						print(term.move_xy(col, row) + term.red + term.on_black + '┣' + term.normal, end='', flush=True)
					#Dernier
					elif col == pixel_columns:
						print(term.move_xy(col, row) + term.red + term.on_black + '┫' + term.normal, end='', flush=True)
					#Chars intermédiaires
					elif line != 3:
						print(term.move_xy(col, row) + term.red + term.on_black + '━' + term.normal, end='', flush=True)
						line +=1
					elif line == 3:
						print(term.move_xy(col, row) + term.red + term.on_black + '╋' + term.normal, end='', flush=True)
						line = 0

				#Lignes impaires
				elif (row-shift) % 2 != 0:
					print(term.move_xy(0, row), math.trunc(number_grid))
					#Premier et dernier char
					if (col == shift) or (col == pixel_columns):
						print(term.move_xy(col, row) + term.red + term.on_black + '┃' + term.normal, end='', flush=True)
					#Chars intermédiaires
					elif line != 3:
						print(term.move_xy(col, row) + term.red + term.on_black + ' ' + term.normal, end='', flush=True)
						line +=1
					elif line == 3:
						print(term.move_xy(col, row) + term.red + term.on_black + '┃' + term.normal, end='', flush=True)
						line = 0

			#Dernière ligne
			elif row == pixel_rows:
				#Coin gauche
				if col == shift:
					print(term.move_xy(col, row) + term.red + term.on_black + '┗' + term.normal, end='', flush=True)
				#Coin droit
				elif col == pixel_columns:
					print(term.move_xy(col, row) + term.red + term.on_black + '┛' + term.normal, end='', flush=True)
				#Chars intermédiaires
				elif line != 3:
					print(term.move_xy(col, row) + term.red + term.on_black + '━' + term.normal, end='', flush=True)
					line +=1
				elif line == 3:
					print(term.move_xy(col, row) + term.red + term.on_black + '┻' + term.normal, end='', flush=True)
					line = 0


	#print the anthills
	for anthill in anthill_dico:
		x = anthill_dico[anthill][0]
		y = anthill_dico[anthill][1]
		x = pixel_to_cell(x,y,shift)[0]
		y = pixel_to_cell(x,y,shift)[1]
		if anthill == 'anthill_blue':
			print(term.move_xy(x,y) + term.blue + term.on_green + u"\u25A0" + term.normal, end='', flush=True)
		else:
			print(term.move_xy(x,y) + term.red + term.on_green + u"\u25A0" + term.normal, end='', flush=True)

	#print the ants
	for ant in ant_dico:
		x = ant[0]
		y = ant[1]
		x = pixel_to_cell(x,y,shift)[0]
		y = pixel_to_cell(x,y,shift)[1]
		if ant_dico[ant]['team'] == 'blue':
			if ant_dico[ant]['clod']:
				print(term.move_xy(x,y) + term.brown + term.on_blue + ":" + term.normal, end='', flush=True)
			else:
				print(term.move_xy(x,y) + term.brown + term.on_blue + "." + term.normal, end='', flush=True)
		else:
			if ant_dico[ant]['clod']:
				print(term.move_xy(x,y) + term.brown + term.on_red + ":" + term.normal, end='', flush=True)
			else:
				print(term.move_xy(x,y) + term.brown + term.on_red + "." + term.normal, end='', flush=True)

	#print the clods
	for clod in clod_dico:
		x = clod[0]
		y = clod[1]
		x = pixel_to_cell(x,y,shift)[0]
		y = pixel_to_cell(x,y,shift)[1]
		print(term.move_xy(x,y) + term.black + term.on_green + "●" + term.normal, end='', flush=True)


		############ Fonction d'affichage à chaque tour #################
		# is_ant = False
		# for ant in ant_dico:
		# 	if x != ant[0] or y != ant[1]:
		# 		is_ant = True

		# if is_ant:
		# 	x = x * 2 + shift - 1
		# 	y = y * 4 + shift - 2
		# 	print(term.move_xy(x,y) + term.black + term.on_green + "●" + term.normal, end='', flush=True)

	print(term.move_xy(0, rows + shift + 2))

def pixel_to_cell(x,y,shift):
	"""
	Parameters
	----------
	x : coordinate x (int)
	y : coordinate y (int)
	shift : shift of the grid (int)
	
	return
	------
	x : coordinate x (int)
	y : coordinate y (int)

	version
	-------
	Specification: Antoine Boudjenah, Tom Marchal (v.1 06/04/21)
	Implémentation: Antoine Boudjenah, Tom Marchal (v.1 06/04/21)
	"""
	x = x * 4 + shift - 2
	y = y * 2 + shift - 1

	return x,y

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
	map : The coordinate of the map (list)

	version
	-------
	Specification: Marchal Tom (v.2 04/04/21)
	Implémentation: Marchal Tom (v.1 04/04/21)
	"""
	#collect the data of the game
	fh = open('.\data_game.txt', 'r')
	lines = fh.readlines()
	fh.close()
	#create the dictionnaries
	map = lines[1]
	map = map.split()
	clod_dico = {}
	anthill_dico = {}
	ant_dico = {}
	nb_lines = 0
	for line in lines:
		#insert data in anthill_dico
		if 'anthills' in line:
			anthill_blue = lines[nb_lines + 1]
			anthill_blue = anthill_blue.split()
			anthill_blue = (int(anthill_blue[0]), int(anthill_blue[1]))
			anthill_dico['anthill_blue'] = anthill_blue
			anthill_red = lines[nb_lines + 2]
			anthill_red = anthill_red.split()
			anthill_red = (int(anthill_red[0]), int(anthill_red[1]))
			anthill_dico['anthill_red'] = anthill_red
		#insert data in clod_dico
		if 'clods' in line:
			for clod in range(nb_lines + 1, len(lines)):
				clod = lines[clod]
				clod = clod.split()
				coordinate = (int(clod[0]), int(clod[1]))
				weight = int(clod[2])
				clod_dico[coordinate] = weight
		nb_lines += 1
	#create an ant at each anthill
	for anthill in anthill_dico:
		if anthill == 'anthill_blue':
			ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])] = {}
			ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['life'] = 3
			ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['scope'] = 3
			ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['strength'] = 1	
			ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['clod'] = False
			ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['team'] = 'blue'
		else:
			ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])] = {}
			ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['life'] = 3
			ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['scope'] = 3
			ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['strength'] = 1	
			ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['clod'] = False
			ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['team'] = 'red'
	return ant_dico, anthill_dico, clod_dico, map

def cpx_file():
	"""Create the file with all the data.
	
	Version 
	-------
	Spécification : Marchal Tom (v.1 26/03/21)
	Implémentation : Marchal Tom (v.1 06/03/21)
	"""
	#create coordinate of the map
	map_x = random.randint(20,40)
	map_y = random.randint(20,40)
	#create the coordinate of the anthills
	anthill_blue= [random.randint(1,map_x),  random.randint(1,int(map_y/3))]
	anthill_red= [random.randint(1,map_x),  random.randint(int(map_y/3*2),int(map_y))]
	#create the number of clods
	clods_number = random.randint(15,int(((map_x+map_y)/2)))
	#create the coordinate of the clods
	clods = []
	for clod in range (0,clods_number+1):
		clod = [random.randint(1,map_x),  random.randint(1,map_y)]
		#verify if the coordinate != the anthills coordinates
		while clod[0] == anthill_blue[0] or clod[0] == anthill_red[0] and clod[1] == anthill_blue[1] or clod[1] == anthill_red[1]:
			clod = [random.randint(1,map_x),  random.randint(1,map_y)]
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
	
def create_server_socket(local_port, verbose):
    """Creates a server socket.
    
    Parameters
    ----------
    local_port: port to listen to (int)
    verbose: True if verbose (bool)
    
    Returns
    -------
    socket_in: server socket (socket.socket)
    
    """
    
    socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # deal with a socket in TIME_WAIT state

    if verbose:
        print(' binding on local port %d to accept a remote connection' % local_port)
    
    try:
        socket_in.bind(('', local_port))
    except:
        raise IOError('local port %d already in use by your group or the referee' % local_port)
    socket_in.listen(1)
    
    if verbose:
        print('   done -> can now accept a remote connection on local port %d\n' % local_port)
        
    return socket_in


def create_client_socket(remote_IP, remote_port, verbose):
    """Creates a client socket.
    
    Parameters
    ----------
    remote_IP: IP address to send to (int)
    remote_port: port to send to (int)
    verbose: True if verbose (bool)
    
    Returns
    -------
    socket_out: client socket (socket.socket)
    
    """

    socket_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # deal with a socket in TIME_WAIT state
    
    connected = False
    msg_shown = False
    
    while not connected:
        try:
            if verbose and not msg_shown:
                print(' connecting on %s:%d to send orders' % (remote_IP, remote_port))
                
            socket_out.connect((remote_IP, remote_port))
            connected = True
            
            if verbose:
                print('   done -> can now send orders to %s:%d\n' % (remote_IP, remote_port))
        except:
            if verbose and not msg_shown:
                print('   connection failed -> will try again every 100 msec...')
                
            time.sleep(.1)
            msg_shown = True
            
    return socket_out
    
    
def wait_for_connection(socket_in, verbose):
    """Waits for a connection on a server socket.
    
    Parameters
    ----------
    socket_in: server socket (socket.socket)
    verbose: True if verbose (bool)
    
    Returns
    -------
    socket_in: accepted connection (socket.socket)
    
    """
    
    if verbose:
        print(' waiting for a remote connection to receive orders')
        
    socket_in, remote_address = socket_in.accept()
    
    if verbose:
        print('   done -> can now receive remote orders from %s:%d\n' % remote_address)
        
    return socket_in            


def create_connection(your_group, other_group=0, other_IP='127.0.0.1', verbose=False):
    """Creates a connection with a referee or another group.
    
    Parameters
    ----------
    your_group: id of your group (int)
    other_group: id of the other group, if there is no referee (int, optional)
    other_IP: IP address where the referee or the other group is (str, optional)
    verbose: True only if connection progress must be displayed (bool, optional)
    
    Returns
    -------
    connection: socket(s) to receive/send orders (dict of socket.socket)
    
    Raises
    ------
    IOError: if your group fails to create a connection
    
    Notes
    -----
    Creating a connection can take a few seconds (it must be initialised on both sides).
    
    If there is a referee, leave other_group=0, otherwise other_IP is the id of the other group.
    
    If the referee or the other group is on the same computer than you, leave other_IP='127.0.0.1',
    otherwise other_IP is the IP address of the computer where the referee or the other group is.
    
    The returned connection can be used directly with other functions in this module.
            
    """
    
    # init verbose display
    if verbose:
        print('\n[--- starts connection -----------------------------------------------------\n')
        
    # check whether there is a referee
    if other_group == 0:
        if verbose:
            print('** group %d connecting to referee on %s **\n' % (your_group, other_IP))
        
        # create one socket (client only)
        socket_out = create_client_socket(other_IP, 42000+your_group, verbose)
        
        connection = {'in':socket_out, 'out':socket_out}
        
        if verbose:
            print('** group %d successfully connected to referee on %s **\n' % (your_group, other_IP))
    else:
        if verbose:
            print('** group %d connecting to group %d on %s **\n' % (your_group, other_group, other_IP))

        # create two sockets (server and client)
        socket_in = create_server_socket(42000+your_group, verbose)
        socket_out = create_client_socket(other_IP, 42000+other_group, verbose)
        
        socket_in = wait_for_connection(socket_in, verbose)
        
        connection = {'in':socket_in, 'out':socket_out}

        if verbose:
            print('** group %d successfully connected to group %d on %s **\n' % (your_group, other_group, other_IP))
        
    # end verbose display
    if verbose:
        print('----------------------------------------------------- connection started ---]\n')

    return connection
        
        
def bind_referee(group_1, group_2, verbose=False):
    """Put a referee between two groups.
    
    Parameters
    ----------
    group_1: id of the first group (int)
    group_2: id of the second group (int)
    verbose: True only if connection progress must be displayed (bool, optional)
    
    Returns
    -------
    connections: sockets to receive/send orders from both players (dict)
    
    Raises
    ------
    IOError: if the referee fails to create a connection
    
    Notes
    -----
    Putting the referee in place can take a few seconds (it must be connect to both groups).
        
    connections contains two connections (dict of socket.socket) which can be used directly
    with other functions in this module.  connection of first (second) player has key 1 (2).
            
    """
    
    # init verbose display
    if verbose:
        print('\n[--- starts connection -----------------------------------------------------\n')

    # create a server socket (first group)
    if verbose:
        print('** referee connecting to first group %d **\n' % group_1)        

    socket_in_1 = create_server_socket(42000+group_1, verbose)
    socket_in_1 = wait_for_connection(socket_in_1, verbose)

    if verbose:
        print('** referee succcessfully connected to first group %d **\n' % group_1)        
        
    # create a server socket (second group)
    if verbose:
        print('** referee connecting to second group %d **\n' % group_2)        

    socket_in_2 = create_server_socket(42000+group_2, verbose)
    socket_in_2 = wait_for_connection(socket_in_2, verbose)

    if verbose:
        print('** referee succcessfully connected to second group %d **\n' % group_2)        
    
    # end verbose display
    if verbose:
        print('----------------------------------------------------- connection started ---]\n')

    return {1:{'in':socket_in_1, 'out':socket_in_1},
            2:{'in':socket_in_2, 'out':socket_in_2}}


def close_connection(connection):
    """Closes a connection with a referee or another group.
    
    Parameters
    ----------
    connection: socket(s) to receive/send orders (dict of socket.socket)
    
    """
    
    # get sockets
    socket_in = connection['in']
    socket_out = connection['out']
    
    # shutdown sockets
    socket_in.shutdown(socket.SHUT_RDWR)    
    socket_out.shutdown(socket.SHUT_RDWR)
    
    # close sockets
    socket_in.close()
    socket_out.close()
    
    
def notify_remote_orders(connection, orders):
    """Notifies orders to a remote player.
    
    Parameters
    ----------
    connection: sockets to receive/send orders (dict of socket.socket)
    orders: orders to notify (str)
        
    Raises
    ------
    IOError: if remote player cannot be reached
    
    """

    # deal with null orders (empty string)
    if orders == '':
        orders = 'null'
    
    # send orders
    try:
        connection['out'].sendall(orders.encode())
    except:
        raise IOError('remote player cannot be reached')


def get_remote_orders(connection):
    """Returns orders from a remote player.

    Parameters
    ----------
    connection: sockets to receive/send orders (dict of socket.socket)
        
    Returns
    ----------
    player_orders: orders given by remote player (str)

    Raises
    ------
    IOError: if remote player cannot be reached
            
    """
   
    # receive orders    
    try:
        orders = connection['in'].recv(65536).decode()
    except:
        raise IOError('remote player cannot be reached')
        
    # deal with null orders
    if orders == 'null':
        orders = ''
        
    return orders
def IA_naive(ant_dico, number_of_the_player):
	""" The IA will play instead of a human, it will move the ants.

	
	Spécification
	-------------
	ant_dico : The dico of the ants (dict)
	number_of_the_player: The number of the player (int)
	return
	------
	order : The order of the IA (list)

	Version
	-------
	Spécification : Marchal Tom (28/03)
	Implémentation : MArchal Tom (28/03)
	"""
	order = ""
	ants = []
	if number_of_the_player == "p1":
		for ant in ant_dico:
			if ant_dico[ant]['team'] == 'blue':
				ants.append(ant)
	else:
		for ant in ant_dico:
			if ant_dico[ant]['team'] == 'red':
				ants.append(ant)
	for ant in ants:
		x = ant[0]
		y = ant[1]
		order += "%d-%d:@"%(x,y)
		move = random.choice(((-1, 0), (1, 0), (0, -1), (0, 1)))
		if move[0] != 0:
			x += move[0]
		if move[1] != 0:
			y += move[1]
		order += "%d-%d"%(x,y)
	return order

def get_AI_sentence():
	""""""
main_game(cpx_file,input('The number of the first group'),input('The type of user (P1)'),input('The number of the second group'), input('The type of user (P2)'))
