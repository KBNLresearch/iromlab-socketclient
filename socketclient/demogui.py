#! /usr/bin/env python
"""
Demo that shows use of Iromlab socket interface

"""

import sys
import os
import imp
import time
import glob
import threading
import queue
import tkinter as tk
from tkinter import ttk
from . import config
from .client import client


class GUI(tk.Frame):

    """This class defines the graphical user interface + associated functions
    for associated actions
    """

    def __init__(self, parent, *args, **kwargs):
        """Initiate class"""
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.build_gui()

    def on_quit(self, event=None):
        os._exit(0)


    def on_submit(self, event=None):
        """Process one record and add it to the queue after user pressed submit button"""

        # Fetch entered values (strip any leading / tralue whitespace characters)
        if config.enablePPNLookup:
            fieldName = "catid"
            value = self.catid_entry.get().strip()
            self.catidOld = value
        else:
            fieldName = "title"
            value = self.title_entry.get().strip()
            self.titleOld = value

        # Send value TODO add code here ..
        myClient = client()
        request = myClient.create_request(fieldName, value)
        myClient.start_connection(config.socketHost, int(config.socketPort), request)

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

        # Reset entry fields and set focus on PPN / Title field
        if config.enablePPNLookup:
            self.catid_entry.delete(0, tk.END)
            self.catid_entry.focus_set()
        else:
            self.title_entry.delete(0, tk.END)
            self.title_entry.focus_set()

    def build_gui(self):
        """Build the GUI"""
                
        self.root.title('socket demo')
        self.root.option_add('*tearOff', 'FALSE')
        self.grid(column=0, row=0, sticky='ew')
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=1, uniform='a')
        self.grid_columnconfigure(2, weight=1, uniform='a')
        self.grid_columnconfigure(3, weight=1, uniform='a')

        if config.enablePPNLookup:
            # Catalog ID (PPN)
            tk.Label(self, text='PPN').grid(column=0, row=3, sticky='w')
            self.catid_entry = tk.Entry(self, width=20, state='normal')

            self.catid_entry.grid(column=1, row=3, sticky='w')
        else:
            # PPN lookup disabled, so present Title entry field
            tk.Label(self, text='Title').grid(column=0, row=3, sticky='w')
            self.title_entry = tk.Entry(self, width=45, state='normal')
            self.title_entry.grid(column=1, row=3, sticky='w', columnspan=3)

        self.submit_button = tk.Button(self,
                                       text='Submit',
                                       height=2,
                                       width=4,
                                       underline=0,
                                       state='normal',
                                       command=self.on_submit)
        self.submit_button.grid(column=1, row=6, sticky='ew')

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

def main():
    """Main function"""
    root = tk.Tk()
    myGUI = GUI(root)
    # This ensures application quits normally if user closes window
    root.protocol('WM_DELETE_WINDOW', myGUI.on_quit)

    while True:
        try:
            root.update_idletasks()
            root.update()
            time.sleep(0.1)
        except KeyboardInterrupt:
            os._exit(0)

if __name__ == "__main__":
    main()
