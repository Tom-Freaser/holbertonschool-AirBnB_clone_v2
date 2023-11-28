#!/usr/bin/python3
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
import os


class TestFileStorage(unittest.TestCase):
    '''
    FileStorage test
    '''
    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        super().__init__(*args, **kwargs)
        self.test_class = FileStorage

    def test_pathname(self):
        '''
        Attrib test
        '''
        test = self.test_class()
        self.assertIsInstance(test._FileStorage__file_path, str)

    def test_file_save(self):
        '''
        File creation test
        '''
        storage.save()
        self.assertTrue(os.path.exists('JSONstorage.json'))

    def test_objects(self):
        '''
        Test
        '''
        test = self.test_class()
        self.assertIsInstance(test._FileStorage__objects, dict)

    def tearDown(self):
        '''
        Destroy JSON file
        '''
        try:
            os.remove('JSONstorage.json')
        except:
            pass

    def test_file_empty(self):
        '''
        File empty test
        '''
        base = BaseModel()
        my_dict = base.to_dict()
        base.save()
        base2 = BaseModel(**my_dict)
        self.assertFalse(os.stat('JSONstorage.json').st_size == 0)