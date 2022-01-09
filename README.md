# chat-app
`server.py` is intended to be run on a server, and `client.py` is to be distributed to clients. The encryption key and ports must remain consistent between the server and clients. Custom key generation can be done using the `fernet` library in python.


In the future I hope to turn this into an onion site with more than one layer of encryption along with an extensive user verification process.
