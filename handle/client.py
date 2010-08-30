from httplib2 import Http 
from urllib import urlencode, quote

NO_CACHE = {'cache-control':'no-cache'} 

class Client(object):
    
    def __init__(self, url, username, password):
        self.baseurl = url if url.endswith('/') else url + '/'
        self.http = Http()
        self.http.add_credentials(username, password)
        
    def create(self, handle, target):
        resp, cont = self.http.request(self._request_url(handle, target=target),
                                       'POST', headers=NO_CACHE)
        status = resp.get('status')
        if status == '201': return resp.get('location')
        if status == '409': raise HandleExists()
        if status == '400': raise BadRequest()
        raise HandleServerException(cont)
    
    def read(self, handle):
        resp, cont = self.http.request(self._resource_url(handle), 
                                       'GET', headers=NO_CACHE)
        status = resp.get('status')
        if status == '204': return resp.get('location')
        if status == '404': return None
        if status == '400': raise BadRequest()
        raise HandleServerException(cont)
    
    def update(self, handle, target, create=False):
        resp, cont = self.http.request(self._request_url(handle, 
                                                         target=target, 
                                                         create=create), 
                                       'PUT', headers=NO_CACHE)
        status = resp.get('status')
        if status == '201' or status == '204': return resp.get('location')
        if status == '400': raise BadRequest()
        if status == '404': raise HandleNotFound()
        raise HandleServerException(cont)
    
    def delete(self, handle):
        resp, cont = self.http.request(self._resource_url(handle),
                                       'DELETE', headers=NO_CACHE)
        status = resp.get('status')
        if status == '204': return True
        if status == '400': raise BadRequest()
        raise HandleServerException(cont)
    
    def _resource_url(self, handle):
        return self.baseurl + quote(handle)
    
    def _request_url(self, handle, **kwargs):
        return self._resource_url(handle) + '?' + urlencode(kwargs)

class HandleServerException(Exception):
    pass

class BadRequest(Exception):
    pass

class HandleNotFound(Exception):
    pass

class HandleExists(Exception):
    pass
