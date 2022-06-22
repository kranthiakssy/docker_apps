from email.policy import strict
from pymodbus.client.sync import ModbusTcpClient
import logging
import time
# from pymodbus.constants import Defaults
# Defaults.RetryOnEmpty = True


client = ModbusTcpClient('192.168.136.202',502)
if client.connect():
    print('Connection Established Succesfully.')
client.write_coil(1, True)
# client.write_coil(3, False)
for i in range(0,10):
    try:
        result = client.read_coils(1,1)
        print('result:',result) # .bits[0]
    except:
        print("failed attempt: ",i)
    time.sleep(10)



client.close()