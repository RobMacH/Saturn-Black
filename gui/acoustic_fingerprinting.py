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

from threading import Semaphore

from ble import connect_to_device


import settings

from paho_mqtt_sub import *
from paho_mqtt_pub import *


HELP_MSG = """Welcome to the Acoustic Fingerprinting App!:
    "Choose one of the following options.
    'p  Predict location
    'm  Send prediction over mqtt
    'q' Quit
: """




BAUDRATE = 115200
DEVICE = '/dev/ttyACM0'
SQUARE_OFFSET = 10
SCREEN_REFRESH = 500 # Refresh every 500 ms

HOST = "csse4011-iot.zones.eait.uq.edu.au"
TOPIC = "local44333289"

WINDOW_SIZE = '1200x900'

# recording = 0

def audio_callback(data):
    
    if settings.recording == 1:
    
        print(data)



class Redirect():
    
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert('end', text)
        self.widget.see('end') # autoscroll

    def flush(self):
        pass



class AcousticFingerprintingAppOld(Tk):

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
   

        self.raw_data_fig, self.ax_raw = self.configure_raw_data_plot()
        self.raw_data_canvas = FigureCanvasTkAgg(self.raw_data_fig, master=self.raw_graph)
        self.raw_data_canvas.get_tk_widget().pack(expand=True, fill='both')
        self.raw_data_canvas.draw()
        self.fft_data_fig, self.ax_fft = self.configure_fft_data_plot()
        self.fft_data_canvas = FigureCanvasTkAgg(self.fft_data_fig, master=self.fft_graph)
        self.fft_data_canvas.get_tk_widget().pack(expand='True', fill='both')
        self.fft_data_canvas.draw()

        self.plot_thread = Thread(name='plot', target=self.plot_data)


        #Zephyr Heartrate Sensor CB:C6:14:E6:FC:92
        # Characteristic # 3    



    def plot_data(self):

        lines = self.ax_raw.plot([],[])[0]

        while (1):

            pass



    

       

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


        return fig, ax

    def configure_fft_data_plot(self):

        fig = Figure()
        ax = fig.add_subplot(111)
        ax.set_title("FFT Data Plot")
        ax.set_xlabel("Something")
        ax.set_ylabel("Something Else")
        ax.set_xlim(0, 100)
        ax.set_ylim(-100, 100)
        # lines = ax.plot([],[])[0]
        
        return fig, ax




    def run(self):

        self.mainloop()


        



class AcousticFingerprintingApp():


    def __init__(self):

        # Globals
        settings.init()

        # Microphone connect
        self.peripheral, self.service_uuid, self.characteristic_uuid = connect_to_device()
        
        # MQTT Connection
        self.mqttc = self._connect_mqtt(HOST, TOPIC)
    

    def _connect_mqtt(self, host, topic):

        mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message
        mqttc.on_subscribe = on_subscribe
        mqttc.on_unsubscribe = on_unsubscribe

        mqttc.user_data_set([0])
        mqttc.connect(host)
        mqttc.subscribe(topic)
        mqttc.loop_start()

        return mqttc
    
    def send_msg_mqtt(self, index: int):

        msg_info = self.mqttc.publish(TOPIC, index, qos=1)



    def run(self):

        # Begin audio streaming
        try:

            content = self.peripheral.notify(self.service_uuid, self.characteristic_uuid, audio_callback)

            while True:

                res = input(HELP_MSG)

                if res == 'p':

                    settings.recording = 1
                    print("Carrying out prediction")
                    time.sleep(5)
                    settings.recording = 0
        
                elif res == 'q':

                    print("Thank-you for using the Acoustic Fingerprinting App, Good-bye!")
                    self.peripheral.disconnect()
                    break

                elif res == 'm':

                    ind = input("Please select room to send: ")
                    self.send_msg_mqtt(ind)
                    
                else:
                    print("Incorrect options, please select again")
                
        except KeyboardInterrupt:
            self.peripheral.disconnect()


        
