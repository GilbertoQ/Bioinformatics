import numpy as np
import itertools as it
import mahotas
import sys
import os.path
import skvideo.io
from pylab import imshow, gray, show
from PIL import Image, ImageEnhance
from time import time

def euclid_dist(coordinate_1, coordinate_2):
    return abs((coordinate_2[0] - coordinate_1[0])/(coordinate_2[1] - coordinate_1[1]))

def shortest_distance(coordinate, list_of_coordinates):
    shortest_coor = None
    shortest_dist = None
    for coor in list_of_coordinates:
        dist = euclid_dist(coordinate, coor)
        if shortest_coor is None or dist < shortest_dist:
            shortest_coor = coor
            shortest_dist = dist
    return shortest_coor
        

def linear_regression(pixels):
    X = np.array([[x, 1] for x, _ in pixels])
    Y = np.array([y for _, y in pixels])
    B = np.dot(np.dot(np.linalg.pinv(np.dot(X.transpose(), X)), X.transpose()), Y)
    return B    

def line_scan(photo, line_sep=10):
    """Find points in the image that lie on a series of repeating lines."""
    photo = photo*1.5
    photo[photo>255] = 255
    photo = photo.astype(np.uint8)
    height, width = photo.shape
    gray()
    T_photo = mahotas.otsu(photo)
    photo=(photo < T_photo)
    percent = .5#0.29
    rang = range(int(percent*height), int(0.9*height), line_sep)
    array = np.zeros(photo.shape)
    array[rang, :] = photo[rang, :] == False
    #print(array.shape)
    return array #pixel_vec

def blockify(pixels, max_block_size=5, distance_between_pixels=10, percentage=0.5):
    """Create blocks from pixels with a max size."""
    height, width = pixels.shape
    for i in range(0, width-max_block_size, distance_between_pixels):
        rang = range(i, i+max_block_size)
        block = pixels[:, rang].view()
        index = np.sum(block, axis=1) > max_block_size*percentage
        pixels[index, :] = 0
        pixels[index, int(np.mean(rang))] = 1
    return pixels

def old(pixels, max_block_size=5, distance_between_pixels=1):
    new_pixels = []
    sequence = []
    for pixel_row in pixels:
        new_pixel_row = []
        i = 0
        for pixel in pixel_row:
            if len(sequence) > 0 and i < max_block_size:
                if sequence[-1][0] - pixel[0] <= distance_between_pixels:
                    sequence.append(pixel)
                else:
                    new_pixel = (int(np.mean([p[0] for p in sequence])), sequence[0][1])
                    new_pixel_row.append(new_pixel)
                    new_pixel_row.append(pixel)
                    sequence = []
                    i = 0
            elif i >= max_block_size:
                new_pixel = (int(np.mean([p[0] for p in sequence])), sequence[0][1])
                new_pixel_row.append(new_pixel)
                sequence = []
                i = 0
            else:
                sequence.append(pixel)
            i += 1
        new_pixels.append(new_pixel_row)
    return new_pixels

def discard_noise(pixels, threshold=50):
    new_pixel = []
    for pixel_row in pixels:
        if len(pixel_row) < threshold:
            new_pixel.append(pixel_row)
    return new_pixel

def find_best_path(pixel, pixel_vec, current_row, width, flag):
    if current_row < len(pixel_vec):
        best_pixel = None
        if flag is True:
            vec = [(x,abs(pixel-x)) for x, pix in enumerate(pixel_vec[current_row]) if pix != 0 and pixel <= x]
        else:
            vec = [(x,abs(pixel-x)) for x, pix in enumerate(pixel_vec[current_row]) if pix != 0 and pixel >= x]
        """for x, pix in enumerate(pixel_vec[current_row]) if pix != 0:
            # If pix is on the left of pixel
            if (pixel >= x or x < width/2) and flag is True:
                continue
            elif (pixel <= x or x >= width/2) and flag is False:
                continue
            elif best_pixel is None or abs(pixel - x) < abs(pixel - best_pixel):
                best_pixel = x"""
        #if best_pixel is not None:
        if len(vec) != 0:
            best_pixel, _ = sorted(vec, key=lambda x: x[1])[0]
            return [(best_pixel, current_row)] + find_best_path(best_pixel, pixel_vec, current_row+1, width, flag)
        #else:
        #    return find_best_path(pixel, pixel_vec, current_row+1, width, flag)
    return []

def find_best_paths(pixels, width, flag):
    """Finds paths where the distance between pixels in the path is smallest."""
    sequences = []
    for y, row in enumerate(pixels):
        for x, pixel in enumerate(row):
            if pixel != 0:
                if (flag is True and x >= width/2) or (flag is False and x < width/2):
                    sequences.append([(x, y)] + find_best_path(x, pixels, y+1, width, flag))
    """sequences = []
    for i, pixel_row in enumerate(pixels):
        for pixel in pixel_row:
            if (flag is True and pixel[0] < width/2) or (flag is False and pixel[0] >= width/2):
                sequences.append(find_best_path(pixel, pixels, i+1, width, flag))"""
    return sequences

def create_image(pixels, height, width):
    image = np.zeros((height, width))
    for pixel_row in pixels:
        for x, y in pixel_row:
            image[y, x] = 1
    return image

def print_picture(pixels, height, width):
    """Construct and then print an image given a list of pixels."""
    image = create_image(pixels, height, width)
    imshow(image)
    show()

