import sys
import socket

"""
Simple socket communication client
Adapted from https://medium.com/python-pandemonium/python-socket-communication-e10b39225a4c
Original code by Rodgers Ouma Mc'Alila
""" 

class client():

    def sendMessage(self, host, port, message):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = (host, int(port))
        print('connecting to {} port {}'.format(*server_address))
        sock.connect(server_address)

        try:

                # Send data
                print('sending {!r}'.format(message))
                sock.sendall(message)

                # Look for the response
                amount_received = 0
                amount_expected = len(message)

                while amount_received < amount_expected:
                    data = sock.recv(16)
                    amount_received += len(data)
                    print('received {!r}'.format(data))

        finally:
                print('closing socket')
                sock.close()

def main():

    if len(sys.argv) != 4:
        sys.stderr.write("USAGE: python cli-launch.py <host> <port> <message>\n")
        sys.exit()
    else:
        socketHost = sys.argv[1]
        socketPort = sys.argv[2]
        message = sys.argv[3]

        messageBytes = message.encode('utf-8')
        myClient = client()
        myClient.sendMessage(socketHost, socketPort, messageBytes)

if __name__ == "__main__":
    main()
