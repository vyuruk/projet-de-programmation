import blessed, math, os, time, random, remote_play

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

	Is_human = False
	if type_1 == "human" and type_2 == "human":
		Is_human = True

	Is_IA = False
	if type_1 == "IA" and type_2 == "IA":
		Is_IA = True
	
	Display_interface(map, ant_dico, clod_dico, anthill_dico, shift)
	Display_refresh(ant_dico,clod_dico,anthill_dico,shift)
	while not Is_game_over(Clod_number_around_anthill,clod_dico,anthill_dico,turn):	
		
		if Is_human:
			y = int(map[1]) + 1
			y = pixel_to_cell_y(y,shift)
			print(term.move_xy(0,y) + term.black + term.on_black + "" + term.normal, end='', flush=True)
			order_player_1 = input("Indiquer vos ordres (P1)")
			#order_player_2 = get_AI_sentence(ant_dico,anthill_dico,clod_dico,2)
			order_player_2 = input("Indiquer vos ordres (P2)")
			orders = player_order(order_player_1,order_player_2)

		if Is_IA:
			order_player_1 = get_AI_sentence(ant_dico,anthill_dico,clod_dico,1)
			order_player_2 = get_AI_sentence(ant_dico,anthill_dico,clod_dico,2)
			orders = player_order(order_player_1,order_player_2)

		is_remote = False
		# create connection
		if type_1 == 'remote':
			connection = remote_play.create_connection(group_2, group_1, verbose=True)
			is_remote = True
		if type_2 == 'remote':
			connection = remote_play.create_connection(group_1, group_2, verbose=True)
			is_remote = True
		if is_remote:
			# get player types
			types = {1:type_1, 2:type_2}

			# main loop (until one of both players says "stop")
			sentences = {1:'', 2:''}
			# get player sentences
			for player_id in (1, 2):
				# get player sentence
				if types[player_id] == 'AI':
					sentences[player_id] = get_AI_sentence(ant_dico,anthill_dico,clod_dico,player_id)
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
				

		for team in range(2):
			for order in orders[team]:
				if 'lift' in order:
					#LEVER
					order = [order]
					Lift_clod(orders[team],ant_dico,clod_dico)
				elif 'drop' in order:
					#POSER
					order = [order]
					Drop_clod(order,ant_dico,clod_dico)
				elif '*' in order:
					#ATTAQUER
					order = [order]
					Fight(order,ant_dico)
				elif '@' in order:
					#BOUGER
					order = [order]
					Ant_movement(map, order, ant_dico, clod_dico, ant_dico, shift, team)

		#Création nouvelle fourmis
		Display_refresh(ant_dico,clod_dico,anthill_dico,shift)
		Is_ant_dead(ant_dico) 
		New_ant(turn,ant_dico,anthill_dico,clod_dico,Clod_number_around_anthill,)

		turn += 1
		time.sleep(1.00)

	End_game(Clod_number_around_anthill,clod_dico,anthill_dico,turn,group_1,group_2)
	#disconnect
	remote_play.close_connection(connection)


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
	nbr_cld_b = Clod_number_around_anthill(clod_dico,anthill_dico, 'blue')
	nbr_cld_r = Clod_number_around_anthill(clod_dico,anthill_dico, 'red')

	Is_game_over = False
	if nbr_cld_r == 8 or nbr_cld_b == 8:
		Is_game_over = True
	if turn == 200:
		Is_game_over = True
	return Is_game_over

def End_game(Clod_number_around_anthill,clod_dico,anthill_dico,turn,group_1,group_2): 
	""" Finish the game and display the winner team.
	Parameter
	---------
	Clod_number_around_anthill: Count the number of clods around the anthill(list)
	clod_dico : The dico of the clods (dict)
	anthill_dico : The dico of the anthills (dict)
	turn : the number of turn (int)
	group_1: the number of the first group (int)
	group_2: the number of the second group (int)

	Version
	-------
	Specification : Yuruk Valentin, Marchal Tom (v.2 16/32/21)
	Implementation : Yuruk Valentin, Antoine Boudjenah (V.3 17/04/21)
	"""

	#R if red team win, B if bleu team win, E if there's no winner(bool)

	nbr_cld_b = Clod_number_around_anthill(clod_dico,anthill_dico, 'blue')
	nbr_cld_r = Clod_number_around_anthill(clod_dico,anthill_dico, 'red')
	if nbr_cld_r == 8: 
		if nbr_cld_b == 8:
			#No winner
			print("There's no winner")
		else:
			#Blue team win
			print("The Blue team is the winner(group %d)"%group_1)	
	elif nbr_cld_b == 8:
		#Red team win
		print("The Red team is the winner(group %d)"%group_2)	
	elif turn == 200:
		if nbr_cld_r == nbr_cld_b:
			print("There's no winner")
		elif nbr_cld_r > nbr_cld_b:
			#Red team win
			print("The Red team is the winner(group %d)"%group_2)
		else:
			#Blue team win
			print("The Blue team is the winner(group %d)"%group_1)	

