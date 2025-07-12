import datetime
import struct

# 0 	Year
# 1 	Year
# 2 	Month
# 3 	Day
# 4 	Hours
# 5 	Minutes
# 6 	Seconds
# 7 	Day of Week (0 = unknown)
# 8 	Fractions256 (0 = uknown)
# 9 	Adjust Reason (0x03 = Manual Update => External Reference => No Time Zone Change => No DST Change)

def get_time_update_cmd() -> bytes:
    format_str = '<hBBBBBBBB' 
    current = datetime.datetime.now()

    payload = struct.pack(format_str, 
        current.year,
        current.month,
        current.day,
        current.hour,
        current.minute,
        current.second,
        0,
        0,
        3)

    return payload