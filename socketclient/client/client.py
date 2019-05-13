#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

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

def main():

    if len(sys.argv) != 5:
        print("usage:", sys.argv[0], "<host> <port> <fieldName> <value>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    fieldName, value = sys.argv[3], sys.argv[4]
    myClient = client()
    request = myClient.create_request(fieldName, value)
    myClient.start_connection(host, port, request)

    try:
        while True:
            events = myClient.sel.select(timeout=1)
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
            if not myClient.sel.get_map():
                break
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        myClient.sel.close()

if __name__ == "__main__":
    main()
