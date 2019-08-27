import os

#copy the proper file into the prepare_receptro.py
#run the prepare receptor
#cp the output into proper place
#rm the the output from prepare receptor folder

def prepare_AD4(MGLTools_dir,original_CWD,one_file,original_CWD2):
    rest_of_path="/MGLToolsPckgs/AutoDockTools/Utilities24"
    os.system("cp " + original_CWD+"/"+one_file +" "+MGLTools_dir+rest_of_path)
    os.chdir(MGLTools_dir+rest_of_path)
    os.system("pythonsh prepare_receptor4.py -r "+one_file)
    os.system("rm "+one_file)
    one_file=one_file[0:-4]+"pdbqt"
    os.system("cp "+ one_file+" "+original_CWD)
    os.system("rm "+one_file)
    os.chdir(original_CWD)
    
