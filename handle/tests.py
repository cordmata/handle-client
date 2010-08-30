import unittest
from client import Client, HandleExists, HandleNotFound, BadRequest

class HandleClientTest(unittest.TestCase):
    """This is extremely bad form for unit testing -- each test depends on the
    successful run of a previous test. This is due to the fact we are testing 
    both this client and the remote service. Open to better ways of doing this."""
    
    HDL_SERVER_BASE = 'http://hdl.handle.net/'
    
    def setUp(self):
        self.client = Client('http://localhost:8080/services/handle', 
                             'handleAdmin', 'handletest')
        self.createdHandle = '2286/py-handleclient:newone'
        self.createdTarget = 'http://www.asu.edu'
        self.updatedTarget = 'http://lib.asu.edu'
        self.badTarget = 'asu.edu'
    
    def test_01_bad_request(self):
        self.assertRaises(BadRequest, self.client.create,
                          self.createdHandle, self.badTarget)
    
    def test_02_create(self):
        hdl = self.client.create(self.createdHandle, self.createdTarget)
        self.assertEqual('%s%s' % (HandleClientTest.HDL_SERVER_BASE, self.createdHandle), hdl)
    
    def test_03_create_handle_exists(self):
        self.assertRaises(HandleExists,
                          self.client.create, 
                          self.createdHandle, 
                          self.createdTarget)
    
    def test_04_read(self):
        tgt = self.client.read(self.createdHandle)
        self.assertEqual(tgt, self.createdTarget)
    
    def test_05_update(self):
        hdl = self.client.update(self.createdHandle, self.updatedTarget)
        self.assertEqual('%s%s' % (HandleClientTest.HDL_SERVER_BASE, self.createdHandle), hdl)
    
    def test_06_update_read(self):
        self.assertEqual(self.client.read(self.createdHandle), self.updatedTarget)
    
    def test_07_delete(self):
        self.assertTrue(self.client.delete(self.createdHandle))
    
    def test_08_read_not_found(self):
        self.assertEqual(self.client.read(self.createdHandle), None)
    
    def test_09_update_not_found(self):
        self.assertRaises(HandleNotFound, self.client.update, 
                          self.createdHandle, self.createdTarget)
        
    def test_10_update_with_create(self):
        hdl = self.client.update(self.createdHandle, self.updatedTarget, create=True)
        self.client.delete(self.createdHandle)
        self.assertEqual('%s%s' % (HandleClientTest.HDL_SERVER_BASE, self.createdHandle), hdl)
        
if __name__ == "__main__":
    unittest.main()