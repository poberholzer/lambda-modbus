#!/usr/bin/python

import datetime
import json
import urllib
import urllib.parse
import urllib.request

from pymodbus.client import ModbusTcpClient

MB_SERVER = 'LAMBDA_IP_ADDRESS'
PORT = 502

API_URL = 'https://<MY_SERVER/home/thermostat'
'''
API_URL response JSON
{
  "timestamp": 1731058205,
  "thermostats": {
    "ROOM_NAME": [GPIO_NUMBER_RASPBERRY_PI],
    ...
  },
  "current_temps": {
    "ROOM_NAME": [<TEMP>, <HUMID>],
    ...
  },
  "in_time": true/false,
  "in_time_start": true/false,
  "30min_diffs": {
    "ROOM_NAME": <temp diff last 30min>,
    ...
  }
}
'''
TARGET_URL = 'https://thermostat.<MY_SERVER>/targets'
'''
TARGET_URL response JSON
[
  { "Id": 32, "RoomName": "ROOM_NAME", "Temp": <temp> },
  ...
]
'''

ROOMS = ['Wohnzimmer', 'Esszimmer']
ROOM_TEMP = 'Wohnzimmer'

REGISTERS = {
    'heating_room_device_temp': (5004, 1, 0.1),
    'heating_operating_mode': (5006, 1, 1),
}

EVAL = {
    'heating_operating_mode': {
        0: 'OFF(RW)',
        1: 'MANUAL(R)',
        2: 'AUTOMATIK(RW)',
        3: 'AUTO-HEATING(RW)',
        4: 'AUTO-COOLING(RW)',
        5: 'FROST(RW)',
        6: 'SUMMER(RW)',
        7: 'FLOOR-DRY(R)',
    },
}

OFF = 5
ON = 2
DIFF = 0.3


def GetLambdaTarget():
    values = json.loads(urllib.request.urlopen(TARGET_URL).read())
    for v in values:
        if v['RoomName'] == 'Lambda':
            return v['Temp']


class ModbusClient(object):

    def __init__(self, server=MB_SERVER, port=PORT):
        self.client = ModbusTcpClient(server, port)
        self.client.connect()

    def GetRegister(self, address_value):
        address, size, multiplicator = address_value
        response = self.client.read_holding_registers(address, size, slave=1)
        r = response.registers
        value = r
        if size == 1:
            value = r[0] * multiplicator
        elif size == 2:
            value = ((r[0] * 2**16) + r[1]) * multiplicator
        return round(value, 3)

    def WriteRegister(self, address, value):
        return self.client.write_registers(address, value, slave=1)

    def GetHeatingMode(self):
        return self.GetRegister(REGISTERS['heating_operating_mode'])

    def SetHeatingMode(self, mode):
        if mode == OFF:
            print('OFF')
        if mode == ON:
            print('ON')
        return self.WriteRegister(REGISTERS['heating_operating_mode'][0], mode)

    def WriteRoomTemp(self, temp):
        return self.WriteRegister(REGISTERS['heating_room_device_temp'][0], temp)


def main():
    print('.'*50)
    print(datetime.datetime.now().isoformat())
    modbus = ModbusClient()
    values = json.loads(urllib.request.urlopen(API_URL).read())
    in_time = values['in_time']
    target_temp = GetLambdaTarget()
    status = modbus.GetHeatingMode()

    temps = []
    diffs = []
    for r, t in values['current_temps'].items():
        if r not in ROOMS:
            continue
        if r == ROOM_TEMP:
            modbus.WriteRoomTemp(int(t[0] * 10))
        temps.append(t[0])
        diffs.append(values['30min_diffs'][r])
    current_temp = min(temps)
    diff = max(diffs)
    print('In Time: ', in_time)
    print('Target temp: ', target_temp)
    print('Current min temp: ', current_temp)
    print('30min diff: ', diff)
    mode = 'OFF'
    if status == ON:
        mode = 'ON'
    print('Current Heating Mode: ', mode)

    if not in_time:
        modbus.SetHeatingMode(OFF)
    elif current_temp >= target_temp:
        modbus.SetHeatingMode(OFF)
    elif diff <= DIFF and current_temp + DIFF <= target_temp:
        modbus.SetHeatingMode(ON)


if __name__ == '__main__':
    main()
