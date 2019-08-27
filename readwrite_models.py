import os
def writeToFile(model, file_name):
    with open(file_name, "wt") as f:
        for item in model:
            f.write(item)

def read_models(file_of_models):
    """Read models from a file.
    
    The methods reads from MDL to ENDML and passes the ID
    of the model and its data."""
    ID = None
    model = []
    for line in file_of_models:
        split = line.split()
        if split[0] == "ENDMDL":
            yield ID, model
            model = []
            ID = None
        elif split[0] == "REMARK" and split[3][0] == "Z":
            model.append(line)
            ID = split[3]
        elif split[0] == "MODEL":
              continue
        else:
            model.append(line)

def separate_models(file_string, sep_file_name,directory, ignore_repeats=True): 
    """Separate models from a file into multiple files.
    
    Separates a file of N models into N files each containing a model.
    Discards models which repeat.
    """
    
    os.chdir(directory)
    #print('HAHAHAHAHAHAh '+os.getcwd())
    unique_ids = {}
    with open(file_string) as file_of_models:
        i = 0
        repeats = 0
        for ID, model in read_models(file_of_models):
            if ignore_repeats == False and ID in unique_ids:
                repeats += 1
            else:
                writeToFile(model, sep_file_name.format(i))
                i += 1
                unique_ids[ID]=1
        print("Repeats: ", repeats)

