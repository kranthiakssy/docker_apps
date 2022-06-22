# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 11:30:41 2020

@author: Administrator
"""


# import tkinter as tk
# from tkinter import *
# from tkinter.ttk import *
# from tkinter import messagebox
#from tkinter import scrolledtext
# from PIL import ImageTk,Image
#import numpy as np
# import pandas as pd
import datetime
#import cryptography
#from cryptography.fernet import Fernet
#import os
# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
from pymodbus.server.sync import StartTcpServer
#from pymodbus.server.sync import StartTlsServer
#from pymodbus.server.sync import StartUdpServer
#from pymodbus.server.sync import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

#from pymodbus.transaction import ModbusRtuFramer, ModbusBinaryFramer
# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)



# def log_file(msg,file='../gen/comm_log.txt'):
#     with open(file,"a") as f:
#         f.write(msg+'\n')
        
# with open('../gen/comm_log.txt',"a") as f:
#     f.write('Log File Created on {0}\n'.format(datetime.datetime.now()))
        
# sh1 = tk.Tk()
# sh1.geometry("430x260-8-200")
# sh1.title("BTune - MODBUS Server")
# sh1.configure(bg='#e0e0e0')

# sh1.iconbitmap('../bin/logo/btune-logo.ico')

# fr0_sh1 = tk.Frame(sh1, bg='#e0e0e0')
# fr0_sh1.grid(row=0, column=0, padx=10)

# my_img_sh1 = ImageTk.PhotoImage(Image.open("../bin/logo/bhel-logo.jpg"))
# my_label_sh1 = tk.Label(fr0_sh1, image=my_img_sh1)
# my_label_sh1.grid(row=0, column=0, padx=5, pady=2)

# lb1_sh1 = tk.Label(fr0_sh1, text="Bharat Heavy Electricals Limited\nMODBUS SERVER",
#                    font=("Calibri",11),
#                    bg='#e0e0e0'
#                    )
# lb1_sh1.grid(row=0, column=1, pady=5)

# my_img_sh2 = ImageTk.PhotoImage(Image.open("../bin/logo/btune-logo.jpg"))
# my_label_sh2 = tk.Label(fr0_sh1, image=my_img_sh2)
# my_label_sh2.grid(row=0, column=2, padx=5, pady=2)

# fr1_sh1 = tk.LabelFrame(sh1,
#                    text="Enter MODBUS Server Details",
#                    padx=80,
#                    pady=5,
#                    bg='#e0e0e0',
#                    relief='raised',
#                    bd=2
#                    )
# fr1_sh1.grid(row=2,column=0,pady=5,padx=10)

# lb1_fr1 = tk.Label(fr1_sh1, text="Enter Server IP address", bg='#e0e0e0')
# lb1_fr1.grid(row=0, column=0)

# sip_addi = tk.StringVar(fr1_sh1, value='172.16.160.65')
# sip_add = tk.Entry(fr1_sh1, textvariable=sip_addi, width=15, relief='sunken', bd=2)
# sip_add.grid(row=0, column=1, pady=8, padx=10)
# sip_add.focus()


# lb2_fr1 = tk.Label(fr1_sh1, text="Enter Server Port No", bg='#e0e0e0')
# lb2_fr1.grid(row=1, column=0)

# sport_noi = tk.IntVar(fr1_sh1, value=502)
# sport_no = tk.Entry(fr1_sh1, textvariable=sport_noi, width=6, relief='sunken', bd=2)
# sport_no.grid(row=1, column=1, pady=8, padx=10)
# sport_no.focus()


# def run_server():
#     # Data from User Interface
#     sip_add_in = sip_add.get()
#     sport_no_in = int(sport_no.get())
#     try:                        
#         lb2_sh1 = tk.Label(sh1, text="Server Started", bg='#e0e0e0')
#         lb2_sh1.grid(row=4, column=0, padx=10, pady=5)
        
#         log_file('Server tried to start at IP:{0}, Port:{1} on {2}'\
#                  .format(sip_add_in,sport_no_in,datetime.datetime.now())
#                  )
        
            
# ----------------------------------------------------------------------- #
# initialize your data store
# ----------------------------------------------------------------------- #
# The datastores only respond to the addresses that they are initialized to
# Therefore, if you initialize a DataBlock to addresses of 0x00 to 0xFF, a
# request to 0x100 will respond with an invalid address exception. This is
# because many devices exhibit this kind of behavior (but not all)::
#
#     block = ModbusSequentialDataBlock(0x00, [0]*0xff)
#
# Continuing, you can choose to use a sequential or a sparse DataBlock in
# your data context.  The difference is that the sequential has no gaps in
# the data while the sparse can. Once again, there are devices that exhibit
# both forms of behavior::
#
#     block = ModbusSparseDataBlock({0x00: 0, 0x05: 1})
#     block = ModbusSequentialDataBlock(0x00, [0]*5)
#
# Alternately, you can use the factory methods to initialize the DataBlocks
# or simply do not pass them to have them initialized to 0x00 on the full
# address range::
#
#     store = ModbusSlaveContext(di = ModbusSequentialDataBlock.create())
#     store = ModbusSlaveContext()
#
# Finally, you are allowed to use the same DataBlock reference for every
# table or you may use a separate DataBlock for each table.
# This depends if you would like functions to be able to access and modify
# the same data or not::
#
#     block = ModbusSequentialDataBlock(0x00, [0]*0xff)
#     store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
#
# The server then makes use of a server context that allows the server to
# respond with different slave contexts for different unit ids. By default
# it will return the same context for every unit id supplied (broadcast
# mode).
# However, this can be overloaded by setting the single flag to False and
# then supplying a dictionary of unit id to context mapping::
#
#     slaves  = {
#         0x01: ModbusSlaveContext(...),
#         0x02: ModbusSlaveContext(...),
#         0x03: ModbusSlaveContext(...),
#     }
#     context = ModbusServerContext(slaves=slaves, single=False)
#
# The slave context can also be initialized in zero_mode which means that a
# request to address(0-7) will map to the address (0-7). The default is
# False which is based on section 4.4 of the specification, so address(0-7)
# will map to (1-8)::
#
#     store = ModbusSlaveContext(..., zero_mode=True)
# ----------------------------------------------------------------------- #
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*100),
    co=ModbusSequentialDataBlock(0, [0]*100),
    hr=ModbusSequentialDataBlock(0, [0]*100),
    ir=ModbusSequentialDataBlock(0, [0]*100))

context = ModbusServerContext(slaves=store, single=True)

# ----------------------------------------------------------------------- #
# initialize the server information
# ----------------------------------------------------------------------- #
# If you don't set this or any fields, they are defaulted to empty strings.
# ----------------------------------------------------------------------- #
identity = ModbusDeviceIdentification()
identity.VendorName = 'Pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
identity.ProductName = 'Pymodbus Server'
identity.ModelName = 'Pymodbus Server'
identity.MajorMinorRevision = '2.3.0'

# ----------------------------------------------------------------------- #
# run the server you want
# ----------------------------------------------------------------------- #
# Tcp:
StartTcpServer(context, identity=identity, address=('localhost', 502))

# TCP with different framer
# StartTcpServer(context, identity=identity,
#                framer=ModbusRtuFramer, address=("0.0.0.0", 5020))

# TLS
# StartTlsServer(context, identity=identity, certfile="server.crt",
#                keyfile="server.key", address=("0.0.0.0", 8020))

# Udp:
# StartUdpServer(context, identity=identity, address=("0.0.0.0", 5020))

# Ascii:
# StartSerialServer(context, identity=identity,
#                    port='/dev/ttyp0', timeout=1)

# RTU:
# StartSerialServer(context, framer=ModbusRtuFramer, identity=identity,
#                   port='/dev/ttyp0', timeout=.005, baudrate=9600)

# Binary
# StartSerialServer(context,
#                   identity=identity,
#                   framer=ModbusBinaryFramer,
#                   port='/dev/ttyp0',
#                   timeout=1)


        
    #     lb2_sh1 = tk.Label(sh1, text="Server Started Successfully", bg='#e0e0e0')
    #     lb2_sh1.grid(row=4, column=0, padx=10, pady=5)
        
    #     log_file('Server Started Running at IP:{0}, Port:{1} on {2}'\
    #              .format(sip_add_in,sport_no_in,datetime.datetime.now())
    #              )
                
    # except:
    #     log_file('Server failed to Start on {0}'\
    #              .format(datetime.datetime.now())
    #                      )
    #     messagebox.showwarning("Warning", "Server Failed to Start. Please try again")




# fr3_sh1 = tk.Frame(sh1, bg='#e0e0e0')
# fr3_sh1.grid(row=3, column=0, padx=10, pady=5)

# bt1_fr3 = tk.Button(fr3_sh1, 
#                  text="Start Server", 
#                  command=run_server, 
#                  width=15, 
#                  bg="#23ff89", 
#                  relief='raised'
#                  )
# bt1_fr3.grid(row=0, column=0, padx=20)

# bt2_fr4 = tk.Button(fr3_sh1,
#                     text="End Server",
#                     command=sh1.destroy,
#                     width=15,
#                     bg='#ffe082',
#                     relief='raised'
#                     )
# bt2_fr4.grid(row=0, column=1, padx=20)

# lb2_sh1 = tk.Label(sh1, text=" ", bg='#e0e0e0')
# lb2_sh1.grid(row=4, column=0, padx=10, pady=5)

# lb3_sh1 = tk.Label(sh1,
#                    text='Version V20.1         copyright@2020 BHEL',
#                    bd=1,
#                    bg='#e0e0e0',
#                    fg='grey50',
#                    padx=10
#                    )
# lb3_sh1.grid(row=10, column=0, sticky='e')

# sh1.mainloop()