#1. run list_file.py on the unzipped/ Original Dude data set
#2. run obabel.txt in order to go from .mol2 to .pdbqt
#3. run list_fil.py again to get the updated list of files

#4. Run readwrite_decoys by passing in all the proper files to go from single pdbqt file to 100's
#5. Run readwrirte_actives by passing in all the proper files to go from single pdbqt file to 100's

#6. Run list_file.py again to get updated list of all the files.
#7. Run readwrite_site on all approprite files. Where readwrite_site will write to the config file after each run then run vina to get final output.

from file_list import *
from get_dict import *
from readwrite_models import separate_models
from readwrite_site import *
from prepare_AD4 import *
from sys import argv
import subprocess
import os
from queue import Empty
import multiprocessing as multi
import time

def task(queue):
    original_CWD=os.getcwd()
    while True:
        try:
            key = queue.get(False)
        except Empty:
            break
        os.chdir(os.getcwd()+'//'+key)
        print("To pdbqt: " +os.getcwd())
        #Use obabel
        os.system('obabel *.mol2 -opdbqt -m 1> mol2.log 2> mol2_error.log')
        os.system('obabel *.pdb -opdbqt -m 1> pdb.log 2> pdb_error.log')
        #Go back to original working dir
        os.chdir(original_CWD)
        queue.task_done()

def write_config(big_x, big_y, big_z, averagex, averagey, averagez, one_file, key, files):
      # write config file
      flaggez = False
      flagger = False
      #if one_file.startswith("crystal_"):
      #      flagger = True
      #      os.system("cp " + original_CWD + "/" + key + "/receptor.pdbqt " + original_CWD + "/ADTWorkspace/")
      #else:
      #      os.system("cp " + original_CWD + "/" + key + "/" + one_file + " " + original_CWD + "/ADTWorkspace/")
            
      folde = key.split('/')[1]
      #vout_folder = original_CWD + "/" + key + "/" + folde + "_vout"
      #os.mkdir(vout_folder)
      #convert to AD4
      
      for adc in files[key]:
            print(original_CWD)
            conf = open(original_CWD + "/"+key+"/config.txt", "w")
            
            if one_file.startswith("crystal_"):
                  #move receptor
                  conf.write("receptor = receptor.pdbqt\n")
            else:
                  #move site
                  conf.write("receptor = " + one_file + "\n")  
            '''
            if (adc.startswith("active_num") and adc.endswith(".pdbqt")):
                  flaggez = True
                  conf.write("ligand = "+ adc +"\n\n")
            elif (adc.startswith("decoy_num") and adc.endswith(".pdbqt")):
                  flaggez = True
                  conf.write("ligand = " + adc + "\n\n")
            elif(adc.startswith("crystal_ligand") and adc.endswith(".pdbqt")):
                  flaggez = True
                  conf.write("ligand = " + adc + "\n\n")
            '''    
            if flaggez:
                  os.system("cp " + original_CWD + "/" + key + "/" + adc + " " + original_CWD + "/ADTWorkspace/")
                  
                  conf.write("center_x = " + str(averagex) + "\n")
                  conf.write("center_y = " + str(averagey) + "\n")
                  conf.write("center_z = " + str(averagez) + "\n\n")
                  
                  conf.write("size_x = " + str(big_x) + "\n")
                  conf.write("size_y = " + str(big_y) + "\n")
                  conf.write("size_z = " + str(big_z) + "\n\n")
                  
                  cda = adc.split('.')[0]
                  conf.write("out = " + cda + "_out.pdbqt\n")
                  conf.write("log = " + cda + "_log.txt\n")      
                  conf.close()      
                  print(adc)
                  os.chdir(original_CWD + "/ADTWorkspace/")
                  os.system("./vina --config config.txt")
                  os.chdir(original_CWD)
                  
                  # Once done, aka vina, remove files
                  os.system("cp " + original_CWD + "/ADTWorkspace/" + cda + "_log.txt " + vout_folder)
                  os.system("cp " + original_CWD + "/ADTWorkspace/" + cda + "_out.pdbqt " + vout_folder)
                  os.system("rm " + original_CWD + "/ADTWorkspace/" + cda + "_out.pdbqt")
                  os.system("rm " + original_CWD + "/ADTWorkspace/" + cda + "_log.txt")
                  os.system("rm " + original_CWD + "/ADTWorkspace/" + adc)
                  flaggez = False
                  
            
      # for each active and decoy and the crystal, save config
      if flagger == True:
            os.system("rm " + original_CWD + "/ADTWorkspace/" + "receptor.pdb")
      else:
            os.system("rm " + original_CWD + "/ADTWorkspace/" + one_file)
            
