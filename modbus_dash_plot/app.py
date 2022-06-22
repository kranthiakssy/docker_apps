import numpy as np
import pandas as pd
import datetime
import time
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
import os
import sys

param = {'ServerIP':'192.168.139.202',
            'PortNo':502,
            'PVreg':0,
            'SPreg':2,
            'CVPosreg':6}
# Client conncetion
client = ModbusTcpClient(host=param['ServerIP'],
                            port=param['PortNo']
                            )

if client.connect():
    print('Connection Established Succesfully.')
    print('Connection Established with host:{0} on port:{1}'\
                .format(param['ServerIP'],param['PortNo'])
                        )
# reading initial float data
data_init = [0,0,0,0,'False']
result_pv0  = client.read_holding_registers(int(param['PVreg']), 2)
decoder_pv0 = BinaryPayloadDecoder.fromRegisters(result_pv0.registers, 
                                                byteorder=Endian.Big, 
                                                wordorder=Endian.Big
                                                )
data_init[0] = decoder_pv0.decode_32bit_float()


result_sp0  = client.read_holding_registers(int(param['SPreg']), 2)
decoder_sp0 = BinaryPayloadDecoder.fromRegisters(result_sp0.registers, 
                                                byteorder=Endian.Big, 
                                                wordorder=Endian.Big
                                                )
data_init[1] = decoder_sp0.decode_32bit_float()

# result_cvp0  = client.read_holding_registers(int(param['CVPosreg']), 2)
# decoder_cvp0 = BinaryPayloadDecoder.fromRegisters(result_cvp0.registers, 
#                                                 byteorder=Endian.Big, 
#                                                 wordorder=Endian.Little
#                                                 )
# data_init[2] = decoder_cvp0.decode_32bit_float()

# result_cvd0  = client.read_holding_registers(int(param['CVDmdreg']), 2)
# decoder_cvd0 = BinaryPayloadDecoder.fromRegisters(result_cvd0.registers, 
#                                                 byteorder=Endian.Big, 
#                                                 wordorder=Endian.Little
#                                                 )
# data_init[3] = decoder_cvd0.decode_32bit_float()

# result_cvdist0 = client.read_coils(int(param['CVPerturbreg']),1)            
# data_init[4] = result_cvdist0.bits[0]
print('Data collected: ',data_init)