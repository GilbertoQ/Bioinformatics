import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
visited = {}
###Gilberto : Changed from np.row_stack to a stack matrix for the ccordinates. Its much faster and 
###the matrix is big enough to where it will never go out of bounds.
### The 'p' in front of variable names stands for protien such as : prow_position.
### Same with the 's' "site" and the 'l' "liagand".
rows=8000
columns=3
prow_position=0
pcolumn_position=0
pcoordinates = np.zeros((rows,columns))


i = 0
for line in open('receptor.pdb'):
    list = line.split()
    id = list[0]
    i = i + 1

    if id == 'ATOM':
        type = list[2]
        residue = list[3]
        type_of_chain = list[4]
        atom_count = float(list[5])
        #pos = np.asmatrix(list[5:8])
        #position = np.row_stack((position, pos))
        pcoordinates[prow_position,pcolumn_position]=list[5]
        pcoordinates[prow_position,pcolumn_position+1]=list[6]
        pcoordinates[prow_position,pcolumn_position+2]=list[7]
        prow_position+=1
        if atom_count >= 0:
            if type_of_chain not in visited:
                visited[type_of_chain] = 1
                
                              
#position = position.astype(float)
pcoordinates[prow_position,pcolumn_position]=-999
#print(pcoordinates)

for row in range(len(pcoordinates)):
	if pcoordinates[row,0]==-999:
		break
	ax.scatter(pcoordinates[row, 0], pcoordinates[row, 1], pcoordinates[row, 2], color = "black")

srow_position=0
scolumn_position=0
scoordinates = np.zeros((rows,columns))

visited = {}
sfdsf = [[0,0,0]]
for line in open('site.pdb'):
    list = line.split()
    id = list[0]
    type = list[2]
    residue = list[3]
    type_of_chain = list[4]
    #pos = np.asmatrix(list[2:5])
    #sfdsf = np.row_stack((sfdsf, pos))
    scoordinates[srow_position,scolumn_position]=list[2]
    scoordinates[srow_position,scolumn_position+1]=list[3]
    scoordinates[srow_position,scolumn_position+2]=list[4]
    srow_position+=1
                
                
              
#sfdsf = sfdsf.astype(float)      
#for row in range(len(sfdsf)):
#        ax.scatter(sfdsf[row, 0], sfdsf[row, 1], sfdsf[row, 2], color = "red")  
scoordinates[srow_position,scolumn_position]=-999 
for row in range(len(scoordinates)):
	if scoordinates[row,0]==-999:
		break
	ax.scatter(scoordinates[row, 0], scoordinates[row, 1], scoordinates[row, 2], color = "red")        
        
        
lrow_position=0
lcolumn_position=0
lcoordinates = np.zeros((rows,columns))

visited = {}
haha = [[0,0,0]]
for line in open('crystal_ligand.pdb'):
    list = line.split()
    id = list[0]
    type = list[2]
    residue = list[3]
    type_of_chain = list[4]
    #sop = np.asmatrix(list[2:5])
    #haha = np.row_stack((haha, sop))
    lcoordinates[lrow_position,lcolumn_position]=list[2]
    lcoordinates[lrow_position,lcolumn_position+1]=list[3]
    lcoordinates[lrow_position,lcolumn_position+2]=list[4]
    lrow_position+=1
                
                
              
#haha = haha.astype(float)      
#for row in range(len(haha)):
#        ax.scatter(haha[row, 0], haha[row, 1], haha[row, 2], color = "green")   

lcoordinates[lrow_position,lcolumn_position]=-999 
for row in range(len(lcoordinates)):
	if lcoordinates[row,0]==-999:
		break
	ax.scatter(lcoordinates[row, 0], lcoordinates[row, 1], lcoordinates[row, 2], color = "green")  
plt.show()
