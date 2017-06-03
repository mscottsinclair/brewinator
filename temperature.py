import RPi.GPIO as GPIO
import os
import glob
import time

GPIO.cleanup(16)
GPIO.setmode(GPIO.BOARD) ## This is the pin number of the board not the ID printed on the Cobbler
GPIO.setup(16, GPIO.OUT) ## Set PIN 16 as output to control the HLT SSRs

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

mltProbeId = '28-000008e10b35'  ## Set ID of MLT temp probe
hltProbeId = '28-000008e137df'  ## Set ID of HLT temp probe

base_dir = '/sys/bus/w1/devices/'
## device_folder = glob.glob(base_dir + '28*')[0]
## print("Device Folder = " + device_folder)
## device_file = device_folder + '/w1_slave'
mltFile = base_dir + mltProbeId + '/w1_slave'
hltFile = base_dir + hltProbeId + '/w1_slave'
## print("Device File = " + device_file)

def read_mlt_temp_raw():
    f=open(mltFile, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_hlt_temp_raw():
    f=open(hltFile, 'r')
    lines = f.readlines()
    f.close()
    return lines

##def read_temp_raw():
##    f=open(device_file, 'r')
##    lines = f.readlines()
##    f.close()
##    return lines

def read_mlt_temp():
    lines = read_mlt_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_mlt_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 /5.0 + 32.0
        return temp_f

def read_hlt_temp():
    lines = read_hlt_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_hlt_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 /5.0 + 32.0
        if temp_f < 80:
            print("Turning on the heat!")
            GPIO.output(16, True)
        elif temp_f > 90:
            print("Turning off the heat!")
            GPIO.output(16, False)
        else:
            GPIO.output(16, False)
        return temp_f

while True:
    try:
        print("MLT Temp is:")
        print(read_mlt_temp())
        print("HLT Temp is:")
        print(read_hlt_temp())
        time.sleep(1)
    except KeyboardInterrupt:
        GPIO.output(16, False)
        GPIO.cleanup(16)
        
