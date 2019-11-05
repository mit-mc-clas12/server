""" 
Testing the type manager function for inference of scard type. 
"""
from collections import namedtuple 
import unittest 

from type_manager import manage_type 

# We have to fake that we're the scard_class 
SCard = namedtuple('SCard', 'name data')

class TestTypeManager(unittest.TestCase):

    def setUp(self):
        self.args = {} 
        self.data = {} 
        self.data['project'] = 'test'
        self.data['group'] = 'test'
        self.data['farm_name'] = 'test'
        self.data['gcards'] = '/jlab/clas12Tags/gcards/clas12-default.gcard'

    def test_one_local_file(self):
        self.data['generator'] = '/volatile/clas12/dmriser/esepp/0.txt'        
        scard = SCard(name='test', data=self.data)
        scard_type = manage_type(self.args, scard)
        self.assertEquals(scard_type, 2)

    def test_many_local_files(self):
        self.data['generator'] = '/volatile/clas12/dmriser/esepp/'        
        scard = SCard(name='test', data=self.data)
        scard_type = manage_type(self.args, scard)
        self.assertEquals(scard_type, 2)

    def test_one_online_file(self):
        self.data['generator'] = 'https://userweb.jlab.org/~dmriser/lund/esepp/0.txt'        
        scard = SCard(name='test', data=self.data)
        scard_type = manage_type(self.args, scard)
        self.assertEquals(scard_type, 2)

    def test_many_online_files(self):
        self.data['generator'] = 'https://userweb.jlab.org/~dmriser/lund/esepp/'        
        scard = SCard(name='test', data=self.data)
        scard_type = manage_type(self.args, scard)
        self.assertEquals(scard_type, 2)

    def test_type1(self):
        self.data['generator'] = 'gemc'        
        scard = SCard(name='test', data=self.data)
        scard_type = manage_type(self.args, scard)
        self.assertEquals(scard_type, 1)

    

if __name__ == '__main__':
    unittest.main() 
