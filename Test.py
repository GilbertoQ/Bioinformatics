# function takes in the 4 required files
# receptor.pdb, *_site.mol2 , decoys_final.mol2 , actives_final.mol2


import numpy as np
import math
import h5py
import matplotlib.pyplot as plt
import os.path

from mpl_toolkits.mplot3d import Axes3D



def rotateY(coor, angle):
	""" Rotates the point around the Y axis by the given angle in degrees. """
	rad = angle * math.pi/180
	cosa = math.cos(rad)
	sina = math.sin(rad)
	z = coor[2] * cosa - coor[0]* sina
	x = coor[2] * sina + coor[0] * cosa
	return ((x,coor[1],z))
def rotateX(coor, angle):
	""" Rotates the point around the X axis by the given angle in degrees. """
	rad = angle * math.pi / 180
	cosa = math.cos(rad)
	sina = math.sin(rad)
	y = coor[1]* cosa - coor[2]* sina
	z = coor[1] * sina + coor[2] * cosa
	return Point3D((coor[0],y,z))
def rotateZ(coor, angle):
    """ Rotates the point around the Z axis by the given angle in degrees. """
    rad = angle * math.pi / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    x = coor[0] * cosa - coor[1] * sina
    y = coor[0] * sina + coor[1] * cosa
    return Point3D(x,y,coor[2])

fig = plt.figure()

ax = fig.add_subplot(111, projection = '3d')



receptor=open('aces/receptor.pdb')




#This is list that will eventually be saved so the atom_type stays consistent
#The first element of the array is the place 
atom_type_s = []
#atom_type_s.append(1)

atom_type_d={}

if os.path.exists ('Atom_types.h5'):
    with h5py.File('Atom_types.h5', 'r') as hf:
        atom_type_s = hf['Atom_types'][:]
    atom_type_s = [n.decode("utf-8", "ignore") for n in atom_type_s]
    #atom_type_s=np.load('Atom_types.h5')
    #atom_type_s=atom_type_s.tolist()
    for i in range(len(atom_type_s)):
        atom_type_d[atom_type_s[i]]=i+1
print(atom_type_s)

#Distance from origin for the cube creation
ANG=10

#print(atom_type_d)

prow_position = 0
pcolumn_position = 0

pcoordinates=[]


#DO NOT DELETE THESE COMMENTED LINES THEY COULD BE EXAMPLE
#pcoordinates=np.asarray(pcoordinates)
#pcoordinates=flatten()
#np.hstack(pcoordinates)



#print(pcoordinates[0])

for line in receptor:
    list = line.split()
    id = list[0]

    if id == 'ATOM':
        
        if not list[2] in atom_type_d:
            atom_type_s.append(list[2])
            atom_type_d[list[2]]=len(atom_type_s)
            #atom_type_s[0]+=1

        #residue = list[3]
        #type_of_chain = list[4]
        #atom_count = float(list[5])

        pcoordinates.append( (float(list[5]),float(list[6]),float(list[7]))) 

        prow_position += 1
        
pcoordinates.append((-999,0,0))

#print(atom_type_d)
receptor.close()



srow_position=0
scolumn_position=0
scoordinates = []

site=open('aces/1e66_site.mol2')

correct=False

for line in site:
    if line == '@<TRIPOS>BOND\n':
        break
    list = line.split()

    if correct:
        if not list[1] in atom_type_d:
            atom_type_s.append(list[1])
            atom_type_d[list[1]]=len(atom_type_s)

        scoordinates.append( (float(list[2]),float(list[3]),float(list[4])))

        srow_position += 1
    if line == '@<TRIPOS>ATOM\n':
        correct=True

scoordinates.append( (-999,0,0))
#print("Printing Site Coordinates: ")
#print(scoordinates)
site.close()

#read in the actives

actives = open('aces/actives_final.mol2')
acoordinates = []
arow_position = 0
acolumn_position = 0
correct=False

