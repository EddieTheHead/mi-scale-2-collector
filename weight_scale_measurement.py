from dataclasses import dataclass
import logging 
import datetime

@dataclass
class ScaleMeasurement:
    weight: float
    unit: str
    time: int
    stabilized: bool

def parse_weight_measurement_message(buffer: bytearray) -> ScaleMeasurement:
    flags = buffer[0]
    units_bit = bool(flags & 0b0000_0001)
    has_timestamp = bool(flags & 0b0000_0010)
    is_stabilized = bool(flags & 0b0010_0000)

    unit = 'lbs' if units_bit else 'kg'
    
    weight_raw = (buffer[2] << 8) | buffer[1]
    if unit == 'kg':
        resolution = 0.005
    else:
        resolution = 0.01

    weight = weight_raw * resolution
    if has_timestamp:
        year = (buffer[4] << 8) | (buffer[3])
        month = buffer[5]
        day = buffer[6]
        hour = buffer[7]
        minute = buffer[8]
        second = buffer[9]

        timestamp = datetime.datetime(year, month, day, hour, minute, second)
    else:
        timestamp = None

    return ScaleMeasurement(weight=weight, unit=unit, time=timestamp, stabilized=is_stabilized)