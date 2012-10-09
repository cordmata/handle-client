Handle Client
=============


This is a very thin client for the [Handle Server Web API](https://github.com/cordmata/handle-service).
There's really not much to it, it's basically an educational reference implementation for the service,
but [we're using it](http://repository.asu.edu/), so feel free.

Installation
------------

`pip install -e git+https://github.com/cordmata/handle-client.git#egg=handle`

Usage
-----

```python
from handle import Client

client = Client("http://your.server.org/handle-service/", "handleAdmin", "yourPass")

client.create("2286.9/test", "http://example.org")
#>>> http://hdl.handle.net/2286.9/test

client.read("2286.9/test")
#>>> http://example.org

client.update("2286.9/test", "http://new.example.org")
#>>> http://hdl.handle.net/2286.9/test

client.delete("2286.9/test")
```

Told you...not much to it.