def Drop_clod(orders,ant_dico,clod_dico):
	""" Check if the ant can drop the clod.

	parameter
	---------
	orders: The order of the player (list)
	ant_dico: The dico of the ants (dict)
	clod_dico: The dico of the clods (dict)

	version
	-------
	Specification : Marchal Tom (v.1 26/02/21)
	Implémentation : Marchal Tom (v.1 26/03/21), Antoine Boudjenah (v.2 17/04/21)
	"""
	
	for order in orders:
		order = order.split(':')
		coordinate = order[0].split('-')
		coordinate = (int(coordinate[0]),int(coordinate[1]))
		#Si une fourmi existe à cet endroit et qu'elle porte une motte de terre
		if Check_something(ant_dico, coordinate, 'clod', True):
			#On dépose la motte de terre
			ant_dico[coordinate]['clod'] = False

def Lift_clod(orders,ant_dico,clod_dico):
	""" 
	Allow an ant to lift a clod

	parameter
	---------
	orders: The order of the player (list)
	ant_dico: The dico of the ants (dict)
	clod_dico: The dico of the clods (dict)

	version
	-------
	Specification : Marchal Tom (v.1 26/02/21)
	Implémentation : Marchal Tom (v.1 26/03/21), Antoine Boudjenah (v.2 17/04/21)
	"""
	for order in orders:
		order = order.split(':')
		coordinate = order[0].split('-')
		coordinate = (int(coordinate[0]),int(coordinate[1]))
		#Si une fourmi existe à cet endroit
		if Check_something(ant_dico, coordinate):
			#Si il y a une motte de terre à cet endroit
			if Check_something(clod_dico, coordinate):
				#Si la fourmi est assez forte
				strength = ant_dico[coordinate]['strength']
				weight = clod_dico[coordinate]
				if strength >= weight:
					ant_dico[coordinate]['clod'] = True

def Fight(orders, ant_dico): 
	""" Check if the ant can attack the other one, create a list of the ant who take damage if he can.

	Parameter
	---------
	orders : The order of the player (list) 
	ant_dico : The dico of the ants (dict)

	Version
	-------
	Specification : Marchal Tom, Valentin Yuruk (v.2 19/03/21)
	Implémentation : Valentin Yuruk, Marchal Tom (v.1 26/03/21), Antoine Boudjenah (v.2 17/04/21)
	"""
	for order in orders:
		order = order.split(':*')
		coordinate = order[0]
		target = order[1]
		coordinate = coordinate.split('-')
		coordinate = (int(coordinate[0]),int(coordinate[1]))
		target = target.split('-')
		target = (int(target[0]),int(target[1]))
		#On vérifie qu'il y a une fourmi aux coordonnées
		if Check_something(ant_dico, coordinate):
			#On vérifie qu'il y a une fourmi sur aux coordonnées de la cible
			if Check_something(ant_dico, target):
				#On vérifie si la cible est à portée de tir
				distance_x = abs(target[0] - coordinate[0])
				distance_y = abs(target[1] - coordinate[1])
				scope = ant_dico[coordinate]['scope']
				if scope >= distance_x and scope >= distance_y:
					damage = ant_dico[coordinate]['strength']
					life = ant_dico[target]['life']
					life = life - damage
					ant_dico[target]['life'] = life
				
def Check_something(dico, coordinate, key='###', result='###'):
	"""
	Check many things, like if something is in a case or if something has an attribut to check

	Parameter
	---------
	dico : Dictionnary of the thing to check
	coordinate : Coordinates where to look (list)
	key : Key to acces in the dico (string)
	result : To check if the element finded is equal to the element wanted (str)


	Return
	-------
	Check_something : True if character is validated, False otherwise (bool)

	Version
	-------
	Spécification : Valentin Yuruk, Antoine Boudjenah (v.1 17/04/21)
	Implémentation : Antoine Boudjenah (v.1 17/04/21)
	"""
	#### NE MARCHE PAS AVEC ANTHILL
	Check_something = False
	for element in dico:
		if coordinate[0] == element[0] and coordinate[1] == element[1]:
			if key != '###':
				if dico[element][key] == result:
						Check_something = True
						break
			else:
				Check_something = True
				break
	return Check_something