def line(image, B, flag):
    height, width = photo.shape
    rang = range(int(width/2), width) if flag is True else range(0, int(width/2))
    for i in rang:
        X = np.array([i, 1])
        Y = np.dot(X, B)
        if Y > 0 and Y < height-1:
            image[int(Y), i] = 1
            image[int(Y)-1, i] = 1
            image[int(Y)+1, i] = 1
    return image
            

def find_lanes(image):
    #Right = True
    ret = []
    height, width = image.shape
    image = line_scan(image, 5)
    #pixels = discard_noise(pixels, width/3)
    #image = blockify(image, 5, 5, 0.5)
    for Right in [False, True]:
        #pixels = [p for p in pixels if len(p) != 0]
        pixels = find_best_paths(image[range(0, int(height*0.8), 5)], width, Right)
        pixels = [[(p[0], p[1]*5) for p in l] for l in pixels]
        best = None
        bestScore = None
        
        for p in pixels:
            if len(p) > 1:
                B = linear_regression(p)
                t = int(width/2)
                h = np.sqrt(1 + abs(np.dot([t, 1], B) - np.dot([t+1, 1], B))**2)
                a = 1
                angle = np.arccos(a/h)
                score = abs(np.dot([t,1], B)-300)
                score = np.sqrt(sum([(y-np.dot([x, 1], B))**2 for x, y in p])/len(p)) * abs(np.dot([t,1], B)-300)
                #* abs(1-abs(angle-np.arccos(3/4)))
                #if np.dot([t, 1], B) < 300:
                #    score *= 1000
                #scores.append((score, p))
                if bestScore is None or score < bestScore:
                    bestScore = score
                    best = B
        ret.append(best)
    return ret

def draw_lanes(B1, B2, vid):
    if left is not None and right is not None:
        #B1 = linear_regression(left)
        #B2 = linear_regression(right)
        vid.append(line(line(photo, B1, False), B2, True))
    elif left is not None:
        #B1 = linear_regression(left)
        vid.append(line(photo, B1, False))
    elif right is not None:
        #B2 = linear_regression(right)
        vid.append(line(photo, B2, True))
    else:
        vid.append(photo)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("No image file given")
    elif not os.path.isfile(sys.argv[1]):
        print("{} is not a file".format(sys.argv[1]))
    elif sys.argv[1][-4:] == ".MOV":
        videogen = skvideo.io.vreader(sys.argv[1],as_grey=True)
        vid = []
        i = 1
        begin = time()
        for photo in videogen:
            photo = photo.reshape((1080, 1920))[220:-220, 560:-560]
            #print(photo.shape)
            #height, width = photo.shape
            #photo = line_scan(photo, 5).astype(np.uint8)*255
            #photo = blockify(photo, 20, 20, 0.8)*255
            left, right = find_lanes(photo)
            draw_lanes(left,right,vid)
            #vid.append(photo)
            #photo = line_scan(photo, 5)
            #photo = blockify(photo, 5, 5, 0.1)
            #photo = create_image(pixels, height, width)
            #photo[pixels] = 255
            #print(photo.shape)
            #vid.append(photo.astype(np.uint8)*255)
            if i%20 == 0:
                print(i)
            i+= 1
            if i == 500:
                break
        print("Algorithm framerate: {!s}".format(500/(time()-begin)))
        skvideo.io.vwrite("vid.mp4", vid)
    else:
        photo=mahotas.imread(sys.argv[1],as_grey=True)
        #photo = photo.astype(np.uint8)
        #gray()
        #imshow(photo)
        #show()
        Right = True
        height, width = photo.shape
        pixels = line_scan(photo, 5)
        print_picture(pixels, height, width)
        pixels = discard_noise(pixels, width/3)
        print_picture(pixels, height, width)
        pixels = blockify(pixels, 5, 1)
        print_picture(pixels, height, width)
        pixels = [p for p in pixels if len(p) != 0]
        print(pixels)
        pixels = find_best_paths(pixels, width, Right)
        pixels = [p for p in pixels if len(p) != 0]
        best = None
        bestScore = None
        nextBest = None
        scores = []        
        for p in pixels:
            print(p)
            if len(p) > 1:
                B = linear_regression(p)
                t = int(width/2)
                h = np.sqrt(1 + abs(np.dot([t, 1], B)**2 - np.dot([t+1, 1], B)**2))
                a = 1
                angle = np.arccos(a/h)
                #print(angle)
                score = np.sqrt(sum([(y-np.dot([x, 1], B))**2 for x, y in p])/len(p)) * np.exp(-abs(1-abs(angle-np.arccos(5/4))))
                #score = len(p)
                scores.append((score, p))
                if bestScore is None or score < bestScore:
                    bestScore = score
                    nextBest = best
                    best = p
        print(best)
        scores = sorted(scores, key=lambda x: x[0])
        print_picture([best], height, width)
        B = linear_regression(best)
        photo=mahotas.imread(sys.argv[1],as_grey=True)
        gray()
        imshow(line(photo, B, Right))
        #show()
        for s, p in scores[:1]:
            print(p)
            print(s)
            B = linear_regression(p)
            photo=mahotas.imread(sys.argv[1],as_grey=True)
            gray()
            imshow(line(photo, B, Right))
            show()


