#!/usr/bin/env python

import serial
import os
import subprocess
import signal
import datetime

ser = serial.Serial("/dev/cu.SLAB_USBtoUART", 921600)

filename = "capture_%s.pcap" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

print("Creating capture file: %s" % filename)
f = open(filename, 'wb')

print("Starting Wireshark")
cmd = "tail -f -c +0 " + filename + " | wireshark -k -i -"
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

def write_hex(f, hex_string):
    #print("Writing: "+hex_string)
    f.write(bytes.fromhex(hex_string))
    f.flush()

# PCAP file header
header = 'd4c3b2a1' + '0200' + '0400' + '00000000' + '00000000' + 'c4090000' + '69000000'
write_hex(f, header)

print("Waiting for packets...")
try:
    while True:
        line = ser.readline()
        line = line.decode().strip()
        if line.startswith("DATA:"):
            data = line[5:]
            write_hex(f, data)
        else:
            print(line)

except KeyboardInterrupt:
    print("Stopping Wireshark...")
    os.killpg(os.getpgid(p.pid), signal.SIGTERM)

f.close()
ser.close()
print("Done")
