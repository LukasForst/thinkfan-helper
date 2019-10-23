## About

This utility solves problems on some kernels when `hwmon` resources are not in the fixed path 
and they can be changed during the reboot.
For that reason, it is sometimes not possible to correctly configure [thinkfan](https://github.com/vmatare/thinkfan)
 since it requires specifying the correct folders where the `hwmon` is located.

This script should be executed after the boot, when the `hwmon` is set and it scans the folder
 `/sys/devices/platform/coretemp.0/hwmon` for `hwmon` folder and then update thinkfan configuration
  located at `/etc/thinkfan.conf` accordingly.
If the configuration changed, script restarts the thinfan service.

## Predisposition

* Python (obviously) > 3.6
* Thinkfan config located in `/etc/thinkfan.conf`
    * also, the script has to have rights to edit the file -> therefore run it as root OR as a user that can write 
    to the file (this is preferred)
