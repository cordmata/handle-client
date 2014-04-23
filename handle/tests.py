import unittest

from mock import Mock
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

    def test_create(self):
        response = Mock()
        response.status_code = 201
        response.headers = {"location": HANDLE_URL}
        CLIENT.session.post = Mock(return_value=response)
        hdl = CLIENT.create(HANDLE, TARGET)
        self.assertEqual(hdl, HANDLE_URL)

    def test_read(self):
        response = Mock()
        response.status_code = 204
        response.headers = {"location": TARGET}
        CLIENT.session.get = Mock(return_value=response)
        target = CLIENT.read(HANDLE)
        self.assertEqual(target, TARGET)

    def test_update(self):
        response = Mock()
        response.status_code = 204
        response.headers = {"location": HANDLE_URL}
        CLIENT.session.put = Mock(return_value=response)
        hdl = CLIENT.update(HANDLE, TARGET)
        self.assertEqual(hdl, HANDLE_URL)

    def test_delete(self):
        response = Mock()
        response.status_code = 204
        CLIENT.session.delete = Mock(return_value=response)
        target = CLIENT.delete("2286/test")

    def test_not_found(self):
        response = Mock()
        response.status_code = 404
        CLIENT.session.get = Mock(return_value=response)
        with self.assertRaisesRegexp(HandleError, "Handle not found."):
            CLIENT.read(HANDLE)

    def test_bad_request(self):
        response = Mock()
        response.status_code = 400
        CLIENT.session.put = Mock(return_value=response)
        with self.assertRaisesRegexp(HandleError, "Bad req*"):
            CLIENT.update(HANDLE, BAD_TARGET)

    def test_unauthorized(self):
        response = Mock()
        response.status_code = 403
        CLIENT.session.post = Mock(return_value=response)
        with self.assertRaisesRegexp(HandleError, "You don't*"):
            CLIENT.create(HANDLE, BAD_TARGET)


if __name__ == "__main__":
    unittest.main()