def Is_in_grid(map, coordinate):
	"""
	Check if coordinates are in the grid or not

	Parameter
	---------
	map : map :  Data of the map (list)
	coordinate : Coordinate to check (list)

	Return
	-------
	Is_in_grid : True if coordinates are in the grid, False otherwise (bool)

	Version
	-------
	Specification : Antoine Boudjenah (v.1 17/04/21)
	Implémentation: Antoine Boudjenah (v.1 17/04/21)
	"""
	columns = int(map[0])
	rows = int(map[1])

	Is_in_grid = False
	if coordinate[0] > 0 and coordinate[0] < columns + 1:
		if coordinate[1] > 0 and coordinate[1] < rows + 1:
			Is_in_grid = True
	
	return Is_in_grid

def Is_target_valid(coordinate, target):
	"""
	Check if the target is valid or not

	Parameter
	---------
	Coordinate : Where the ant is currently
	Target : Where the ant would like to move

	Return
	-------
	Is_target_valid : True if the ant can move at theses coorinates, False otherwise (bool)

	Version
	-------
	Specification : Antoine Boudjenah (v.1 17/04/21)
	Implémentation: Antoine Boudjenah (v.1 17/04/21)
	"""
	Is_target_valid = False
	if abs(target[0] - coordinate[0]) == 0 or 1:
		if abs(target[1] - coordinate[1]) == 0 or 1:
			Is_target_valid = True
			
	return Is_target_valid

def Is_anthill(anthill_dico, coordinate, team):
	"""
	Check if an enemy anthill is on coordinates

	Parameter
	---------
	anthill_dico : The dico oh the anthills (dict)
	coordinate : the coordinate of the anthill (int)
	team : The team of the anthill (str)

	Return 
	------
	Is_anthill : True if there is an anthill(bool)

	Version
	-------
	Spécification : Marchal Tom (v.2 25/04/21), Antoine Boudjenah (v.1, 20/04/21)
	Implémentation: Antoine Boudjenah (v.1 20/04/21)
	"""
	Is_anthill = False
	if team == 'blue':
		team = 'anthill_red'
	else:
		team = 'anthill_blue'
	for anthill in anthill_dico:
		ennemi_anthill = anthill_dico[anthill]
		if ennemi_anthill == coordinate:
			Is_anthill = True
	return Is_anthill

def Ant_movement(map, orders, ant_dico, clod_dico, anthill_dico, shift, team): 
	""" 
	Check if the ant can move where the order indicate.

	Parameter
	---------
	map :  Data of the map (list)
	orders : The order of the player (list)
	ant_dico : The dico of the ants (dict)
	clod_dico : The dico of the clods(dict)
	anthill_dico : the dico of the anthills(dict)
	team: The number of the team (int)

	Version
	-------
	Specification : Marchal Tom (v.2 19/03/21), Valentin Yuruk ( v.3 23/04/21)
	Implémentation: Marchal Tom (v.2 02/04/21), Antoine Boudjenah (v.3 17/04/21)
	"""

	for order in orders:
		if team == 0 : 
			team = 'blue'
		else : 
			team = 'red'
		order = order.split(':@')
		coordinate = order[0]
		target = order[1]
		coordinate = coordinate.split('-')
		coordinate = (int(coordinate[0]),int(coordinate[1]))
		target = target.split('-')
		target = (int(target[0]),int(target[1]))

		#Verifier si la fourmi existe dans la bonne équipe
		if Check_something(ant_dico, coordinate, 'team', team):
			#On regarde si il n'y a rien d'illégal à la destination
			#On commence par regarder si la destination se trouve à l'intérieur du plateau
			if Is_in_grid(map, target):
				#On vérifie que l'objectif est valide ( distance )
				if Is_target_valid(coordinate, target): #Si objectif valide
					#On vérifie qu'il n'y ait pas de fourmi à la destination
					if not Check_something(ant_dico, target): #Si pas de fourmi
						#On vérifie qu'il n'y ait pas de fourmilière ennemie à la destination
						if not Is_anthill(anthill_dico, target, team):
							#Si une motte de terre sur la même case
							if Check_something(clod_dico, coordinate):
								#Si la fourmi porte la motte de terre
								if Check_something(ant_dico, coordinate, 'clod', True):
									#si il n'y a pas de motte de terre à la destination
									if not Check_something(clod_dico, target):
										#On déplace la motte de terre avec la fourmi
										new_position = [target[0],target[1]]
										new_position = tuple(new_position)
										clod_dico[new_position] = clod_dico[coordinate]
										clod_dico.pop(coordinate)
							new_position = [target[0],target[1]]
							new_position = tuple(new_position)
							ant_dico[new_position] = ant_dico[coordinate]
							ant_dico.pop(coordinate)
							data = [coordinate, target]
							for print_in_black in data:
								x = pixel_to_cell_x(print_in_black[0], shift)
								y = pixel_to_cell_y(print_in_black[1], shift)
								print(term.move_xy(x, y) + term.on_black + ' ' + term.normal, end='', flush=True)	
			
