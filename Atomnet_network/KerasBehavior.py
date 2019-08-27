import unittest
import numpy as np

import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from keras.layers import Dense, Activation, Conv3D, Flatten, Dropout
from keras.models import Sequential
    
class TestBatchGenerator(unittest.TestCase):
    '''Test Keras for its behaviour.'''
    
    def test_keras_loss_calc_before_training(self):
        '''Show that Keras calculates the loss function before training.'''
        model = Sequential()
        model.add(Dense(1, input_shape=(10,)))
        model.compile(optimizer='SGD', loss='mean_squared_error')
        samples = np.random.rand(64, 10)
        labels = (np.random.rand(64, 1) > 0.5).astype(np.int32)
        y = model.predict_on_batch(samples)
        numpy_loss = np.mean(np.power(labels-y, 2))
        keras_loss = model.train_on_batch(samples, labels)
        keras_test_loss = model.test_on_batch(samples, labels)
        
        self.assertTrue(np.isclose(numpy_loss, keras_loss))
        
    def test_keras_loss_calc_after_training(self):
        '''Show that Keras doesn't calculates the loss function after training.'''
        model = Sequential()
        model.add(Dense(1, input_shape=(10,)))
        model.compile(optimizer='SGD', loss='mean_squared_error')
        samples = np.random.rand(64, 10)
        labels = (np.random.rand(64, 1) > 0.5).astype(np.int32)
        keras_loss = model.train_on_batch(samples, labels)
        y = model.predict_on_batch(samples)
        numpy_loss = np.mean(np.power(labels-y, 2))
        keras_test_loss = model.test_on_batch(samples, labels)
        
        self.assertFalse(np.isclose(numpy_loss, keras_loss))
        
    def test_keras_test_loss(self):
        '''Show that the loss function in Keras is being produced as thought.'''
        model = Sequential()
        model.add(Dense(1, input_shape=(10,)))
        model.compile(optimizer='SGD', loss='mean_squared_error')
        samples = np.random.rand(64, 10)
        labels = (np.random.rand(64, 1) > 0.5).astype(np.int32)
        y = model.predict_on_batch(samples)
        numpy_loss = np.mean(np.power(labels-y, 2))
        keras_test_loss = model.test_on_batch(samples, labels)

        self.assertTrue(np.isclose(numpy_loss, keras_test_loss))
        
    def test_keras_test_loss_batch(self):
        '''Show that the total loss can be calculated from batches.'''
        model = Sequential()
        model.add(Dense(1, input_shape=(10,)))
        model.compile(optimizer='SGD', loss='mean_squared_error')
        samples = np.random.rand(64, 10)
        labels = (np.random.rand(64, 1) > 0.5).astype(np.int32)
        test_loss_total = model.test_on_batch(samples, labels)
        test_loss_batch = []
        test_loss_batch.append(model.test_on_batch(samples[:32], labels[:32])*32)
        test_loss_batch.append(model.test_on_batch(samples[32:], labels[32:])*32)
        test_loss_batch = np.sum(test_loss_batch)/64
        

        self.assertTrue(np.isclose(test_loss_total, test_loss_batch))
        
if __name__ == '__main__':
    unittest.main()