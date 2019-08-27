import unittest
import numpy as np

from Utilities import batch_generator

class TestBatchGenerator(unittest.TestCase):
    '''Test Class for batch_generator.'''
    
    def test_batch_shape(self):
        '''Test that the batch_generator produces predictable batches.'''
        array = np.empty((32,1))
        self.assertEqual(next(batch_generator(array, 32)).shape, (32,1))
        array = np.empty((64,10))
        self.assertEqual(next(batch_generator(array, 32)).shape, (32,10))
        array = np.empty((16,1))
        self.assertEqual(next(batch_generator(array, 32)).shape, (16,1))
        array = np.empty((32,1))
        self.assertEqual(next(batch_generator(array[:16], 32)).shape, (16,1))
        
    def test_batch_shape_cached(self):
        '''Test that the batch_generator with cache produces predictable batches.'''
        cache_size = 4
        array = np.empty((32,1))
        self.assertEqual(next(batch_generator(array, 32, cache_size)).shape, (32,1))
        array = np.empty((64,1))
        self.assertEqual(next(batch_generator(array, 32, cache_size)).shape, (32,1))
        array = np.empty((16,1))
        self.assertEqual(next(batch_generator(array, 32, cache_size)).shape, (16,1))
        array = np.empty((32,1))
        self.assertEqual(next(batch_generator(array[:16], 32, cache_size)).shape, (16,1))
        
    def test_batch_value_cached(self):
        '''Test that the values of a batch are correct.'''
        array = np.arange(128).reshape((64, 2))
        test_array = np.arange(64).reshape((32, 2))
        Generator = batch_generator(array, 32, 2)
        equality = np.all(next(Generator) == test_array)
        self.assertTrue(equality)
        test_array = np.arange(64, 128).reshape((32, 2))
        equality = np.all(next(Generator) == test_array)
        self.assertTrue(equality)
        self.assertRaises(StopIteration, next, Generator)
        
        array = np.arange(126).reshape((63, 2))
        test_array = np.arange(64).reshape((32, 2))
        Generator = batch_generator(array, 32, 2)
        equality = np.all(next(Generator) == test_array)
        self.assertTrue(equality)
        test_array = np.arange(64, 126).reshape((31, 2))
        equality = np.all(next(Generator) == test_array)
        self.assertTrue(equality)
        self.assertRaises(StopIteration, next, Generator)
        
    def test_batch_slice_shape_cached(self):
        '''Test that the batch_generator with cache produces predictable batches.
        
        Test the slice funcationality
        '''
        cache_size = 4
        array = np.empty((32,1))
        self.assertEqual(next(batch_generator(array, 32, cache_size, start=16)).shape, (16,1))
        array = np.empty((64,1))
        self.assertEqual(next(batch_generator(array, 32, cache_size, start=16, end=32)).shape, (16,1))
        
    def test_batch_slice_value_cached(self):
        '''Test that the values of a batch are correct.
        
        Test the slice funcationality.
        '''
        array = np.arange(128).reshape((64, 2))
        test_array = np.arange(32, 96).reshape((32, 2))
        Generator = batch_generator(array, 32, 2, start=16)
        equality = np.all(next(Generator) == test_array)
        self.assertTrue(equality)
        test_array = np.arange(96, 128).reshape((16, 2))
        equality = np.all(next(Generator) == test_array)
        self.assertTrue(equality)
        self.assertRaises(StopIteration, next, Generator)
        
        array = np.arange(64).reshape((32, 2))
        test_array = np.arange(32).reshape((16, 2))
        Generator = batch_generator(array, 32, 2, end=16)
        equality = np.all(next(Generator) == test_array)
        self.assertTrue(equality)
        self.assertRaises(StopIteration, next, Generator)
        
        array = np.arange(128).reshape((64, 2))
        test_array = np.arange(32, 64).reshape((16, 2))
        Generator = batch_generator(array, 32, 2, start=16, end=32)
        equality = np.all(next(Generator) == test_array)
        self.assertTrue(equality)
        self.assertRaises(StopIteration, next, Generator)
        
if __name__ == '__main__':
    unittest.main()