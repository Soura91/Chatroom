#!/usr/bin/env python3

"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
add_name = dict([])
######################
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,client_address)).start()

#######################
def handle_client(client,client_address):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf8")
    add_name[str(client_address)] = name
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg == bytes("{knock-knock}", "utf8"):
            cname = ""
            for x in add_name:
                cname += " " +add_name[x]
            client.send(bytes("{knock-knock} Who's there? We are: %s" % cname, "utf8"))
            continue
            broadcast(msg, name+": ")
        elif msg == bytes("{quit}", "utf8"):
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del add_name[str(client_address)]
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break
        elif msg == bytes("{fire}", "utf8"):
            broadcast(msg, name + ": ")
            broadcast(bytes("%s evacuating...!" % name, "utf8"))
            time.sleep(30)
            client.close()
            del add_name[str(client_address)]
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break
        else:
            broadcast(msg, name + ": ")


################

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

##################### main #############
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
