# function that outputs a text file with the directory path of each folder in 
# DUDE\all\ and a list of the files within each folder
# to run simply open terminal in proper folder then type "python file_list.py DUDE\all".
#To test code simply pass folder with appriopriate contents

from sys import argv
import os
from os import walk
from os import listdir
import gzip
from types import *

def get_files(file,mypath):
	#file, mypath = argv
	#print(mypath)
	listdir(mypath)

	f = []

	for (dirpath, dirnames, filenames) in walk(mypath):
		temp_remove=[]
		temp_update=[]
		f.append(dirpath)
		#print(filenames)
		for i in filenames:
			#print(i)
			if i.endswith('.gz') or i.endswith('.ism') or i.endswith('.sdf'):
				if i.endswith('.sdf.gz') or i.endswith('.ism') or i.endswith('.sdf'):
					temp_remove.append(i)
				else:
					#print(i)
					file=gzip.open(dirpath+"//"+ i ,'r')
					temp=i[:-3]
					outF=open(dirpath+"//"+temp,'wb')
					outF.write( file.read() )
				
					file.close()
					outF.close()
					temp_update.append(temp)
					temp_remove.append(i)
		for i in temp_remove:
			os.remove(dirpath+"//"+i)
			filenames.remove(i)
		for i in temp_update:
			filenames.append(i)
		for dpath in range(1):
			f.append(filenames) 


	final_file = open("List of Files.txt", "w")

	folder=True
	for entry in f:
		if folder:
			final_file.write("Folder: ")
		for file in entry:
			if file == len(file)*file:
				final_file.write(file)
			else:
				final_file.write("File: ")
				final_file.write(file)
				final_file.write("\n")
		final_file.write("\n")
		folder=not folder


	final_file.close()