for line in actives:
    if line == '@<TRIPOS>BOND\n':
        correct = False
        acoordinates.append((-999,0,0))
        arow_position += 1
    list = line.split()

    if correct:
        if not list[1] in atom_type_d:
            atom_type_s.append(list[1])
            atom_type_d[list[1]]=len(atom_type_s)


        acoordinates.append((float(list[2]),float(list[3]),float(list[4])))

        arow_position += 1
    if line == '@<TRIPOS>ATOM\n':
        correct=True

#acoordinates[arow_position,acolumn_position]=-999
#print(acoordinates)
actives.close()



decoys = open('aces/decoys_final.mol2')
correct = False
dcoordinates = []
drow_position=0
dcolumn_position=0
for line in decoys:
    if line == '@<TRIPOS>BOND\n':
        correct = False
        dcoordinates.append((-999,0,0))
        drow_position += 1
    list = line.split()

    if correct:
        if not list[1] in atom_type_d:
            atom_type_s.append(list[1])
            atom_type_d[list[1]]=len(atom_type_s)


        dcoordinates.append((float(list[2]),float(list[3]),float(list[4])))

        drow_position += 1
    if line == '@<TRIPOS>ATOM\n':
        correct=True

decoys.close()





##Finally save array
print(atom_type_s)
atom_type_s = [n.encode("ascii", "ignore") for n in atom_type_s]
##print(atom_type_d)
z=np.asarray(atom_type_s)
##print(z)
with h5py.File('Atom_types.h5', 'w') as hf:
    hf.create_dataset("Atom_types",  data=z)
#np.save('Atom_types',z)


site_x_average = 0.0
site_y_average = 0.0
site_z_average = 0.0
site_av_list = []

for x in range(len(scoordinates)):
    site_x_average += float(scoordinates[x][0])
    site_y_average += float(scoordinates[x][1])
    site_z_average += float(scoordinates[x][2])


divisor=len(scoordinates)
site_x_average = site_x_average / divisor
site_y_average = site_y_average / divisor
site_z_average = site_z_average / divisor




site_av_list.append([site_x_average, site_y_average, site_z_average])



#Move acoorrdinats and dcoorridants to the origin
#DO NOT DELETE
'''
for i in range(len(acoordinates)):
	if acoordinates[i][0]==-999:
		continue
	temp=[]
	if site_av_list[0][0]<= 0:
		temp.append(float('%.3f'%(acoordinates[i][0]+abs(site_av_list[0][0]))))
	else:
		temp.append(float('%.3f'%(acoordinates[i][0]-site_av_list[0][0])))
	if site_av_list[0][1]<= 0:
		temp.append(float('%.3f'%(acoordinates[i][1]+abs(site_av_list[0][1]))))
	else:
		temp.append(float('%.3f'%(acoordinates[i][1]-site_av_list[0][1])))
	if site_av_list[0][2]<= 0:
		temp.append(float('%.3f'%(acoordinates[i][2]+abs(site_av_list[0][2]))))
	else:
		temp.append(float('%.3f'%(acoordinates[i][2]-site_av_list[0][2])))
	temp2=(temp[0],temp[1],temp[2])
	acoordinates[i]=temp2

print(acoordinates)
'''



points = []

points1 = np.column_stack([site_av_list[0][0] + ANG, site_av_list[0][1] + ANG, site_av_list[0][2] + ANG])
points2 = np.column_stack([site_av_list[0][0] + ANG, site_av_list[0][1] + ANG, site_av_list[0][2] - ANG])
points3 = np.column_stack([site_av_list[0][0] + ANG, site_av_list[0][1] - ANG, site_av_list[0][2] + ANG])
points4 = np.column_stack([site_av_list[0][0] + ANG, site_av_list[0][1] - ANG, site_av_list[0][2] - ANG])

