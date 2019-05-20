import socket
import time

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
    socketHost = '127.0.0.1'
    socketPort = '65432'

    PPNs = ['18594650X',
            'Sluwe Sjaantje sloeg de slome slager',
            '230370241',
            '216562856 ',
            'aap',
            'noot',
            'mies',
            'piet',
            'japie',
            '',
            '376144572'
            '',
            '',
            '37750159X',
                        '230370241',
            '216562856 ',
            'aap',
            'noot',
            'mies',
            'piet',
            'japie',
            '',
            '376144572'
            '',
            '']

    for PPN in PPNs:
        messageBytes = PPN.encode('utf-8')
        myClient = client()
        myClient.sendMessage(socketHost, socketPort, messageBytes)
        time.sleep(1)

if __name__ == "__main__":
    main()
