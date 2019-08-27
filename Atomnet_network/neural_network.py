import numpy as np
import gzip
import tarfile
import os
import shutil
import h5py
import random
from keras.models import Sequential
from keras.utils.training_utils import multi_gpu_model
from keras.layers import Dense, Activation, Conv3D, Flatten, Dropout
from keras.callbacks import CSVLogger, ModelCheckpoint, TensorBoard, EarlyStopping
import tensorflow as tf
import keras
import argparse
from tqdm import tqdm    
    
from Utilities import batch_generator


def shuffle_hdf5(filename, dataset, size=512):
    with h5py.File(filename, 'r+') as hdf5:
        data = hdf5[dataset]
        length = len(data)
        leftover = True if length%size > 0 else False
        bins = int(length/size)
        if len(data.shape()) > 1:
            store = np.zeros((size*2,)+data.shape()[1:])
        else:
            store = np.zeros((size*2,))
        for b in range(bins):
            store[:size] = data[(size*b):(size*(b+1))]
            for r in range(b+1, bins):
                store[size:] = data[(size*r):(size*(r+1))]
                np.random.shuffle(store)
                data[(size*r):(size*(r+1))] = store[size:]
            if leftover is True:
                leftover_elements = length - bins*size
                store[size:(size+leftover_elements)] = data[(bins*size):]
                np.random.shuffle(store[:(size+leftover_elements)])
                data[(bins*size):] = store[size:(size+leftover_elements)]
            data[(size*b):(size*(b+1))] = store[:size]


def read_cubes(file_name):
    """Generates 20 by 20 by 20 cubes from file."""
    if file_name.endswith(".gz"):
        with gzip.open(file_name, 'rt') as gz:
            try:
                next(gz)
            except UnicodeDecodeError:
                pass
            next(gz)
            for line in gz:
                line = line.rstrip().split(",")
                line = np.array([float(l) for l in line]).reshape((20,20,20,1))
                yield line
    elif file_name.endswith(".csv"):
        with open(file_name, 'rt') as csv:
            for line in csv:
                line = line.rstrip().split(",")
                line = np.array([float(l) for l in line]).reshape((20,20,20,1))
                yield line

def create_model():
    model = Sequential()
    model.add(Conv3D(128, (5, 5, 5), input_shape=(20,20,20,1))) # 16,16,16,1
    model.add(Activation('relu'))
    model.add(Conv3D(256, (3, 3, 3))) # 14,14,14,1
    model.add(Activation('relu'))
    model.add(Conv3D(256, (3, 3, 3))) # 12,12,12,1
    model.add(Activation('relu'))
    model.add(Conv3D(256, (3, 3, 3))) # 10,10,10,1
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Activation('sigmoid'))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    
    return model

def create_callbacks():
    csv_logger = CSVLogger('training.log', append=True)
    #model_logger = ModelCheckpoint('weights.E{epoch:02d}-L{loss:.2f}.hdf5', monitor='loss', save_best_only=True)
    tensor_logger = TensorBoard()
    #earlyStop = EarlyStopping(monitor='loss', min_delta=0.01)
    call = [csv_logger, tensor_logger]
    
    return call
    
def limit_GPU_memory(limit=1.0):
    # TensorFlow wizardry
    config = tf.ConfigProto()
     
    # Don't pre-allocate memory; allocate as-needed
    #config.gpu_options.allow_growth = True
     
    # Only allow a total of half the GPU memory to be allocated
    config.gpu_options.per_process_gpu_memory_fraction = limit
     
    # Create a session with the above options specified.
    keras.backend.tensorflow_backend.set_session(tf.Session(config=config))

def generator_training(model, data, generator_size):
    '''Run training on model with generator data in batches using Keras.'''
    call = create_callbacks()
    model.fit_generator(data, steps_per_epoch=generator_size,
                        callbacks=call)
    # Compress all logging files.
    #with tarfile.open("experiment.tar.gz", "w:gz") as tar:
    #    tar.add('logs')
    #    shutil.rmtree('logs')
    #    tar.add('training.log')
    #    os.remove('training.log')
    #
                        
def generator_validation(model, data, generator_size):
    '''Run training on model with generator data in batches using Keras.'''
    accuracy = model.evaluate_generator(data, steps=generator_size)[1]
    return accuracy
    
def batch_training(model, data, generator_size):
    '''Run training on model with generator data in batches.'''
    BATCH_SIZE = 32
    past_losses = []
    batches = tqdm(data, total=generator_size)
    for batch_x, batch_y in batches:
        x = model.train_on_batch(batch_x, batch_y)[0]
        x = x*len(batch_x)
        past_losses.append(x)
        batches.set_description('AVG Loss: {:2.3f}'.format(np.mean(past_losses)/BATCH_SIZE))
        
def batch_validation(model, data, generator_size):
    '''Run validation on model with generator data in batches.'''
    losses = []
    for batch_x, batch_y in tqdm(data, total=generator_size):
        y = model.predict_on_batch(batch_x)
        y = np.sum(np.round(y) == batch_y)
        losses.append(y)
    return np.sum(losses)/generator_size
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--Generator", help="Use Keras Generator.",
                    action="store_true")
    args = parser.parse_args()

    use_batch = args.Generator
    
    limit_GPU_memory(0.7)
    
    keras.backend.set_floatx('float16')
    typez=keras.backend.floatx()
    model = create_model()
    
    with open("structure.json", "w") as json:
        json.write(model.to_json())
    
    #model = multi_gpu_model(model, 2)
    model.compile(optimizer='SGD',
                  metrics=['accuracy'],
                  loss='mean_squared_error')
    
    ################################################
    # Train model and run validation
    ################################################
    with h5py.File('completed0.hdf5', 'r') as hf:
        model.fit(hf['mydataset'], hf['labels'], shuffle='batch')