points5 = np.column_stack([site_av_list[0][0] - ANG, site_av_list[0][1] + ANG, site_av_list[0][2] + ANG])
points6 = np.column_stack([site_av_list[0][0] - ANG, site_av_list[0][1] + ANG, site_av_list[0][2] - ANG])
points7 = np.column_stack([site_av_list[0][0] - ANG, site_av_list[0][1] - ANG, site_av_list[0][2] + ANG])
points8 = np.column_stack([site_av_list[0][0] - ANG, site_av_list[0][1] - ANG, site_av_list[0][2] - ANG])


points = np.row_stack((points1, points2))
points = np.row_stack((points, points3))
points = np.row_stack((points, points4))
points = np.row_stack((points, points5))
points = np.row_stack((points, points6))
points = np.row_stack((points, points7))
points = np.row_stack((points, points8))






##
##
##
##
##Cube creation
##
##site_av_list is averages
##
##p,s,d,a are all the coordinates

site_p=[]
site_s=[]
site_a=[]
site_d=[]

a_counter=0
d_counter=0

for i in range(len(pcoordinates)):
	check=(pcoordinates[i][0],pcoordinates[i][1],pcoordinates[i][2])
	if (check[0]<=site_av_list[0][0]+ANG and  check[0]>=site_av_list[0][0]-ANG) and (check[1]<=site_av_list[0][1]+ANG and  check[1]>=site_av_list[0][1]-ANG) and (check[2]<=site_av_list[0][2]+ANG and  check[2]>=site_av_list[0][2]-ANG):
		site_p.append(check)

for i in range(len(scoordinates)):
	check=(scoordinates[i][0],scoordinates[i][1],scoordinates[i][2])
	if (check[0]<=site_av_list[0][0]+ANG and  check[0]>=site_av_list[0][0]-ANG) and (check[1]<=site_av_list[0][1]+ANG and  check[1]>=site_av_list[0][1]-ANG) and (check[2]<=site_av_list[0][2]+ANG and  check[2]>=site_av_list[0][2]-ANG):
		site_s.append(check)

flag=True
while (flag):
	check=(acoordinates[a_counter][0],acoordinates[a_counter][1],acoordinates[a_counter][2])
	if (check[0]<=site_av_list[0][0]+ANG and  check[0]>=site_av_list[0][0]-ANG) and (check[1]<=site_av_list[0][1]+ANG and  check[1]>=site_av_list[0][1]-ANG) and (check[2]<=site_av_list[0][2]+ANG and  check[2]>=site_av_list[0][2]-ANG):
	    site_a.append(check)
	a_counter+=1
	if check[0]==-999:
		flag=False


flag=True
while (flag):
	check=(dcoordinates[d_counter][0],dcoordinates[d_counter][1],dcoordinates[d_counter][2])
	if (check[0]<=site_av_list[0][0]+ANG and  check[0]>=site_av_list[0][0]-ANG) and (check[1]<=site_av_list[0][1]+ANG and  check[1]>=site_av_list[0][1]-ANG) and (check[2]<=site_av_list[0][2]+ANG and  check[2]>=site_av_list[0][2]-ANG):
	    site_d.append(check)
	d_counter+=1
	if check[0]==-999:
		flag=False




#check if rotation works




#print(site_a)
#for i in range(8):
    #ax.scatter(points[i][0], points[i][1], points[i][2], color = "black")

for i in range(len(site_p)):
	#site_p[i]=rotateY(site_p[i],45)
	ax.scatter(site_p[i][0], site_p[i][1], site_p[i][2], color = "blue")


for i in range(len(site_s)):
	#site_s[i]=rotateY(site_s[i],45)
	ax.scatter(site_s[i][0], site_s[i][1], site_s[i][2], color = "red")

for i in range(len(site_a)):
	#site_a[i]=rotateY(site_a[i],45)
	ax.scatter(site_a[i][0], site_a[i][1], site_a[i][2], color = "green")

#for i in range(len(site_d)):
	#ax.scatter(site_d[i][0], site_d[i][1], site_d[i][2], color = "green")
print(len(site_p)+len(site_s)+len(site_a))
plt.show()