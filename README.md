# TP_redes
Implementation of a program pair that operates in the client-server model over the TCP

This code was developed in Python3.6

### It's necessary to install the following libraries:

    $ pip install threaded
    $ pip install sockets
    
## To run 

### Initiate the server
    $ python3 init_server.py
    
### Initiate support client
    $ python3 support_client.py
    
### Initiate the client who will send the request
    $ python3 client_requestor.py

## Program

1- Server record the clients connections.

2- Client Requestor send a number of words first and after send the words.

3- Server receive the request and choice a randomly registered support client to send a request.

4- The support client receive the request and return the parsed words. vowels, consonants and numbers.

5- The server receives the response from support and sends the response to the requesting client.

6- Resquestor client receive the response and save it in a document file "output.txt".

7- The server send a shutdown message to all clients and finish the execution.

### Client Requestor
The program will read the document "modelo_entrada.txt" remove comment lines and parse the first element (a number), which will be a number of lines to send a server. (Obs: Client requestor is also a support client

### Server
The server will receive the data and send to a random client.

### Support Client
The support client will receive the server data and separate the word into vowels, consonants and numbers. If the string don't is a alfanumeric, the client will send a error string.

![redes](https://user-images.githubusercontent.com/51409770/110681493-a78e0480-81b8-11eb-842b-374bc5bc92c2.png)

