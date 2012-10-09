import unittest

from mock import Mock, patch

import client
from client import Client, HandleError

HANDLE = "2286/test"
HANDLE_PROXY = "http://hdl.handle.net/"
HANDLE_URL = HANDLE_PROXY + HANDLE
TARGET = "http://www.asu.edu"
BAD_TARGET = "asu.edu"
CLIENT = Client(
    "http://handle.lib.asu.edu/handleservice",
    "doesNot", "matter"
)

class HandleClientTest(unittest.TestCase):

    @patch("client.requests")
    def test_create(self, requests):
        response = Mock()
        response.status_code = 201
        response.headers = {"location": HANDLE_URL}
        requests.post = Mock(return_value=response)
        hdl = CLIENT.create(HANDLE, TARGET)
        self.assertEqual(hdl, HANDLE_URL)

    @patch("client.requests")
    def test_read(self, requests):
        response = Mock()
        response.status_code = 204
        response.headers = {"location": TARGET}
        requests.get = Mock(return_value=response)
        target = CLIENT.read(HANDLE)
        self.assertEqual(target, TARGET)

    @patch("client.requests")
    def test_update(self, requests):
        response = Mock()
        response.status_code = 204
        response.headers = {"location": HANDLE_URL}
        requests.put = Mock(return_value=response)
        hdl = CLIENT.update(HANDLE, TARGET)
        self.assertEqual(hdl, HANDLE_URL)

    @patch("client.requests")
    def test_delete(self, requests):
        response = Mock()
        response.status_code = 204
        requests.delete = Mock(return_value=response)
        target = CLIENT.delete("2286/test")

    @patch("client.requests")
    def test_not_found(self, requests):
        response = Mock()
        response.status_code = 404
        requests.get = Mock(return_value=response)
        with self.assertRaisesRegexp(HandleError, "Handle not found."):
            CLIENT.read(HANDLE)

    @patch("client.requests")
    def test_bad_request(self, requests):
        response = Mock()
        response.status_code = 400
        requests.put = Mock(return_value=response)
        with self.assertRaisesRegexp(HandleError, "Bad req*"):
            CLIENT.update(HANDLE, BAD_TARGET)

    @patch("client.requests")
    def test_unauthorized(self, requests):
        response = Mock()
        response.status_code = 403
        requests.post = Mock(return_value=response)
        with self.assertRaisesRegexp(HandleError, "You don't*"):
            CLIENT.create(HANDLE, BAD_TARGET)


if __name__ == "__main__":
    unittest.main()
