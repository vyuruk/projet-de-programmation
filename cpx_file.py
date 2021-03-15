
import random, os
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
path = os.path.realpath('.\data_game.txt')
print(path)
