import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from threading import Thread
import numpy as np
# import serial
# import serial.tools
# import serial.tools.list_ports
# from serial import Serial
from tkinter import Frame, Tk, Image, Button, Text, Canvas, PhotoImage, Label, Entry, Toplevel
# from tkterminal import Terminal
# from paho_mqtt_sub import *
# from paho_mqtt_pub import *
# from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from threading import Thread




BAUDRATE = 115200
DEVICE = '/dev/ttyACM0'
SQUARE_OFFSET = 10
SCREEN_REFRESH = 500 # Refresh every 500 ms

HOST = "csse4011-iot.zones.eait.uq.edu.au"
TOPIC = "un44333289"

WINDOW_SIZE = '1200x900'





class Redirect():
    
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert('end', text)
        self.widget.see('end') # autoscroll

    def flush(self):
        pass

    


class AcousticFingerprintingApp(Tk):

    def __init__(self):

        super().__init__()

         # Main window settings
        self.title("Acoustic Fingerprinting App")
        # self.minsize(1200, 1000)
        self.geometry(WINDOW_SIZE)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Window is split into the graphing and logging for displaying/debugging info.
        self.frame_display = Frame(master=self, background='black')
        self.frame_text = Frame(master=self, background='white')
        self.frame_display.pack(side='top', expand=True, fill='both')
        self.frame_text.pack(side='bottom', expand=True, fill='both')
        # self.frame_text.grid(row=1, column=0, sticky='nesw')
        # self.frame_display.grid(row=0, column=0, sticky='nesw')

        self.raw_graph = Frame(master=self.frame_display, bg='red')
        self.raw_graph.pack(side='left', expand=True, fill='both')
        self.fft_graph = Frame(master=self.frame_display, background='blue')
        self.fft_graph.pack(side='right', expand=True, fill='both')
   

        self.raw_data_fig = self.configure_raw_data_plot()
        self.raw_data_canvas = FigureCanvasTkAgg(self.raw_data_fig, master=self.raw_graph)
        self.raw_data_canvas.get_tk_widget().pack(expand=True, fill='both')
        self.raw_data_canvas.draw()
        self.fft_data_fig = self.configure_fft_data_plot()
        self.fft_data_canvas = FigureCanvasTkAgg(self.fft_data_fig, master=self.fft_graph)
        self.fft_data_canvas.get_tk_widget().pack(expand='True', fill='both')
        self.fft_data_canvas.draw()

        #Zephyr Heartrate Sensor CB:C6:14:E6:FC:92
        # Characteristic # 3



    

        # # MQTT Connection
        # self.mqttc = self._connect_mqtt(HOST, TOPIC)

        # # Setup serial connection
        # self.serial = self._connect_device(DEVICE)

    
    def configure_raw_data_plot(self) -> Figure:

        fig = Figure()
        ax = fig.add_subplot(111)
        ax.set_title("Raw Data Plot")
        ax.set_xlabel("Something")
        ax.set_ylabel("Something Else")
        ax.set_xlim(0, 100)
        ax.set_ylim(-100, 100)
        # lines = ax.plot([],[])[0]


        return fig

    def configure_fft_data_plot(self):

        fig = Figure()
        ax = fig.add_subplot(111)
        ax.set_title("FFT Data Plot")
        ax.set_xlabel("Something")
        ax.set_ylabel("Something Else")
        ax.set_xlim(0, 100)
        ax.set_ylim(-100, 100)
        # lines = ax.plot([],[])[0]
        
        return fig




    def run(self):

        # self.graph_canvas.after(SCREEN_REFRESH, self._update_canvas)
        # self.pos_label.after(SCREEN_REFRESH, self._update_pos)
        self.mainloop()
