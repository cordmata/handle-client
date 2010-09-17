from httplib2 import Http 
from urllib import urlencode, quote

NO_CACHE = ('cache-control', 'no-cache') 
FORM_ENCODED = ('Content-type', 'application/x-www-form-urlencoded')

class Client(object):
    '''This is a client for interacting with the ASU Handle 
    Administration Web Service.'''
    
    REGISTRY_BASE_URL = 'http://hdl.handle.net/'
    
    def __init__(self, url, username, password):
        self.baseurl = url if url.endswith('/') else url + '/'
        self.http = Http()
        self.http.add_credentials(username, password)
        
    def create(self, target, prefix, suffix=None):
        '''Request a handle be created for the supplied target under the 
        supplied prefix. If no suffix is supplied one will be generated.
        
        @param target: String representing a valid URL, malformed URLs will
            result in a BadRequest exception.
            
        @param prefix: Prefix of the handle that the service is able to register
            handles under. Example: '2286.9'
        
        @param suffix: A string unique in the namespace of the supplied prefix. 
            If not supplied the server will generate one.
        
        @return: String representing the handle in the form of 'suffix/prefix'
            Example: '2286.9/af4y7fkd'
        '''
        
        req_params = {'target': target, 'prefix': prefix}
        if suffix:
            req_params['suffix'] = suffix
        resp, cont = self.http.request(self.baseurl, 'POST', 
                                       headers=dict([NO_CACHE, FORM_ENCODED]), 
                                       body=urlencode(req_params))
        status = resp.get('status')
        if status == '201': 
            return resp.get('location').lstrip(self.REGISTRY_BASE_URL)
        if status == '409': 
            raise HandleExists()
        if status == '400': 
            raise BadRequest()
        raise HandleServerException(cont)
    
    def read(self, handle):
        '''Retrieve the target of the supplied handle.
        
        @param handle: in the form of 'prefix/suffix' 
        
        @return: URL the handle will resolve to.
        '''
        url = self._resource_url(handle)
        resp, cont = self.http.request(url, 'GET', headers=dict([NO_CACHE]))
        status = resp.get('status')
        if status == '204': 
            return resp.get('location')
        if status == '404': 
            return None
        if status == '400': 
            raise BadRequest()
        raise HandleServerException(cont)
    
    def update(self, handle, target, create=False):
        '''Change the target URL that an existing handle resolves to.
        
        @param handle: The handle to change.
        
        @param target: Valid URL of the new target.
        
        @param create: If set to True the supplied handle will be created
            with the specified target if it does not already exist.
        
        @return: The handle that was either updated or created.
        '''
        url = self._request_url(handle, target=target, create=create)
        resp, cont = self.http.request(url, 'PUT', headers=dict([NO_CACHE]))
        status = resp.get('status')
        if status == '201' or status == '204': 
            return resp.get('location').lstrip(self.REGISTRY_BASE_URL)
        if status == '400': 
            raise BadRequest()
        if status == '404': 
            raise HandleNotFound()
        raise HandleServerException(cont)
    
    def delete(self, handle):
        '''Remove the handle completely from the registry.
        
        @param handle: The handle to remove.'''
        resp, cont = self.http.request(self._resource_url(handle),
                                       'DELETE', headers=dict([NO_CACHE]))
        status = resp.get('status')
        if status == '204': 
            return True
        if status == '400': 
            raise BadRequest()
        raise HandleServerException(cont)
    
    def _resource_url(self, handle):
        if handle:
            return self.baseurl + quote(handle)
        return self.baseurl
    
    def _request_url(self, hdl, **kwargs):
        return self._resource_url(hdl) + '?' + urlencode(kwargs)

class HandleServerException(Exception):
    pass

class BadRequest(Exception):
    pass

class HandleNotFound(Exception):
    pass

class HandleExists(Exception):
    pass
