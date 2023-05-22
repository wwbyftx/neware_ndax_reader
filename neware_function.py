
# multi = struct.unpack("i",byte3[94:98])  #4
# [Y, M, D, h, m, s] = struct.unpack('<HBBBBB', byte3[87:94]) # OK 7
# [Charge_energy, DChgEnergy] = struct.unpack('<qq', byte3[71:87]) # OK 16
# [ChgCap,DChgCap] = struct.unpack('<q', byte3[63:71]) # OK 16
# [Voltage,current] = struct.unpack('<i', byte3[43:51]) # OK
# [time] = struct.unpack('Q', byte3[35:43]) # OK
# [Index, Cycle] = struct.unpack('<IB', byte3[24:29]) #OK
# [Range] = struct.unpack('i',byte3[0:4]) #OK
import struct
from datetime import datetime


def byte_to_list(bytes):
    [Index] = struct.unpack('<I', bytes[8:12])
    [Cycle] = struct.unpack('<I', bytes[12:16])
    [Step] = struct.unpack('<B', bytes[16:17])
    [Status] = struct.unpack('<B', bytes[17:18])
    [time] = struct.unpack('Q', bytes[23:31])
    [Voltage, Current] = struct.unpack('<ii', bytes[31:39])
    [Charge_capacity, Discharge_capacity] = struct.unpack('<qq', bytes[43:59])
    [Charge_energy, Discharge_energy] = struct.unpack('<qq', bytes[59:75])
    [Y, M, D, h, m, s] = struct.unpack('<HBBBBB', bytes[75:82])
    [Range] = struct.unpack("i", bytes[82:86])







    state_dict = {
        1: 'CC_Chg',
        2: 'CC_DChg',
        3: 'Rest',
        4: 'Rest',
        5: '5',
        6:'6',
        7: 'CCCV_Chg',
        8: 'Cp_Dchg',
        9:'Cp_Chg',
        10: '10',
        11:'11',
        12:'12',
        13: '13',
        15:'15',
        16:'16',
        17: '17',
        18:'18',
        19: '19',
        20: '20',
        21:'21',
    }
    multiplier_dict = {
        -300000: 1e-2,
        -200000: 1e-2,
        -100000: 1e-2,
        -60000: 1e-2,
        -30000: 1e-2,
        -50000: 1e-2,
        -20000: 1e-2,
        -12000: 1e-2,
        -10000: 1e-2,
        -6000: 1e-2,
        -5000: 1e-2,
        -3000: 1e-2,
        -1000: 1e-2,
        -500: 1e-3,
        -100: 1e-3,
        0: 0,
        10: 1e-3,
        100: 1e-2,
        200: 1e-2,
        1000: 1e-1,
        6000: 1e-1,
        12000: 1e-1,
        50000: 1e-1,
        60000: 1e-1,
    }
    Date = datetime(Y, M, D, h, m, s)
    multiplier = multiplier_dict[Range]
    list = [
        Index,
        Cycle + 1,
        Step,
        state_dict[Status],
        time/1000,
        Voltage/10000,
        Current*multiplier/1000,
        Charge_capacity*multiplier/3600000,
        Discharge_capacity*multiplier/3600000,
        Charge_energy*multiplier/3600000,
        Discharge_energy*multiplier/3600000,
        Date
    ]
    return list



def aux_to_list(bytes):
    [temperature] = struct.unpack('<h', bytes[41:43])
    [Index] = struct.unpack('<I', bytes[8:12])
    #[Cycle] = struct.unpack('<I', bytes[12:16])

    list = [
        Index,
        temperature/10
    ]
    return list