def New_ant(turn, ant_dico, anthill_dico, clod_dico,Clod_number_around_anthill):
	"""the function that will count clods around the anthills.
	parameters
	----------
	clod_dico: dictionary of the clod (dict)
	anthill_dico: dictionary of anthill (dict)
    turn: new turn in the game (int)
    Clod_number_around_anthill: number of clods around the anthill(int)

	return
	------
	nbr_cld_r: the number of clod around the red anthill(int)
	nbr_cld_b: the number of clod around the blue anthill(int)
	
	Version
	------- 
	Specification : Antoine Boudjenah, Marchal Tom (v.1 22/02/21), Valentin Yuruk (v.2 24/02/21)
	Implémentation : Marchal Tom (v.1 26/03/21)
	"""
	clods_blue = Clod_number_around_anthill(clod_dico, anthill_dico, 'blue')
	clods_red = Clod_number_around_anthill(clod_dico, anthill_dico, 'red')


	if turn % 5 == 0:
		#create an ant
		for ant in ant_dico:
			if ant[0] != anthill_dico['anthill_blue'][0] or ant[1] != anthill_dico['anthill_blue'][1]:
				if clods_blue <= 2:
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])] = {}
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['life'] = 3
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['scope'] = 3
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['strength'] = 1
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['clod'] = False
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['team'] = 'blue'
					break
				if clods_blue <= 5 and clods_blue > 3:
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])] = {}
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['life'] = 5
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['scope'] = 3
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['strength'] = 2
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['clod'] = False
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['team'] = 'blue'
					break
				if clods_blue <= 8 and clods_blue > 6:
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])] = {}
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['life'] = 7
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['scope'] = 3
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['strength'] = 3
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['clod'] = False
					ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['team'] = 'blue'
					break
		for ant in ant_dico:
			if ant[0] != anthill_dico['anthill_red'][0] or ant[1] != anthill_dico['anthill_red'][1]:
				if clods_red <= 2:
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])] = {}
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['life'] = 3
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['scope'] = 3
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['strength'] = 1
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['clod'] = False
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['team'] = 'red'
					break
				if clods_red <= 5 and clods_red > 3:
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])] = {}
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['life'] = 5
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['scope'] = 3
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['strength'] = 2
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['clod'] = False
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['team'] = 'red'
					break
				if clods_red <= 8 and clods_red > 6:
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])] = {}
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['life'] = 7
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['scope'] = 3
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['strength'] = 3
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['clod'] = False
					ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['team'] = 'red'
					break
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

