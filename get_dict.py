
def get_dict(file2):
	files={}

	final_file = open("List of Files.txt", "r")

	current_file=""
	i=0
	for line in final_file:
		splitter = " ".join(line.split())
		if splitter.partition(' ')[0]=="Folder:":
			i=i+1
			if splitter.partition(' ')[2]!=file2:
				files[splitter.partition(' ')[2]]=[]
				current_file=splitter.partition(' ')[2]
			#print(splitter.partition(' ')[0])
		elif splitter.partition(' ')[0]=="File:":
			files[current_file].append(splitter.partition(' ')[2])
		#else:
			#continue

	#for key in files:
		#print(key)
		#print(files[key][0])
	final_file.close()	
	return files
