import numpy as np

def batch_generator(array, batch_size=32, cache_size=None, start=0, end=None):
    '''Produce a generator that generates batches for training.'''
    if end is None:
        end = len(array)
    length = end-start
    if cache_size is None:
        batches = int(length/batch_size)
        for i in range(batches):
            yield array[(start+i*batch_size):(start+(i+1)*batch_size)]
        if length != length/batch_size:
            yield array[(start+batches*batch_size):end]
    else:
        size = cache_size*batch_size
        number_of_cache = int(length/size)
        for num in range(number_of_cache):
            cache = array[(start + num*size):(start + (num+1)*size)]
            for i in range(cache_size):
                yield cache[(i*batch_size):((i+1)*batch_size)]
        if length/size != number_of_cache:
            remainder = length - number_of_cache*size
            batches = int(remainder/batch_size)
            cache = array[(start + number_of_cache*cache_size*batch_size):end]
            for i in range(batches):
                yield cache[(i*batch_size):((i+1)*batch_size)]
            if batches*batch_size != remainder:
                yield cache[(batches*batch_size):]
        
        
if __name__ == '__main__':
    import h5py
    from time import time, sleep
    from tqdm import tqdm
    
    
    with h5py.File('completed0.hdf5', 'r') as hf:
        data = hf['mydataset']
        begin = time()
        for i in batch_generator(hf['mydataset'], 1024, 8, start=32, end=2000):
            print(i.shape)
        print('Time Elapsed: {!s}'.format(time()-begin))
        
        
        