def Display_interface(map, ant_dico, clod_dico, anthill_dico, shift):
	"""display the interface at the start of the game till the end. 
	
	parameters
	----------
	map : Dimensions of the map (list)
	anthill_dico : dictionary of anthill (dict)
	shift : The shift of the grid (int)
    clod_dico : dictionary of the clod (dict)
	ant_dico: dictionary of ant (dict)

	Version
	------- 
	Specification : Antoine Boudjenah, (v.2 6/04/21) Valentin Yuruk (v.3 23/04/21)
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

def Display_refresh(ant_dico, clod_dico, anthill_dico, shift):
	"""display the interface at the start of the game till the end. 
	
	parameters
	----------
	clod_dico: dictionary of the clod (dict)
	ant_dico: dictionary of ant (dict)
    anthill_dico: dictionary of the anthill (dict)
	shift : The shift of the grid (int)

	Version
	------- 
	Specification : Antoine Boudjenah (v.1 6/04/21), Valentin Yuruk (v.2 23/04/21)
	Implémentation : Antoine Boudjenah (v.2 2/05/21)
	"""

	#print the ants
	for ant in ant_dico:
		x = pixel_to_cell_x(ant[0],shift)
		y = pixel_to_cell_y(ant[1],shift)
		if ant_dico[ant]['life'] <= 0:
			if ant_dico[ant]['clod']:
				print(term.move_xy(x,y) + term.white + term.on_black + "●" + term.normal, end='', flush=True)
			else:
				print(term.move_xy(x,y) + term.black + term.on_black + " " + term.normal, end='', flush=True)
		if ant_dico[ant]['team'] == 'blue' and ant_dico[ant]['life'] > 0:
			#Si la fourmi porte une motte de terre
			if ant_dico[ant]['clod']:
				print(term.move_xy(x,y) + term.brown + term.on_blue + ":" + term.normal, end='', flush=True)
			else:
				print(term.move_xy(x,y) + term.brown + term.on_blue + "." + term.normal, end='', flush=True)
		elif ant_dico[ant]['team'] == 'red' and ant_dico[ant]['life'] > 0:
			if ant_dico[ant]['clod']:
				print(term.move_xy(x,y) + term.brown + term.on_red + ":" + term.normal, end='', flush=True)
			else:
				print(term.move_xy(x,y) + term.brown + term.on_red + "." + term.normal, end='', flush=True)

	#print the anthills
	for anthill in anthill_dico:
		x = pixel_to_cell_x(anthill_dico[anthill][0],shift)
		y = pixel_to_cell_y(anthill_dico[anthill][1],shift)
		if anthill == 'anthill_blue':
			print(term.move_xy(x,y) + term.blue + term.on_black + u"\u25A0" + term.normal, end='', flush=True)
		else:
			print(term.move_xy(x,y) + term.red + term.on_black + u"\u25A0" + term.normal, end='', flush=True)

	#print the clods
	for clod in clod_dico:
		coordinate = [clod[0], clod[1]]
		x = pixel_to_cell_x(clod[0],shift)
		y = pixel_to_cell_y(clod[1],shift)
		if Check_something(ant_dico,coordinate):
			#Si fourmi aux coordonnées qui ne porte pas de motte de terre
			if Check_something(ant_dico, coordinate, 'clod', False):
				#Si team bleue
				if Check_something(ant_dico, coordinate, 'team', 'blue'):
					print(term.move_xy(x,y) + term.white + term.on_blue + "●" + term.normal, end='', flush=True)
				#Si team rouge
				else:
					print(term.move_xy(x,y) + term.white + term.on_red + "●" + term.normal, end='', flush=True)
		#Si pas de fourmis aux coordonnées
		else:
			print(term.move_xy(x,y) + term.white + term.on_black + "●" + term.normal, end='', flush=True)

		
def pixel_to_cell_x(x,shift):
	""" Convert the pixel coordinate into cell coordinate.
	Parameters
	----------
	x : coordinate of x in pixel(int)
	shift : shift of the grid (int)
	
	return
	------
	x : coordinate of x in cell(int)

	version
	-------
	Specification: Antoine Boudjenah, Tom Marchal (v.1 06/04/21), Tom Marchal (v.2 24/04/21)
	Implémentation: Antoine Boudjenah, Tom Marchal (v.1 06/04/21)
	"""
	x = x * 4 + shift - 2

	return x

def pixel_to_cell_y(y,shift):
	""" Convert the pixel coordinate into cell coordinate
	Parameters
	----------
	y : coordinate of y in pixel (int)
	shift : shift of the grid (int)
	
	return
	------
	y : coordinate of y in cell(int)

	version
	-------
	Specification: Antoine Boudjenah, Tom Marchal (v.1 06/04/21), Tom Marchal (v.2 24/04/21)
	Implémentation: Antoine Boudjenah, Tom Marchal (v.1 06/04/21)
	"""

	y = y * 2 + shift - 1

	return y

def Is_ant_dead(ant_dico):
	"""verify if an ant is dead or not.

	parameters
	----------
	ant_dico: dictionary of ant (dict)
	
	Version
	-------
	Specification : Antoine Boudjenah (v.1 22/02/21), Valentin Yuruk(v.2 23/04/21)
	Implementation: Antoine Boudjenah (V.1 15/03/21), Marchal Tom (v.2 03/05/21)
	"""
	cles = []
	for cle in ant_dico:
		life = ant_dico[cle]['life']
		if life <= 0:
			cles.append(cle)
	if len(cles) > 0:
		for cle in cles:
			del ant_dico[cle]

def Clod_number_around_anthill(clod_dico, anthill_dico, team):
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
	Implémentation : Marchal Tom (v.1 26/03/21), Antoine Boudjenah(V.2 02/05/21)
	"""
	team = 'anthill_%s'%team
	coordinate = [anthill_dico[team][0], anthill_dico[team][1]]
	nbr_cld = 0
	
	for x in range(0,3):
		for y in range(0,3):
			coordinate = [anthill_dico[team][0]+x-1,anthill_dico[team][1]+y-1]
			if Check_something(clod_dico, coordinate):
				nbr_cld += 1

	return nbr_cld
	
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
			ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['strength'] = 10
			ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['clod'] = False
			ant_dico[(anthill_dico['anthill_blue'][0],anthill_dico['anthill_blue'][1])]['team'] = 'blue'
		else:
			ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])] = {}
			ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['life'] = 3
			ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['scope'] = 3
			ant_dico[(anthill_dico['anthill_red'][0],anthill_dico['anthill_red'][1])]['strength'] = 10
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
	map_x = random.randint(10,20)
	map_y = random.randint(10,20)
	#create the coordinate of the anthills
	anthill_blue= [random.randint(2,map_x),  random.randint(2,int(map_y/3))]
	anthill_red= [random.randint(2,map_x),  random.randint(int(map_y/3*2),int(map_y)-1)]
	#create the number of clods
	clods_number = random.randint(5,int(((map_x+map_y)/2)))
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

