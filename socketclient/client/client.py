#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback
import time

from . import libclient

class client():

    sel = selectors.DefaultSelector()

    def create_request(self, fieldName, value):
        if fieldName == "catid":
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(fieldName=fieldName, value=value),
            )
        elif fieldName == "title":
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(fieldName=fieldName, value=value),
            )
        else:
            return dict(
                type="binary/custom-client-binary-type",
                encoding="binary",
                content=bytes(fieldName + value, encoding="utf-8"),
            )


    def start_connection(self, host, port, request):
        addr = (host, port)
        print("starting connection to", addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = libclient.Message(self.sel, sock, addr, request)
        self.sel.register(sock, events, data=message)
    
    def send_request(self, host, port, fieldName, value):
        request = self.create_request(fieldName, value)
        self.start_connection(host, port, request)

        try:
            while True:
                events = self.sel.select(timeout=1)
                for key, mask in events:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except Exception:
                        print(
                            "main: error: exception for",
                            f"{message.addr}:\n{traceback.format_exc()}",
                        )
                        message.close()
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            self.sel.close()


def main():

    if len(sys.argv) != 5:
        print("usage:", sys.argv[0], "<host> <port> <fieldName> <value>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    fieldName, value = sys.argv[3], sys.argv[4]
    PPNs = ['18594650X',
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
        value = PPN
        myClient = client()
        myClient.send_request(host, port, fieldName, value)
        time.sleep(1)

if __name__ == "__main__":
    main()
