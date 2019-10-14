import os
import re
from functools import cmp_to_key

def write_settings(path: str, payload: str):
    with open(path, "w", encoding="UTF-8") as file:
        file.write(payload)

def open_settings(path: str):
    with open(path, "r", encoding="UTF-8") as file: 
        return file.readlines()

def __fittness__(line: str):
    if line.startswith("tp_fan"):
        return 1
    elif line.startswith("hwmon"):
        return 3
    elif(line.startswith("(")):
        return 5
    else:
        return 4

def update_settings(current, new):
    config = [x for x in current if(not x.startswith("hwmon"))] + new
    return sorted(config, key=cmp_to_key(lambda i1, i2: __fittness__(i1) - __fittness__(i2)))

def get_sensors():
    base_path = "/sys/devices/platform/coretemp.0/hwmon"
    hwmon_dirs = os.listdir(base_path)
    assert len(hwmon_dirs) == 1
    hwmon_dir = f"{base_path}/{hwmon_dirs[0]}"
    return [f"hwmon {hwmon_dir}/{x}\n" for x in os.listdir(hwmon_dir) if os.path.isfile(f"{hwmon_dir}/{x}") and re.match("temp[0-9]+_input", x)]

if __name__ == "__main__":
    config_path = "/etc/thinkfan.conf"
    current = open_settings(config_path)
    new = get_sensors()
    updated_config = "".join(update_settings(current, new))
    print(updated_config)
    write_settings(config_path, updated_config)