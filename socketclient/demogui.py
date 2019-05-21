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
from . import client
from . import config

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
        value = self.catid_entry.get().strip()
        
        # Encode entered value to bytes
        # TODO: may need exception handler for encode errors
        messageBytes = value.encode('utf-8')

        # Send message
        myClient = client.client()
        myClient.sendMessage(config.socketHost, config.socketPort, messageBytes)

        # Reset entry fields and set focus on PPN / Title field
        self.catid_entry.delete(0, tk.END)
        self.catid_entry.focus_set()

    def build_gui(self):
        """Build the GUI"""
                
        self.root.title('Socket client demo')
        self.root.option_add('*tearOff', 'FALSE')
        self.grid(column=0, row=0, sticky='ew')
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=3, uniform='a')

        # Catalog ID (PPN) or title
        tk.Label(self, text='PPN (or title)').grid(column=0, row=3, sticky='w')
        self.catid_entry = tk.Entry(self, width=60, state='normal')
        self.catid_entry.grid(column=1, row=3, sticky='w')

        # Submit button
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
    # This ensures the application quits normally if user closes window
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