def write_config_protien(big_x, big_y, big_z, averagex, averagey, averagez, one_file, key):      
    conf = open("config.txt", "w")
    if one_file.startswith("crystal_"):
        #move receptor
        conf.write("receptor = receptor.pdbqt\n\n")
    else:
        #move site
        conf.write("receptor = " + one_file + "\n")  
    conf.write("center_x = " + str(averagex) + "\n")
    conf.write("center_y = " + str(averagey) + "\n")
    conf.write("center_z = " + str(averagez) + "\n\n")
                  
    conf.write("size_x = " + str(big_x) + "\n")
    conf.write("size_y = " + str(big_y) + "\n")
    conf.write("size_z = " + str(big_z) + "\n\n")      
    conf.close()
      
def do_this(files):
    #Save the original working directory to always go back to
    original_CWD=os.getcwd()
    #Iterate over all the folders
    for key in files:
        #Change working dir to folder
        os.chdir(os.getcwd()+'//'+key)
        print("To pdbqt: " +os.getcwd())
        #Use obabel
        os.system('obabel *.mol2 -opdbqt -m')
        os.system('obabel *.pdb -opdbqt -m')
        #Go back to original working dir
        os.chdir(original_CWD)

def do_this_in_parallel(files):
    manager = multi.Manager()
    queue_of_keys = manager.Queue()
    for key in files:
        queue_of_keys.put(key)
    with multi.Pool(multi.cpu_count()-1) as processes:
        processes.map(task, [queue_of_keys for i in range(multi.cpu_count()-1)])
        queue_of_keys.join()


if __name__ == "__main__":
    file2=None
    mypath=None
    if len(argv)>1:
        file2, mypath = argv
        #Step 1
        get_files(file2,mypath)

    #Step 2(Get the dict first)
    files=get_dict(file2)
    #files={"abl1":["actives_final.pdbqt","decoys_final.pdbqt"],"ada":["actives_final.pdbqt","decoys_final.pdbqt"]}

    #Save the original working directory to always go back to
    original_CWD=os.getcwd()
    
    #do_this_in_parallel(files)
    do_this(files)

    os.chdir(original_CWD)
    #Step 4 and 5
    get_files(file2,mypath)
    files=get_dict(file2)
    #print(files)
    #files={"abl1":["actives_final.pdbqt","decoys_final.pdbqt"]}
    
    for key in files:
        os.chdir(original_CWD)
        temp3=os.getcwd()+'//'+key
        os.chdir(os.getcwd()+'//'+key)
        print("Seperating: " +os.getcwd())
        for one_file in files[key]:
            #print(one_file)
            temp2=one_file
            if "actives" in one_file:
                if one_file.endswith(".pdbqt"):
                    separate_models(temp2, "active_num_{}.pdbqt",temp3,ignore_repeats=True) #actives(temp2)
            elif "decoys" in one_file:
                if one_file.endswith(".pdbqt"):
                    separate_models(temp2, "decoy_num_{}.pdbqt",temp3, ignore_repeats=False) #decoys(temp2)
    os.chdir(original_CWD)
    if len(argv)>1:
        #Step 6
        get_files(file2,mypath)
        files=get_dict(file2)
    #files2 = {"abl1":["2hzi_site.pdbqt", "crystal_ligand.pdbqt"]}
    

    
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
    else:
        print("Could not find MGLTools")
    

    for key in files:
        os.chdir(original_CWD)
        os.chdir(os.getcwd() + '//' + key)
        print("Handling site: " + os.getcwd())
        temp=""
        size=len(files[key])
        flag=False
        for one_file in files[key]:
            #print(one_file)
            if "site" in one_file:
                if one_file.endswith(".pdbqt"):
                    #call prepare_AD4 on site .pdbqt
                    big_x,big_y,big_z,averagex,averagey,averagez = get_conf_attributes(one_file, 1)
                    os.system("obabel "+one_file+" -omol2 -m")
                    new_file=one_file[0:-5]+"mol2"
                    prepare_AD4(MGLTools_dir,os.getcwd(),new_file,original_CWD)
                    os.system('obabel *.pdb -omol2 -m')
                    new_file="receptor.mol2"
                    prepare_AD4(MGLTools_dir,os.getcwd(),new_file,original_CWD)
                    print(one_file)
                   
                    #write_config(big_x, big_y, big_z, averagex, averagey, averagez, one_file, key, files)
                    write_config_protien(big_x, big_y, big_z, averagex, averagey, averagez, one_file, key)
                    break
            if one_file.startswith("crystal_") and one_file.endswith(".pdbqt"):
                temp=one_file
                flag=True
            if size==1 and flag:
                os.system('obabel *.pdb -omol2 -m')
                big_x,big_y,big_z,averagex,averagey,averagez = get_conf_attributes(temp, 0)
                #call prepare_AD4 on mol2 receptor
                new_file="receptor.mol2"
                prepare_AD4(MGLTools_dir,os.getcwd(),new_file,original_CWD)
                #write_config(big_x, big_y, big_z, averagex, averagey, averagez, temp, key, files)
                write_config_protien(big_x, big_y, big_z, averagex, averagey, averagez, temp, key)
                break
            size=size-1
    os.chdir(original_CWD)
    get_files(file2,mypath)
    files=get_dict(file2)
    
