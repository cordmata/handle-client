from os.path import join
from urllib import quote

import requests

NO_CACHE = {'Cache-Control': 'no-cache'}


class Client(object):
    """This is a client for interacting with the ASU Handle
    Administration Web Service."""

    def __init__(self, url, username, password):
        self.baseurl = url.rstrip('/')
        self.auth = (username, password)

    def create(self, handle, target):
        """
        Request a handle be created for the supplied target under the
        supplied prefix. If no suffix is supplied one will be generated.

        @param target:
            String representing a valid URL, malformed URLs will result in a
            BadRequest exception.

        @param handle:
            String of the handle you want to create Example: '2286.9/af4y7fkd'

            see: http://www.handle.net/overviews/system_fundamentals.html#syntax

        @return: URL of the created handle (main Handle proxy server).

            Example: '2286.9/af4y7fkd'
        """
        resp = requests.post(
            self.URL(handle),
            data={'target': target},
            headers=NO_CACHE,
            auth=self.auth
        )
        if resp.status_code is 201:
            return resp.headers.get('location')
        raise HandleError(resp.status_code)

    def read(self, handle):
        """
        Retrieve the target of the supplied handle.

        @param handle: in the form of 'prefix/suffix'

        @return: URL the handle will resolve to.
        """
        resp = requests.get(self.URL(handle), auth=self.auth, headers=NO_CACHE)

        if resp.status_code is 204:
            return resp.headers.get('location')
        raise HandleError(resp.status_code)

    def update(self, handle, target):
        '''Change the target URL that an existing handle resolves to.

        @param handle: The handle to change.

        @param target: Valid URL of the new target.

        @return: The handle that was either updated or created.
        '''
        resp = requests.put(
            self.URL(handle),
            params={'target': target},
            auth=self.auth,
            headers=NO_CACHE
        )
        status = resp.status_code
        if status is 201 or status is 204:
            return resp.headers.get('location')
        raise HandleError(status)

    def delete(self, handle):
        """Remove the handle completely from the registry.

        @param handle: The handle to remove."""
        resp = requests.delete(
            self.URL(handle),
            auth=self.auth,
            headers=NO_CACHE
        )
        if resp.status_code is not 204:
            raise HandleError(resp.status_code)

    def URL(self, handle):
        return join(self.baseurl, quote(handle))

class HandleError(Exception):

    def __init__(self, status):
        if status is 400:
            self.message = 'Bad request.'
        if status is 401:
            self.message = 'Authentication failed.'
        if status is 403:
            self.message = "You don't have the right to do that."
        if status is 404:
            self.message = 'Handle not found.'
        if status is 409:
            self.message = 'Handle already exists.'

    def __unicode__(self):
        return unicode(self.message)

    def __str__(self):
        return self.message