def get_coordinate(coordinate, target):
	"""
	"""
	new_position = coordinate
	distance = (target[0]-coordinate[0], target[1]-coordinate[1])

	if distance[0] > 0: 
		new_position[0] = coordinate[0] + 1
	elif distance[0] < 0 : 
		new_position[0] = coordinate[0] - 1
	if distance[1] > 0 : 
		new_position[1] = coordinate[1] + 1
	elif distance[1] < 0 : 
		new_position[1] = coordinate[1] - 1
	return new_position

def Is_around(anthill, element):
	"""
	#Vérifier si la motte de terre n'est pas autour de la fourmilière
	"""
	is_around = False
	for x in range(0,3):
		for y in range(0,3):
			target = [anthill[0] + x - 1 , anthill[1] + y - 1]
			if element[0] == target[0] and element[1] == target[1]:
				is_around = True
	return is_around

def Is_nearest(coordinate, element, dico):
	"""
	#regarde si la motte est la plus proche
	elemebnt = clod ...
	dico
	coordinate
	"""
	is_nearest = True
	dist_x = abs(coordinate[0] - element[0])
	dist_y = abs(coordinate[1] - element[1])

	for elmt in dico:
		x = abs(coordinate[0] - elmt[0])
		y = abs(coordinate[1] - elmt[1])
		if dist_x > x and dist_y > y:
			is_nearest = False

	return is_nearest


