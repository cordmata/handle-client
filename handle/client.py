import requests


class Client(object):
    """Client for interacting with the ASU Handle  Web Service."""

    def __init__(self, url, username, password, verify_ssl=True):
        self.baseurl = url.rstrip('/') + '/'
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.verify = verify_ssl
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'User-Agent': 'asu-handle-client'
        })

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

        resp = self.session.post(
            self.baseurl + handle, data={"target": target}
        )
        if resp.status_code is 201:
            return resp.headers.get("location")
        raise HandleError(resp.status_code)

    def read(self, handle):
        """
        Retrieve the target of the supplied handle.

        @param handle: in the form of 'prefix/suffix'

        @return: URL the handle will resolve to.

        """
        resp = self.session.get(self.baseurl + handle)
        if resp.status_code is 204:
            return resp.headers.get("location")
        raise HandleError(resp.status_code)

    def update(self, handle, target):
        """Change the target URL that an existing handle resolves to.

        @param handle: The handle to change.

        @param target: Valid URL of the new target.

        @return: The handle that was either updated or created.

        """
        resp = self.session.put(
            self.baseurl + handle, params={"target": target}
        )
        status = resp.status_code
        if status is 201 or status is 204:
            return resp.headers.get("location")
        raise HandleError(status)

    def delete(self, handle):
        """Remove the handle completely from the registry.

        @param handle: The handle to remove."""
        resp = self.session.delete(self.baseurl + handle)
        if resp.status_code is not 204:
            raise HandleError(resp.status_code)


class HandleError(Exception):

    def __init__(self, status):
        status = int(status)
        if status == 400:
            self.message = "Bad request."
        elif status == 401:
            self.message = "Authentication failed."
        elif status == 403:
            self.message = "You don't have the right to do that."
        elif status == 404:
            self.message = "Handle not found."
        elif status == 409:
            self.message = "Handle already exists."
        else:
            self.message = "Handle Server error."

    def __unicode__(self):
        return unicode(self.message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.__str__()
