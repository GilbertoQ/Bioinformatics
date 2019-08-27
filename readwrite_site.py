
import numpy as np

def get_conf_attributes(one_file, flagger):
    #example file
    #site=open("abl1/2hzi_site.pdbqt")
    #obtain the file and read it
        
    site=open(one_file)

    #if flagger is equal to 0 that means no binding_site
    #if flagger is equal to 1 that means a binding site file is avialible


    site_cord = []
    for line in site:
        splitter = line.split()
        if splitter[0] == "ATOM":
            if splitter[4]=='A':
                site_cord.append((float(splitter[6]), float(splitter[7]), float(splitter[8])))
            else:
                site_cord.append((float(splitter[5]), float(splitter[6]), float(splitter[7])))

    summx = 0
    summy = 0
    summz = 0
    big_x = 0
    big_y = 0
    big_z = 0
    i = 0
    #find average
    for row in range(len(site_cord)):
        if site_cord[row][0] == 0:
            i = i - 1
            break
        i = i + 1
        summx = summx + site_cord[row][0]
        summy = summy + site_cord[row][1]
        summz = summz + site_cord[row][2]


    averagex = summx / i
    averagey = summy / i
    averagez = summz / i

    #find farthest atom from center
    if flagger == 1:
        for row in range(len(site_cord)):  
            if np.abs(site_cord[row][0])-averagex > big_x:
                big_x = np.abs(site_cord[row][0])-averagex
            if np.abs(site_cord[row][1])-averagey > big_y:
                big_y = np.abs(site_cord[row][1])-averagey
            if np.abs(site_cord[row][2])-averagez > big_z:
                big_z = np.abs(site_cord[row][2])-averagez 

    #multiply by 2 since thats what autodock requires
        big_x=int(round(big_x*2))
        big_y=int(round(big_y*2))
        big_z=int(round(big_z*2))
    if flagger == 0:
        big_x = 25
        big_y = 25
        big_z = 25


    print("Big_x: ", big_x)
    print("Big_y: ", big_y)
    print("Big_z: ", big_z)

    #round to nearest 3 decimal points
    averagex=round(averagex,3)
    averagey=round(averagey,3)
    averagez=round(averagez,3)


    print("Average_X: ", averagex)
    print("Average_Y: ", averagey)
    print("Average_Z: ", averagez)

    return big_x,big_y,big_z,averagex,averagey,averagez

