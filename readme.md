# Iromlab socket client demo

This repository contains a simple socket client that demonstrates the use of the socket interface in [Iromlab](https://github.com/KBNLresearch/iromlab). It includes both a command-line tool and a graphical client.

Make sure to start up the server (i.e. Iromlab with *enableSocketAPI* set to *True*) before running the client (not doing so will result in an error message).

## Usage command line tool

    python cli-launch.py <host> <port> <message>

As an example, the invocation below sends the identifier string "18594650X" to a server listening on port 65432 of localhost (=IP address 127.0.0.1):

    python cli-launch.py 127.0.0.1 65432 18594650X

## Usage GUI client

Start the client using this command:

    python gui-launch.py

Then enter some text in the text widget and press the Submit button.
