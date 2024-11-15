#!/usr/bin/python

from pymodbus.client import ModbusTcpClient


MB_SERVER = '<LAMBDA_IP>'
PORT = 502

LAMBDA_REGISTERS = {
    'ambient_error_number': (0, 1, 1),
    'ambient_operating_state': (1, 1, 1),
    'ambient_actual_ambient_temp': (2, 1, 0.1),
    'ambient_average_ambient_temp_1h': (3, 1, 0.1),
    'ambient_calculated_ambient_temp': (4, 1, 0.1),

    'emanager_error_number': (100, 1, 1),
    'emanager_operating_state': (101, 1, 1),
    'emanager_actual_power': (102, 1, 1),
    'emanager_actual_power_consumption': (103, 1, 1),
    'emanager_power_consumption_setpoint': (104, 1, 1),

    'heat_pump_hp_error_state': (1000, 1, 1),
    'heat_pump_hp_error_number': (1001, 1, 1),
    'heat_pump_hp_state': (1002, 1, 1),
    'heat_pump_operating_state': (1003, 1, 1),
    'heat_pump_t_flow': (1004, 1, 0.01),
    'heat_pump_t_return': (1005, 1, 0.01),
    'heat_pump_vol_sink': (1006, 1, 0.01),
    'heat_pump_t_eqin': (1007, 1, 0.01),
    'heat_pump_t_eqout': (1008, 1, 0.01),
    'heat_pump_vol_source': (1009, 1, 0.01),
    'heat_pump_compressor_rating': (1010, 1, 0.01),
    'heat_pump_qp_heating': (1011, 1, 0.1),
    'heat_pump_fi_power_consumption': (1012, 1, 1),
    'heat_pump_cop': (1013, 1, 0.01),
    'heat_pump_modbus_request_release_password': (1014, 1, 1),
    'heat_pump_request_type': (1015, 1, 1),
    'heat_pump_request_flow_line_temp': (1016, 1, 0.1),
    'heat_pump_request_return_line_temp': (1017, 1, 0.1),
    'heat_pump_request_heat_sink_temp_diff': (1018, 1, 0.1),
    'heat_pump_relais_state_for_2nd_heating_stage': (1019, 1, 1),
    'heat_pump_statistic_vda_e_since_last_reset': (1020, 2, 1),
    'heat_pump_statistic_vda_q_since_last_reset': (1022, 2, 1),
    'heat_pump_set_error_quitt': (1050, 1, 1),

    'boiler_error_number': (2000, 1, 1),
    'boiler_operating_state': (2001, 1, 1),
    'boiler_actual_high_temp': (2002, 1, 0.1),
    'boiler_actual_low_temp': (2003, 1, 0.1),
    'boiler_set_maximum_buffer_temp': (2050, 1, 0.1),

    'buffer_error_number': (3000, 1, 1),
    'buffer_operating_state': (3001, 1, 1),
    'buffer_actual_high_temp': (3002, 1, 0.1),
    'buffer_actual_low_temp': (3003, 1, 0.1),
    'buffer_set_maximum_buffer_temp': (3050, 1, 0.1),

    'heating_error_number': (5000, 1, 1),
    'heating_operating_state': (5001, 1, 1),
    'heating_flow_line_temp': (5002, 1, 0.1),
    'heating_return_line_temp': (5003, 1, 0.1),
    'heating_room_device_temp': (5004, 1, 0.1),
    'heating_setpoint_flow_line_temp': (5005, 1, 0.1),
    'heating_operating_mode': (5006, 1, 1),
    'heating_set_offset_flow_line_temp_setpoint': (5050, 1, 0.1),
    'heating_set_setpoint_room_heating_temp': (5051, 1, 0.1),
    'heating_set_setpoint_room_cooling_temp': (5052, 1, 0.1),
}

