#!/usr/bin/env python3

import os
import re
import subprocess
import sys
from functools import cmp_to_key

def open_settings(path: str):
    with open(path, "r", encoding="UTF-8") as file: 
        return file.readlines()


def get_hwmon_location():
    base_path = "/sys/devices/platform/coretemp.0/hwmon"
    hwmon_dirs = os.listdir(base_path)
    assert len(hwmon_dirs) == 1
    hwmon_dir = f"{base_path}/{hwmon_dirs[0]}"
    return [f"hwmon {hwmon_dir}/{x}\n" for x in os.listdir(hwmon_dir) if os.path.isfile(f"{hwmon_dir}/{x}") and re.match("temp[0-9]+_input", x)]


def update_settings(current, new):
    config = [x for x in current if(not x.startswith("hwmon"))] + new
    return sorted(config, key=cmp_to_key(lambda i1, i2: line_fitness(i1) - line_fitness(i2)))

def line_fitness(line: str):
    if line.startswith("tp_fan"):
        return 1
    elif line.startswith("hwmon"):
        return 3
    elif(line.startswith("(")):
        return 5
    else:
        return 4

def are_same(current, new):
    cur = set([x.strip() for x in current if x.startswith("hwmon")])
    ne = set([x.strip() for x in new if x.startswith("hwmon")])
    return cur.issubset(ne) and cur.issuperset(ne)

def save_settings(current, new):
    updated_config = "".join(update_settings(current, new))
    print(f"Updating config!\n{updated_config}")
    write_settings(config_path, updated_config)

def write_settings(path: str, payload: str):
    with open(path, "w", encoding="UTF-8") as file:
        file.write(payload)

def restart_thinkfan():
    process = subprocess.Popen("systemctl restart thinkfan.service".split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    if(error):
        print(f"Error ocurred during the thinkfan restart!\n{error}")
    else:
        print("Service was restarted successfully, everything set.")

if __name__ == "__main__":

    config_path = "/etc/thinkfan.conf"
    current = open_settings(config_path)
    new = get_hwmon_location()

    if(are_same(current, new)):
        print("All set! No change detected.")
    else:
        save_settings(current, new)
        restart_thinkfan()
