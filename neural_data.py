#Problems:
#2: The binding site and the receptor are not on top of each other sometimes. Use AutoDockTools to check the kpcb site and the kpcb receptor.
#They are seperate. If you download the kpcb receptor from the scPDB database then it is correct(try it). This doesnt matter for vina though since 
#we use the bindingsite as the recptor and if not availibale we use a 25*25*25 cube around the crystal_ligand which is on the DUDE receptor. 
#But for the second preproccessing step we will need to get the protien from scPDB database to get the 20*20*20 cube.




import os
from file_list import get_files
from get_dict import get_dict
from prepare_AD4 import *
from sys import argv
import csv 
from readwrite_site import get_conf_attributes
import h5py
import numpy as np
import math


okok = []

def normalize(center, cube, which):
        # tuple cannot be updated, so converting to list is necessary. Then we change back to tuple when we return
        cube_to_list = [list(elem) for elem in cube]
        diff=0
        if center >= -10 and center <=10:
                if center <0:
                        diff = abs(center)+10
                else:
                        diff=10-center
                        
        else:
                if center < 0:
                        diff=abs(center)+10
                else :
                        diff=10-center 
        #print(str(which)+" "+str(diff))
        for x in cube_to_list:
                x[which]=round(x[which]+diff,3)
        '''
        new_center = 10 * len(cube[which])
        summation = []
        for x in cube_to_list:
                summation.append(x[which])
        ex = (10 * len(summation) / sum(summation))
        for x in cube_to_list:
                x[which] = ex * x[which]
        '''
        back_to_tuple = [tuple(elem) for elem in cube_to_list]
        return back_to_tuple

def model_outs(f,atom_type_s,atom_type_d):
      file = open(f)
      models = []
      #avgs = []
      site_cord = []
      for line in file:
            splitter = line.split()
            if splitter[0] == "ATOM":
                  if splitter[4]=='A':
                      site_cord.append((float(splitter[6]), float(splitter[7]), float(splitter[8]),splitter[12]))
                      if not splitter[12] in atom_type_d:
                          atom_type_s.append(splitter[12])
                          atom_type_d[splitter[12]]=len(atom_type_s)
                  else:
                      site_cord.append((float(splitter[5]), float(splitter[6]), float(splitter[7]),splitter[11]))
                      if not splitter[11] in atom_type_d:
                          atom_type_s.append(splitter[11])
                          atom_type_d[splitter[11]]=len(atom_type_s)
            elif splitter[0] == "ENDMDL":
                  #print(site_cord)
                  models.append(site_cord)
                  site_cord = []
      
 
      file.close()    
      return models
def get_center_of_binding_site(f):
    file = open(f)
    center=[]
    i=0
    for line in file:
        if "center" in line:
            center.append(float(line.split(' ')[2]))
    print(center)
    file.close()
    return tuple(center)
def read_receptor(f,atom_type_s,atom_type_d):
    file=open(f)
    site_cord = []
    for line in file:
            splitter = line.split()
            if splitter[0] == "ATOM":
                  if splitter[4]=='A':
                      site_cord.append((float(splitter[6]), float(splitter[7]), float(splitter[8]),splitter[12]))
                      if not splitter[12] in atom_type_d:
                          atom_type_s.append(splitter[12])
                          atom_type_d[splitter[12]]=len(atom_type_s)
                  else:
                      site_cord.append((float(splitter[6]), float(splitter[7]), float(splitter[8]),splitter[12]))
                      if not splitter[12] in atom_type_d:
                          atom_type_s.append(splitter[12])
                          atom_type_d[splitter[12]]=len(atom_type_s)
    return site_cord


if __name__ == "__main__":
    file2 = None
    mypath = None
    if len(argv) > 1:
        file2, mypath = argv
        
        get_files(file2, mypath)
        files = get_dict(file2)
        print(files)

original_CWD = os.getcwd()

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
print(atom_type_d['C'])


#Distance from origin for the cube creation
ANG=10

file_out_cubes=[]
receptor_cube=[]
cube=[]

#before doing anything we have to put proper protien in the file. The scpdb one wich is supposed to be prossesed.
#Assume the receptor is in the folder just not proccesed by preapare_receptorA4.py hence do that.
#Assume that the scpdb receptor for every protien is called scpdb_receptor.mol2

#Find if the computer has MGLTools  

MGLTools_dir=""

for dirpath, dirnames, filenames in os.walk('/'):
    #if folder in dirnames and all(brother in dirnames for brother in brothers):
    #print 'matches on %s' % os.path.join(dirpath, 'zeFolder')
    if "MGL" in dirpath:
        count=dirpath.count('/')
        if count == 3:
            MGLTools_dir=dirpath
            print(MGLTools_dir)
            break