def get_AI_sentence(ant_dico,anthill_dico,clod_dico,player_id):
	""" Get the orders given by the IA
	
	Parameters
	----------
	ant_dico : The dico of the ants (dict)
	anthill_dico : The dico of the anthills (dict)
	clod_dico : The dico of the clods (dict)
	player_id: the number of the player (int)
	
	Return
	------
	orders : The order(s) of the IA (str)
	
	Version
	-------
	Parameters : Marchal Tom (v.1 26/04/21)
	Implémentation : Marchal Tom ()
	"""
	order = ""
	orders = ""
	# Récupère la fourmilière de l'équipe
	if player_id == 1:
		team = 'blue'
		enemy = 'red'
	else:
		team = 'red'
		enemy = 'blue'
	anthill_color = "anthill_%s"%team
	enemy_anthill = "anthill_%s"%enemy
	anthill = anthill_dico[anthill_color]
	enemy_anthill = anthill_dico[enemy_anthill]

	# ETAPE 1
	# ----------
	# Si motte < 3:      -> NIVEAU 1
    # Ramasser des mottes

    # Si Fourmis ennemies s'approchent de la fourmilière (moins de 4 cases)
    #     Si position de force   
    #         Dirige vers la fourmi adverse
    #     Sinon
    #         Les fourmis les plus proches se dirigent vers la fourmilière (défense)


	# Première étape : Récupérer un maximum de mottes de terres pour avoir un avantage sur le niveau des fourmis 
	#Si moins de 3 mottes de terres


	if Clod_number_around_anthill(clod_dico,anthill_dico, team) < 3:
		#Pour chaque fourmis
		for ant in ant_dico:
			if not check_if_ant_has_order(ant,orders):
				coordinate = [ant[0], ant[1]]
				#Pour les fourmis de l'équipe
				if ant_dico[ant]['team'] == team:
					#Pour les fourmis de l'équipe qui ne portent pas de motte de terres
					if ant_dico[ant]['clod'] == False:
						#On va chercher pour chaque fourmis la motte de terre la plus proche
						for clod in clod_dico:
							is_around = Is_around(anthill, clod)
							is_nearest = Is_nearest(coordinate, clod, clod_dico)

							#dirige la fourmi vers la motte de terre
							if is_around == False and is_nearest == True:
								if coordinate[0] != clod[0] or coordinate[1] != clod[1]:
									new_position = get_coordinate(coordinate, clod)
									order = "%d-%d:@%d-%d"%(coordinate[0],coordinate[1],new_position[0],new_position[1])
									break
								else:
									if ant_dico[ant]['strength'] >= clod_dico[clod]:
										order = "%d-%d:lift"%(coordinate[0],coordinate[1])
										break

					#Si elle porte une motte de terre
					else:
						target = [anthill[0], anthill[1]]
						distance_anthill = [abs(target[0] - coordinate[0]), abs(target[1] - coordinate[1])]
						#Si elle est à côté de la fourmilière
						if distance_anthill[0] < 3 and distance_anthill[1] < 3:
							#La foumi est à coté de la fourmilière
							if distance_anthill[0] < 2 and distance_anthill[1] <2:	
								order = "%d-%d:drop"%(coordinate[0],coordinate[1])
							#Cases entre 2 et 3
							else:
								#Parcourir les cases autour de la fourmilière
								for x in range(0,3):
									for y in range(0,3):
										target = [anthill[0] + x - 1, anthill[0] + y - 1]
										#Si case libre
										if not Check_something(clod_dico, target):
											#Se diriger vers la case la plus proche autour de la fourmilière
											new_position = get_coordinate(coordinate, target)
											order = "%d-%d:@%d-%d"%(coordinate[0],coordinate[1],new_position[0],new_position[1])

						#dirige la fourmi vers la fourmilière si elle n'est pas autour de la fourmilière
						else:
							if not check_if_ant_has_order(ant,orders):
								new_position = get_coordinate(coordinate, anthill)
								order = "%d-%d:@%d-%d"%(coordinate[0],coordinate[1],new_position[0],new_position[1])

			orders += order + " "

	if Clod_number_around_anthill(clod_dico, anthill_dico, team) >= 3:
		# Deuxième étape : Se diriger vers la fourmilière adverse
		# Si 3 mottes de terres ou plus
		for ant in ant_dico:
			if ant_dico[ant]['team'] == team:
				ant = list(ant)
				ant_x = ant[0]
				ant_y = ant[1]
				if ant[0] < enemy_anthill[0]:
					ant[0] += 1
				elif ant[0] > enemy_anthill[0]:
					ant[0] -= 1

				if ant[1] < enemy_anthill[1]:
					ant[1] += 1
				elif ant[1] > enemy_anthill[1]:
					ant[1] -= 1
				if not check_if_ant_has_order(ant,orders):
					order = "%d-%d:@%d-%d"%(ant_x,ant_y,ant[0],ant[1])
					orders += order + " "
		


		# Défense : Attaquer toutes les fourmis proches de la fourmilière
		for enemy_ant in ant_dico:
			if anthill[0]-3 <= enemy_ant[0] <= anthill[0]+3 and anthill[1]-3 <= enemy_ant[1] <= anthill[1]+3:
				for ant in ant_dico:
					if ant_dico[ant]['team'] == team:
						if anthill[0]-6 <= ant[0] <= anthill[0]+6 and anthill[1]-6 <= ant[1] <= anthill[1]+6:
							dist_x = abs(ant[0] - enemy_ant[0])
							dist_y = abs(ant[1] - enemy_ant[1])
							if dist_x < 4 and dist_y < 4:
								if not check_if_ant_has_order(ant,orders):
										order = "%d-%d:*%d-%d"%(ant[0],ant[1],enemy_ant[0],enemy_ant[1])
										orders += order + " "
							else:
								ant = list(ant)
								if ant[0] < enemy_ant[0]:
									ant[0] += 1
								elif ant[0]> enemy_ant[0]:
									ant[0] -= 1
								if ant[1]< enemy_ant[1]:
									ant[1] += 1
								elif ant[1] > enemy_ant[1]:
									ant[1] -= 1
								if not check_if_ant_has_order(ant,orders):
									order = "%d-%d:@%d-%d"%(ant_x,ant_y,ant[0],ant[1])
								orders += order + " "

		# Position de force --> Attaquer la fourmi adverse
		for ant in ant_dico:
			if ant_dico[ant]['team'] == team:
				for enemy_ant in ant_dico:  	
					if ant_dico[enemy_ant]['team'] == enemy:
						dist_x= abs(ant[0]-enemy_ant[0])
						dist_y= abs(ant[1]-enemy_ant[1])
						if dist_x<4 and dist_y<4:
							if ant_dico[ant]['life']> ant_dico[enemy_ant]['life']:
								if not check_if_ant_has_order(ant,orders):
									order = "%d-%d:*%d-%d"%(ant[0],ant[1],enemy_ant[0],enemy_ant[1])
									orders += order + " "

		# Position de faiblesse --> Rester en retrait et prendre les mottes de terres adverses
		for ant in ant_dico:
			if ant_dico[ant]['team'] == team:
				for enemy_ant in ant_dico:
					if ant_dico[enemy_ant]['team'] == enemy:
						dist_x = abs(ant[0] - enemy_ant[0])
						dist_y = abs(ant[1] - enemy_ant[1])
						if dist_x < 4 and dist_y < 4:
							if ant_dico[ant]['life'] < ant_dico[enemy_ant]['life']:
								ant = list(ant)
								ant_x = ant[0]
								ant_y = ant[1]
								if ant[0] < enemy_ant[0]:
									ant[0] -= 1
								elif ant[0] > enemy_ant[0]:
									ant[0] += 1

								if ant[1] < enemy_ant[1]:
									ant[1] -= 1
								elif ant[1] > enemy_ant[1]:
									ant[1] += 1
								if not check_if_ant_has_order(ant,orders):
									order = "%d-%d:@%d-%d"%(ant_x,ant_y,ant[0],ant[1])
									orders += order + " "
		
	# Ramener les mottes de terres autour de la fourmilière si la fourmi en porte une
	for ant in ant_dico:
		if ant_dico[ant]['team'] == team:
			if ant_dico[ant]['clod']:
				ant = list(ant)
				ant_x = ant[0]
				ant_y = ant[1]
				if ant_x == anthill[0]+1 or ant_x == anthill[0] or ant_x == anthill[0]-1 and ant_y == anthill[1]+1 or ant_y == anthill[1] or ant_y == anthill[1]-1:
					if ant_x != anthill[1] or ant_y != anthill[1]:
						if not check_if_ant_has_order(ant,orders):
							order = "%d-%d:drop"%(ant_x,ant_y)
				else:
					if ant_x < anthill[0]:
						ant[0] += 1
					elif ant_x > anthill[0]:
						ant[0] -= 1
					if ant_y < anthill[1]:
						ant[1] += 1
					elif ant_y > anthill[1]:
						ant[1] -= 1
					if not check_if_ant_has_order(ant,orders):
						order = "%d-%d:@%d-%d"%(ant_x,ant_y,ant[0],ant[1])
				orders += order + " "
					
		# Intercepter des fourmis adverses qui retourne vers leurs fourmilières avec une motte de terre
		for ant in ant_dico:
			if ant_dico[ant]['team'] == team:
				for enemy_ant in ant_dico:
					if ant_dico[enemy_ant]['team'] == enemy:
						if ant_dico[enemy_ant]['clod']:
							dist_x = abs(ant[0] - enemy_ant[0])
							dist_y = abs(ant[1] - enemy_ant[1])
							if dist_x < 4 and dist_y < 4:
								if not check_if_ant_has_order(ant,orders):
									order = "%d-%d:*%d-%d"%(ant[0],ant[1],enemy_ant[0],enemy_ant[1])
									orders += order + " "

		return orders

def check_if_ant_has_order(ant,orders):
	"""Check if the ant has already an order in this turn

	Parameters
	----------
	ant : The ant you check (list)
	orders : the orders of the turn (str)

	return
	------
	is_order: True if the ant has already an order (bool)

	Version
	-------
	Spécification: Tom Marchal (v.1 29/04/21)
	Implémentation : Tom Marchal (v.1 29/04/21)

	"""
	is_order = False
	#check si orders n'est pas vide
	if ":" in orders:
		orders = orders.split()
		for order in orders:
			order = order.split(":")
			if str(ant[0]) in str(order[0]) and str(ant[1]) in str(order[0]):
				is_order = True

	return is_order

main_game(cpx_file,1,'human',2, 'human')
