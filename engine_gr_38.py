#-*- coding: utf-8 -*-

import blessed, math, os, time
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
def Player_order(order_player_1,order_player_2):
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
    """
	#sépare les ordres de la chaine de caractère en liste
	order_p1 = order_player_1.split()
	order_p2 = order_player_2.plit()
	return order_p1, order_p2

def Is_game_over( Clod_number_around_anthill(Clod_dico, Anthill_dico, red), Clod_number_around_anthill(Clod_dico, Anthill_dico,blue),Turn):
    """Verify if the game is over or not.

    parameters        
	----------
    Clod_number_around_anthill(red): the number of clod around the red anthill (int)
	Clod_number_around_anthill(blue): the number of clod around the blue anthill (int)
	Turn: The number of turn (int)

    return       
	------
    Is_over : True if one team have won or the game has reached 200 turns (bool)

	Version
	-------
	Specification : Yuruk Valentin ( v.1 22/02/21)
    """
def End_game(Turn, Clod_number_around_anthill(red),Clod_number_around_anthill(blue)): 
	""" Finish the game and display the winner team.

	Parameter
	---------
	Turn :the number of turn (int)
	Clod_number_around_anthill(red): check the number of clods around the red anthill (int)
	Clod_number_around_anthill(blue): check the number of clods around the blue anthill (int)

	Version
	-------
	Specification : Yuruk Valentin, Marchal Tom (v.1 22/02/21)
	"""
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
	"""
def lift_clod(order,ant_dico,clod_dico)
	""" Check if the ant can lift the clod.

	parameter
	---------
	order: The order of the player (str)
	ant_dico: The dico of the ants (dict)
	clod_dico: The dico of the clods (dict)

	version
	-------
	Specification : Marchal Tom (v.1 26/02/21)
	"""
def Fight(order,ant_dico): 
	""" Check if the ant can attack the other one, attack if he can.

	Parameter
	---------
	order : The order of the player (str) 
	ant_dico : The dico of the ants (dict)

	return
	------
	order_player_1: The order of the first player (str)
	order_player_2: The order of the second player (str)

	Version
	-------
	Specification : Marchal Tom (v.1 20/02/21)
	"""
def Ant_movement(order, ant_dico): 
	""" Check if the ant can move where the order indicate.
	Parameter
	---------
	order : The order of the player (str)
	ant_dico : The dico of the ants (dict)
	
	Version
	-------
	Specification : Marchal Tom (v.1 20/02/21)
	"""
def New_ant(turn, ant_dico, Clod_number_around_anthill(red),Clod_number_around_anthill(blue)): 
	""" Create an ant every 5 turns if there is nothing on the spawn coordinate and adapt the level of the ant with the number of clod around the anthill.

	Parameter
	---------
	turn: The number of turn (int)
	ant_dico: The dico of the ants (dict)
	Clod_number_around_anthill(red): Check the number of clod around the red anthill (int)
	Clod_number_around_anthill(blue) : Check the number of clod around the blue anthill (int)

	Version
	-------
	Specification : Marchal Tom (v.1 20/02/21)
	"""

def Is_ant_dead(Ant_dico):
	"""verify if a ant is dead or not.
	parameters
	----------
	Ant_dico: dictionary of ant (dict)
	
	Version
	------- 
	Specification : Antoine Boudjenah (v.1 22/02/21)
	"""
	
	Is_ant_dead = False
	for cle in Ant_dico.items():
		life = ant_dico[cle][life]
		if life == 0:
			Ant_dico.del[cle]
			Is_ant_dead = True
	return Is_ant_dead

def Clod_number_around_anthill(Clod_dico, Anthill_dico, team):
	"""the function that will count clods around the anthill.
	parameters
	----------
	Clod_dico: dictionary of the clod (dict)
	Anthill_dico: dictionary of anthill (dict)
	team : The anthill's team where we look around (str)

	return
	------
	Clod_number_around_anthill: the number of clod around anthill(int)
	
	Version
	------- 
	Specification : Antoine Boudjenah, Marchal Tom (v.1 22/02/21)
	"""
	anthill_team = "anthill_" + team
	coordinate = Anthill_dico[anthill_team]
	for clod in Clod_dico:
		if clod[0] == coordinate[0]+1 and clod[1] = coordinate[1]:
			
def Display_interface(Cpx_file, Ant_dico, Clod_dico, Anthill_dico):
	"""display the interface at the start of the game till the end. 
	parameters
	----------
	Cpx_file : The file with the data (file)
	Cod_dico: dictionary of the clod (dict)
	Anthill_dico: dictionary of anthill (dict)
	Ant_dico: dictionary of ant (dict)

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
	for row in range (0,rows):
    	for col in range (0,columns):
        	print(term.move_yx(row, col) + term.black + term.on_green + "_" + term.normal, end='', flush=True)
        	if col % 3 == 0:
            	print(term.move_yx(row, col) + term.black + term.on_green + u"\u2502" + term.normal, end='', flush=True)
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
	for clod in clods_dico:
    	x = clod[0]
    	y = clod[1]
    	for ant in ant_dico:
        	if clods_dico[clod] != ant_dico[ant]:
            	print(term.move_yx(x,y) + term.brown + term.on_red + "" + term.normal, end='', flush=True)
	for anthill in anthills_dico:
    	x = anthill[0]
    	y = anthill[1]
		if anthill == 'anthill_blue':
    		print(term.move_yx(row, col) + term.blue + term.on_green + u"\u25A0" + term.normal, end='', flush=True)
		else:
			print(term.move_yx(row, col) + term.red + term.on_green + u"\u25A0" + term.normal, end='', flush=True)
def data(".\cpx_file"):
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
	Implémentation: Marchal TOM (v.1 12/03/21
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

#Squelette de la fonction : 

Play_game( ):

	Display_interface( ) 

	Ant= {} 

	Clod = {} 

	Anthill = {} 

	Clod_dico( )  

	Ant_dico( ) 

	Anthill_dico( ) 

	Turn = 0 

	While not is_game_over( ): 

		#Demander ordre 

		order_player_1 = input("Indiquer vos ordres (P1)")
		order_player_2 = input("Indiquer vos ordres (P2) ")

		#Soulever/ lacher motte 

		For order in order_player( ):

		#combats 

		For order in order_player( ): 

			if “@” in order: 

				fight( ) 

		#déplacement 

		For order in player_order( ): 

			ant_movement( ) 

		# création nouvelle fourmis 

		Is_ant_dead( ) 

		New_ant( ) 

		#est-ce que gagner? 

		Clod_number_around_anthill( ) 

		Turn += 1 

	End_game( ) 