if MGLTools_dir != "":
    print("Found MGLTools location")
    for key in files:
        if os.path.isfile(key+'/'+'scpdb_receptor.mol2'):
                os.chdir(original_CWD)
                os.chdir(os.getcwd() + '//' + key)
                #Found scpdb receptor. Use prepare_receptor.py
                prepare_AD4(MGLTools_dir,os.getcwd(),'scpdb_receptor.mol2',original_CWD)
                os.rename('scpdb_receptor.pdbqt','receptor.pdbqt')
        os.chdir(original_CWD)
else:
    print("Could not find MGLTools. Will Continue Assuming you have proper prepared_AD4 receptor files")

d_type=0
for key in files:
      # read in every out in vout
      if "vout" in key:
            #Read in the receptor for this vout folder and center of binding site
            receptor = read_receptor(key.split('/')[0]+'/'+key.split('/')[1]+'/'+"receptor.pdbqt",atom_type_s,atom_type_d)
            center = get_center_of_binding_site(key.split('/')[0]+'/'+key.split('/')[1]+'/'+"config.txt")
            #print(center[0])
            #print(receptor[0])
            #Get receptor cube
            count=0
            for i in range(len(receptor)):
                if (receptor[i][0] <= center[0]+ANG and receptor[i][0] >= center[0]-ANG) and (receptor[i][1]<= center[1]+ANG and receptor[i][1] >= center[1]-ANG) and (receptor[i][2] <= center[2]+ANG and receptor[i][2] >= center[2]-ANG) :
                    #In future to normalize the receptor cube so that the center is 10*10*10 do it here since we are already looping over everything
                    receptor_cube.append(receptor[i])
                    count=count+1
            print("receptor cube " + str(count)+":")                   
            #print(receptor_cube)
            
                        
            for fil in files[key]:
                  if "out" in fil:
                        if "active" in fil:
                                d_type=1
                        else:
                                d_type=2
                        # found one of the outs
                        file_out_cubes=[]
                        models = model_outs((key + "/" + fil),atom_type_s,atom_type_d)
                        #print(models)
                        #print(atom_type_s)
                        #print(atom_type_d)
                        
                        #Got the averages and all the 3d points for one_file
                        #Get the cube and then save as panda or h5 format
                        for i in range(len(models)):
                            for p in range(len(models[i])):
                                if (models[i][p][0] <= center[0]+ANG and models[i][p][0] >= center[0]-ANG) and (models[i][p][1] <= center[1]+ANG and models[i][p][1] >= center[1]-ANG) and (models[i][p][2] <= center[2]+ANG and models[i][p][2] >= center[2]-ANG) : 
                                    #In future to normalize the ligand cube so that the center is 10*10*10 do it here since we are already looping over everything
                                    # Angel's Note: In this for loop, not all the x-coordinates are being looped on. It only loops up to some x-coordinate... but we need all of them.
                                    # print(cube) below prints out every x-coordinate, but "cube" gets defined outside of this loop... And we need "cube" to access all the x-coordinates
                                    # we can change all the coordinates so that the cube's center is 10*10*10, but it would have to be outside of this loop... I believe so.
                                    cube.append(models[i][p])
                            if i== 0:
                                print(cube)
                            cube=cube+receptor_cube
                            if i==0:
                                print(cube)
                            cube = normalize(center[0], cube, 0)
                            cube = normalize(center[1], cube, 1)
                            cube = normalize(center[2], cube, 2)
                            if i==0:
                                print(cube)
                            # just to check if x center is now 10
                            check_center = []
                            for x in cube:
                                x = list(x)
                                check_center.append(x[2])
                            #print("IS IT 10 YET?", sum(check_center)/len(check_center))
                            
                            
                            print("ligand cube " + str(i) + ":")                   
                            #print(cube)
                            #write = csv.writer(open("test.csv", "w"))
                            #for row in cube:
                            #write.writerow(row)
                            file_out_cubes.append(cube)
                            cube=[]
                        
                        times=0
                        for grid in file_out_cubes:
                                times=times+1
                                #print("New Good")
                                point={}
                                for i in range(0,20):
                                        point[i]={}
                                for i in range(0,20):
                                        for j in range(0,20):
                                                point[i][j]={}
                                for i in range(0,20):
                                        for j in range(0,20):
                                                for p in range(0,20):
                                                        point[i][j][p]=0
                                
                                for entry in grid:
                                        #print(int(entry[0]))
                                        
                                        if point[int(entry[0])][int(entry[1])][int(entry[2])] == 0:
                                                point[int(entry[0])][int(entry[1])][int(entry[2])]=atom_type_d[entry[3]]
                                        else:
                                                print(str(entry[0])+" "+str(entry[1])+" "+str(entry[2])+" " + str(entry[3])+" COLLISION")
                                                print(point[int(entry[0])][int(entry[1])][int(entry[2])])
                                                done=False
                                                if entry[0]<19:
                                                        if point[int(math.ceil(entry[0]))][int(entry[1])][int(entry[2])] == 0 and not done:
                                                                point[int(entry[0])][int(entry[1])][int(entry[2])]=atom_type_d[entry[3]]
                                                                print(str(entry[0])+" "+str(entry[1])+" "+str(entry[2])+" " + str(entry[3])+" Second== Good")
                                                                done=True
                                                if entry[1]<19:
                                                        if point[int(entry[0])][int(math.ceil(entry[1]))][int(entry[2])]== 0 and not done:
                                                                point[int(entry[0])][int(entry[1])][int(entry[2])]=atom_type_d[entry[3]]
                                                                print(str(entry[0])+" "+str(entry[1])+" "+str(entry[2])+" " + str(entry[3])+" Third ==Good")
                                                                done=True
                                                if entry[2]<19:
                                                        if point[int(entry[0])][int(entry[1])][int(math.ceil(entry[2]))]== 0 and not done:
                                                                print(str(entry[0])+" "+str(entry[1])+" "+str(entry[2])+" " + str(entry[3])+" Fourth ==Good")
                                                                point[int(entry[0])][int(entry[1])][int(entry[2])]=atom_type_d[entry[3]]
                                                                done=True
                                                                
                                                                
                                                                
                                #print(point)                              
                                #The dict Point is a dict of a dict of a dict. Simply iterate over it and it will be in correct position
                                # To make a list out of point simply iterate over it Then put into new list to save.                             
                                #Then we save save it into the harddrive
                                #Things we want to do with the saved file
                                #1. Save it(obviosuly)
                                #2. Open it quickly even if the file is massive(so opening it in blocks/chunks/whatever)
                                #3. grab a random row quickly. for example if there are 20 million rows in saved file i can say
                                # temp=data[20 million] to get it then say temp=data[0] and it will be able to do this quickly
                                #that type of ability will be helpfull in the furture
                                #print(times)
                                if d_type==1:
                                        if os.path.isfile("actives.csv"):
                                                row=[]
                                                f=open("actives.csv", "a")
                                                write = csv.writer(f)
                                                for i in range(len(point)):
                                                        for j in range(len(point[i])):
                                                                for k in range(len(point[i][j])):
                                                                        row.append(point[i][j][k])
                                                #for row in cube:
                                                print(len(row))
                                                write.writerow(row)
                                                f.close()
                                        else:
                                                row=[]
                                                f=open("actives.csv", "w")
                                                write = csv.writer(f)
                                                for i in range(len(point)):
                                                        for j in range(len(point[i])):
                                                                for k in range(len(point[i][j])):
                                                                        row.append(point[i][j][k])
                                                #for row in cube:
                                                print(len(row))
                                                write.writerow(row)
                                                f.close()
                                if d_type==2:
                                        if os.path.isfile("decoys.csv"):
                                                row=[]
                                                f=open("decoys.csv", "a")
                                                write = csv.writer(f)
                                                for i in range(len(point)):
                                                        for j in range(len(point[i])):
                                                                for k in range(len(point[i][j])):
                                                                        row.append(point[i][j][k])
                                                #for row in cube:
                                                print(len(row))
                                                write.writerow(row)
                                                f.close()
                                        else:
                                                row=[]
                                                f=open("decoys.csv", "w")
                                                write = csv.writer(f)
                                                for i in range(len(point)):
                                                        for j in range(len(point[i])):
                                                                for k in range(len(point[i][j])):
                                                                        row.append(point[i][j][k])
                                                #for row in cube:
                                                print(len(row))
                                                write.writerow(row)
                                                f.close()
                                '''
                                if times==2:
                                        check=[]
                                        f=open("actives.csv","r")
                                        reader=csv.reader(f)
                                        for line in reader:
                                             check.append(line)  
                                        print("Hey "+str(len(check))) 
                                        count=0
                                        for i in range(len(check[0])):
                                                if check[0][i]==check[1][i]:
                                                        count=count+1 
                                                else:
                                                        print(str(i)+" "+str(check[0][i]+" "+check[1][i]))      
                                        print("Booooo "+str(count))
                                '''
                         
                         
                                
                        #print(point)
                        #currently using break to stop after one file(each file holds around 9 models hence 9 cubes)
                        #break
                        
                        

##Finally save atoms array
#print(atom_type_s)
atom_type_s = [n.encode("ascii", "ignore") for n in atom_type_s]
##print(atom_type_d)
z=np.asarray(atom_type_s)
##print(z)
with h5py.File('Atom_types.h5', 'w') as hf:
    hf.create_dataset("Atom_types",  data=z)

