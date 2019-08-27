from PIL import Image, ImageEnhance
from numpy import array
import numpy as np
import sys
import os.path
import mahotas
from pylab import imshow, gray, show
from matplotlib import pyplot as plt
from max_entro import *
import itertools
from image_processing import *

def weightedAverage(pixel):
    return 0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2]

if len(sys.argv) <=1:
        print("No image file given")
else:
        if os.path.isfile(sys.argv[1]):
                file_name=sys.argv[1].split('.')
                photo=mahotas.imread(sys.argv[1],as_grey=True)
                photo = photo.astype(np.uint8)
                gray()
                height, width = photo.shape
                top_left = int(0.29*height)
                bottom_left = int(0.22*height)
                imshow(photo[top_left:-bottom_left, :])
                show()
                T_photo = mahotas.otsu(photo[top_left:-bottom_left, :])
                plt.hist(photo[top_left:-bottom_left, :].ravel(),256,[0,256]); plt.show()
                #T_photo = motsu(photo)
                #T_photo = max_entro(sys.argv[1])
                #T_photo = mahotas.rc(photo)
                print("Otsu's method {!s}".format(T_photo))
                new_p = Image.fromarray(photo)
                if new_p.mode != 'RGB':
                        new_p = new_p.convert('RGB')
    
                print(np.shape(photo))
                go=photo.shape
                '''
                for row in range(go[0]):
                        for column in range(go[1]):
                                if photo[row][column] <T_photo:
                                        photo[row][column]=1
                                else:
                                        photo[row][column]=0
                '''
                photo=(photo < T_photo)
                imshow(photo)
                show()
                #for row in photo:
                        #print(row)   
                                     
                k=3
                count=0
                temp=np.zeros(k)
                check=0
                start_c=0
                flag=True
                for row in range(go[0]):
                        k=3
                        flag=True
                        temp=np.zeros(k)
                        count=0
                        for column in range(go[1]):
                                #print(go[1]-column)
                                if go[1]-column <= k and flag:
                                        k=go[1]-column
                                        flag=False
                                if count==0:
                                        start_c=column    
                                #print(count)
                                temp[count]=photo[row][column]
                                count=count+1
                                if count >= k:
                                        sumy=0
                                        count=0
                                        for i in range(0,k):
                                                sumy=sumy+temp[i]
                                                #print(str(sumy)+" "+str(i))
                                        #print("hey:"+str(sumy))
                                        if sumy!=k:
                                                #print("Hey:"+str(k))
                                                #print(start_c)
                                                for ret in range(start_c,(start_c+k)):
                                                        #print(ret)
                                                        try:
                                                                photo[row][ret]=0
                                                        except IndexError:
                                                                print("error")
                                                                #check=check+1
                                        
                                                
                #print("Hey")                                
                #for row in photo:
                        #print(row)  
                #print("Hey "+str(check))         
                #gray()
                imshow(photo)
                show()
                
                new_p.save(file_name[0]+"_grayscale."+file_name[1])
        #else:
                print("File does not exist")