LAMBDA_EVAL = {
    'ambient_operating_state': {
        0: 'OFF',
        1: 'AUTOMATIK',
        2: 'MANUAL',
        3: 'ERROR',
    },
    'emanager_operating_state': {
        0: 'OFF',
        1: 'AUTOMATIK',
        2: 'MANUAL',
        3: 'ERROR',
        4: 'OFFLINE',
    },
    'heat_pump_hp_error_state': {
        0: 'NONE',
        1: 'MESSAGE',
        2: 'WARNING',
        3: 'ALARM',
        4: 'FAULT',
    },
    'heat_pump_hp_state': {
        0: 'INIT',
        1: 'REFERENCE',
        2: 'RESTART-BLOCK',
        3: 'READY',
        4: 'START PUMPS',
        5: 'START COMPRESSOR',
        6: 'PRE-REGULATION',
        7: 'REGULATION',
        8: 'Not Used',
        9: 'COOLING',
        10: 'DEFROSTING',
        20: 'STOPPING',
        30: 'FAULT-LOCK',
        31: 'ALARM-BLOCK',
        40: 'ERROR-RESET',
    },
    'heat_pump_operating_state': {
        0: 'STBY',
        1: 'CH',
        2: 'DHW',
        3: 'CC',
        4: 'CIRCULATE',
        5: 'DEFROST',
        6: 'OFF',
        7: 'FROST',
        8: 'STBY-FROST',
        9: 'Not',
        10: 'SUMMER',
        11: 'HOLIDAY',
        12: 'ERROR',
        13: 'WARNING',
        14: 'INFO-MESSAGE',
        15: 'TIME-BLOCK',
        16: 'RELEASE-BLOCK',
        17: 'MINTEMP-BLOCK',
        18: 'FIRMWARE-DOWNLOAD',
    },
    'heat_pump_request_type': {
        0: 'NO REQUEST ',
        1: 'FLOW PUMP CIRCULATION',
        2: 'CENTRAL HEATING',
        3: 'CENTRAL COOLING',
        4: 'DOMESTIC HOT WATER',
    },
    'boiler_operating_state': {
        0: 'STBY',
        1: 'DHW',
        2: 'LEGIO',
        3: 'SUMMER',
        4: 'FROST',
        5: 'HOLIDAY',
        6: 'PRIO-STOP',
        7: 'ERROR',
        8: 'OFF',
        9: 'PROMPT-DHW',
        10: 'TRAILING-STOP',
        11: 'TEMP-LOCK',
        12: 'STBY-FROST',
    },
    'buffer_operating_state': {
        0: 'STBY',
        1: 'HEATING',
        2: 'COOLING',
        3: 'SUMMER',
        4: 'FROST',
        5: 'HOLIDAY',
        6: 'PRIO-STOP',
        7: 'ERROR',
        8: 'OFF',
        9: 'STBY-FROST',
    },
    'heating_operating_state': {
        0: 'HEATING',
        1: 'ECO',
        2: 'COOLING',
        3: 'FLOORDRY',
        4: 'FROST',
        5: 'MAX-TEMP',
        6: 'ERROR',
        7: 'SERVICE',
        8: 'HOLIDAY',
        9: 'CH-SUMMER',
        10: 'CC-WINTER',
        11: 'PRIO-STOP',
        12: 'OFF',
        13: 'RELEASE-OFF',
        14: 'TIME-OFF',
        15: 'STBY',
        16: 'STBY-HEATING',
        17: 'STBY-ECO',
        18: 'STBY-COOLING',
        19: 'STBY-FROST',
        20: 'STBY-FLOORDRY',
    },
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


def main():
    client = ModbusClient()

    data = {}
    for name, address_value in LAMBDA_REGISTERS.items():
        value = client.GetRegister(address_value)
        if name in LAMBDA_EVAL.keys():
            value = LAMBDA_EVAL[name][value]
        data[name] = value

    print(data)


if __name__ == '__main__':
    main()
