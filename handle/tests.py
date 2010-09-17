import unittest
from client import Client, HandleExists, HandleNotFound, BadRequest

class HandleClientTest(unittest.TestCase):
    """This is extremely bad form for unit testing. This is really an 
    integration test because each scenario depends on the side effects of a 
    successful run of a previous "unit". This is due to the fact we are testing 
    this client against a remote service. Therefore, I am collapsing these 
    connected actions into one test. I'm open to better ways of doing this."""
    
    HDL_SERVER_BASE = 'http://hdl.handle.net/'
    
    def setUp(self):
        self.client = Client('http://handle_int.lib.asu.edu:8080/handleservice', 
                             'handleAdmin', 'vj83j#W4')
        self.prefix = '2286.9'
        self.suffix = 'py-handleclient:newone'
        self.handle = self.prefix + '/' + self.suffix
        self.target = 'http://www.asu.edu'
        self.new_target = 'http://lib.asu.edu'
        self.bad_target = 'asu.edu'
    
    def test_bad_request(self):
        self.assertRaises(BadRequest, self.client.create, self.bad_target,
                          self.prefix, self.suffix)
    
    def test_supplied_handle(self):
        hdl = self.client.create(self.target, self.prefix, self.suffix)
        
        # ensure the returned value looks like we expect
        self.assertEqual('%s%s' % (self.HDL_SERVER_BASE, self.handle), hdl)
        
        # ensure we can not create one that already exists
        self.assertRaises(HandleExists, self.client.create, self.target,
                          self.prefix, self.suffix)
        
        # ensure expected handle target
        self.assertEqual(self.client.read(self.handle), self.target)   
        
        # test that we can update the target
        hdl = self.client.update(self.handle, self.new_target)
        self.assertEqual('%s%s' % (self.HDL_SERVER_BASE, self.handle), hdl)
        self.assertEqual(self.client.read(self.handle), self.new_target)
        
        # ensure we can delete
        self.assertTrue(self.client.delete(self.handle))
        
        # make sure we can not find the handle we just deleted
        self.assertEqual(self.client.read(self.handle), None)
        
        # make sure we can't update something that does not exist
        self.assertRaises(HandleNotFound, self.client.update, 
                          self.handle, self.target)
        
        # tell the update method to create it if not found
        hdl = self.client.update(self.handle, self.target, create=True)
        self.assertEqual('%s%s' % (self.HDL_SERVER_BASE, self.handle), hdl)

        self.client.delete(self.handle)
        
    def test_generated_handle(self):
        hdl_url = self.client.create(self.target, self.prefix)
        hdl = hdl_url.lstrip(self.HDL_SERVER_BASE)
        
        # ensure expected handle target
        self.assertEqual(self.client.read(hdl), self.target)
        self.client.delete(hdl)
        
if __name__ == "__main__":
    unittest.main()