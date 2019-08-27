# function takes in the 4 required files
# receptor.pdb, *_site.mol2 , decoys_final.mol2 , actives_final.mol2
import numpy as np




def preprocces_data(receptor, site, decoys, actives):
    # First read the 4 files and put data into appropriate containers
    # Save a dict using numpy of the atom types while reading the file
    # This will keep atom types consistent across many files

    # save original recetor and site coords for easier future use.

    # Second find the center of the binding_site with
    # the formula centroid = average(x), average(y), average(z)
    # where x, y and z are arrays of floating-point numbers.
    # Build a 20*20*20 cube around that centroid.
    # Save the cube of info
    # pput info int vector
    # Rotate entire structure then save cube again, for about 5 times.
    # Do this for every decoy and actives
    # return many vectors

    receptor=open('abl1/receptor.pdb')




    ROWS = 8000
    COLUMNS = 3
    ATOM_TYPE = 1

    # np.save('file_name'numpy variable,)

    atom_type = np.array(500)
    print("Hello")

    prow_position = 0
    pcolumn_position = 0
    pcoordinates = np.zeros((ROWS, COLUMNS))

    for line in receptor:
        list = line.split()
        id = list[0]

        if id == 'ATOM':
            type = list[2]
            residue = list[3]
            type_of_chain = list[4]
            atom_count = float(list[5])

            pcoordinates[prow_position, pcolumn_position] = list[5]
            pcoordinates[prow_position, pcolumn_position + 1] = list[6]
            pcoordinates[prow_position, pcolumn_position + 2] = list[7]
            prow_position += 1
            if atom_count >= 0:
                if type_of_chain not in visited:
                    visited[type_of_chain] = 1
