
from multiprocessing import Process, Pipe, Queue, current_process
# from queue import Full
# from subprocess import Popen, PIPE, call
# from datetime import datetime
import time, random, os
# # from smbus import SMBus
# # import RPi.GPIO as GPIO
# from pid import pidpy as PIDController
import xml.etree.ElementTree as ET
# from flask import Flask, render_template, request, jsonify

import Temp1Wire
import Display

# global parent_conn, parent_connB, parent_connC, statusQ, statusQ_B, statusQ_C
# global xml_root, template_name, pinHeatList, pinGPIOList
# global brewtime, oneWireDir

# app = Flask(__name__, template_folder='templates')
# #url_for('static', filename='raspibrew.css')

# #Parameters that are used in the temperature control process
# class param:
#     status = {
#         "numTempSensors" : 0,
#         "temp" : "0",
#         "tempUnits" : "F",
#         "elapsed" : "0",
#         "mode" : "off",
#         "cycle_time" : 2.0,
#         "duty_cycle" : 0.0,
#         "boil_duty_cycle" : 60,
#         "set_point" : 0.0,
#         "boil_manage_temp" : 200,
#         "num_pnts_smooth" : 5,
#         "k_param" : 44,
#         "i_param" : 165,
#         "d_param" : 4             
#     }
                      
# # main web page    
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'GET':
#         #render main page
#         return render_template(template_name, mode = param.status["mode"], set_point = param.status["set_point"], \
#                                duty_cycle = param.status["duty_cycle"], cycle_time = param.status["cycle_time"], \
#                                k_param = param.status["k_param"], i_param = param.status["i_param"], \
#                                d_param = param.status["d_param"])
        
#     else: #request.method == 'POST' (first temp sensor / backwards compatibility)
#         # get command from web browser or Android   
#         #print request.form
#         param.status["mode"] = request.form["mode"] 
#         param.status["set_point"] = float(request.form["setpoint"])
#         param.status["duty_cycle"] = float(request.form["dutycycle"]) #is boil duty cycle if mode == "boil"
#         param.status["cycle_time"] = float(request.form["cycletime"])
#         param.status["boil_manage_temp"] = float(request.form.get("boilManageTemp", param.status["boil_manage_temp"])) 
#         param.status["num_pnts_smooth"] = int(request.form.get("numPntsSmooth", param.status["num_pnts_smooth"])) 
#         param.status["k_param"] = float(request.form["k"])
#         param.status["i_param"] = float(request.form["i"])
#         param.status["d_param"] = float(request.form["d"])
                
#         #send to main temp control process 
#         #if did not receive variable key value in POST, the param class default is used
#         parent_conn.send(param.status)  
        
#         return 'OK'

# #post params (selectable temp sensor number)    
# @app.route('/postparams/<sensorNum>', methods=['POST'])
# def postparams(sensorNum=None):
    
#     param.status["mode"] = request.form["mode"] 
#     param.status["set_point"] = float(request.form["setpoint"])
#     param.status["duty_cycle"] = float(request.form["dutycycle"]) #is boil duty cycle if mode == "boil"
#     param.status["cycle_time"] = float(request.form["cycletime"])
#     param.status["boil_manage_temp"] = float(request.form.get("boilManageTemp", param.status["boil_manage_temp"])) 
#     param.status["num_pnts_smooth"] = int(request.form.get("numPntsSmooth", param.status["num_pnts_smooth"]))
#     param.status["k_param"] = float(request.form["k"])
#     param.status["i_param"] = float(request.form["i"])
#     param.status["d_param"] = float(request.form["d"])
            
#     #send to main temp control process 
#     #if did not receive variable key value in POST, the param class default is used
#     if sensorNum == "1":
#         print("got post to temp sensor 1")
#         parent_conn.send(param.status)
#     elif sensorNum == "2":
#         print("got post to temp sensor 2")
#         if len(pinHeatList) >= 2:
#             parent_connB.send(param.status)
#         else:
#             param.status["mode"] = "No Temp Control"
#             param.status["set_point"] = 0.0
#             param.status["duty_cycle"] = 0.0 
#             parent_connB.send(param.status)
#             print("no heat GPIO pin assigned")
#     elif sensorNum == "3":
#         print("got post to temp sensor 3")
#         if len(pinHeatList) >= 3:
#             parent_connC.send(param.status)
#         else:
#             param.status["mode"] = "No Temp Control"
#             param.status["set_point"] = 0.0
#             param.status["duty_cycle"] = 0.0 
#             parent_connC.send(param.status)
#             print("no heat GPIO pin assigned")
#     else:
#         print("Sensor doesn't exist (POST)")
        
#     return 'OK'

# #post GPIO     
# @app.route('/GPIO_Toggle/<GPIO_Num>/<onoff>', methods=['GET'])
# def GPIO_Toggle(GPIO_Num=None, onoff=None):
    
#     if len(pinGPIOList) >= int(GPIO_Num):
#         out = {"pin" : pinGPIOList[int(GPIO_Num)-1], "status" : "off"}
#         if onoff == "on":
#             GPIO.output(pinGPIOList[int(GPIO_Num)-1], ON)
#             out["status"] = "on"
#             print("GPIO Pin #%s is toggled on" % pinGPIOList[int(GPIO_Num)-1])
#         else: #off
#             GPIO.output(pinGPIOList[int(GPIO_Num)-1], OFF)
#             print("GPIO Pin #%s is toggled off" % pinGPIOList[int(GPIO_Num)-1])
#     else:
#         out = {"pin" : 0, "status" : "off"}
        
#     return jsonify(**out)
    
# #get status from RasPiBrew using firefox web browser (first temp sensor / backwards compatibility)
# @app.route('/getstatus') #only GET
# def getstatusB():          
#     #blocking receive - current status    
#     param.status = statusQ.get()        
#     return jsonify(**param.status)

# #get status from RasPiBrew using firefox web browser (selectable temp sensor)
# @app.route('/getstatus/<sensorNum>') #only GET
# def getstatus(sensorNum=None):          
#     #blocking receive - current status
#     if sensorNum == "1":
#         param.status = statusQ.get()
#     elif sensorNum == "2":
#         param.status = statusQ_B.get()
#     elif sensorNum == "3":
#         param.status = statusQ_C.get()
#     else:
#         print("Sensor doesn't exist (GET)")
#         param.status["temp"] = "-999"
        
#     return jsonify(**param.status)

# def getbrewtime():
#     return (time.time() - brewtime)    
       
# # Stand Alone Get Temperature Process               
# def gettempProc(conn, myTempSensor):
#     p = current_process()
#     print('Starting:', p.name, p.pid)
    
#     while (True):
#         t = time.time()
#         time.sleep(.5) #.1+~.83 = ~1.33 seconds
#         num = myTempSensor.readTempC()
#         elapsed = "%.2f" % (time.time() - t)
#         conn.send([num, myTempSensor.sensorNum, elapsed])
        
# #Get time heating element is on and off during a set cycle time
# def getonofftime(cycle_time, duty_cycle):
#     duty = duty_cycle/100.0
#     on_time = cycle_time*(duty)
#     off_time = cycle_time*(1.0-duty)   
#     return [on_time, off_time]
        
# # Stand Alone Heat Process using I2C (optional)
# def heatProcI2C(cycle_time, duty_cycle, conn):
#     p = current_process()
#     print('Starting:', p.name, p.pid)
#     bus = SMBus(0)
#     bus.write_byte_data(0x26,0x00,0x00) #set I/0 to write
#     while (True):
#         while (conn.poll()): #get last
#             cycle_time, duty_cycle = conn.recv()
#         conn.send([cycle_time, duty_cycle])  
#         if duty_cycle == 0:
#             bus.write_byte_data(0x26,0x09,0x00)
#             time.sleep(cycle_time)
#         elif duty_cycle == 100:
#             bus.write_byte_data(0x26,0x09,0x01)
#             time.sleep(cycle_time)
#         else:
#             on_time, off_time = getonofftime(cycle_time, duty_cycle)
#             bus.write_byte_data(0x26,0x09,0x01)
#             time.sleep(on_time)
#             bus.write_byte_data(0x26,0x09,0x00)
#             time.sleep(off_time)

# # Stand Alone Heat Process using GPIO
# def heatProcGPIO(cycle_time, duty_cycle, pinNum, conn):
#     p = current_process()
#     print('Starting:', p.name, p.pid)
#     if pinNum > 0:
#         GPIO.setup(pinNum, GPIO.OUT)
#         while (True):
#             while (conn.poll()): #get last
#                 cycle_time, duty_cycle = conn.recv()
#             conn.send([cycle_time, duty_cycle])  
#             if duty_cycle == 0:
#                 GPIO.output(pinNum, OFF)
#                 time.sleep(cycle_time)
#             elif duty_cycle == 100:
#                 GPIO.output(pinNum, ON)
#                 time.sleep(cycle_time)
#             else:
#                 on_time, off_time = getonofftime(cycle_time, duty_cycle)
#                 GPIO.output(pinNum, ON)
#                 time.sleep(on_time)
#                 GPIO.output(pinNum, OFF)
#                 time.sleep(off_time)

# def unPackParamInitAndPost(paramStatus):
#     #temp = paramStatus["temp"]
#     #tempUnits = paramStatus["tempUnits"]
#     #elapsed = paramStatus["elapsed"]
#     mode = paramStatus["mode"]
#     cycle_time = paramStatus["cycle_time"]
#     duty_cycle = paramStatus["duty_cycle"]
#     boil_duty_cycle = paramStatus["boil_duty_cycle"] 
#     set_point = paramStatus["set_point"] 
#     boil_manage_temp = paramStatus["boil_manage_temp"]
#     num_pnts_smooth = paramStatus["num_pnts_smooth"]
#     k_param = paramStatus["k_param"]
#     i_param = paramStatus["i_param"] 
#     d_param = paramStatus["d_param"] 
    
#     return mode, cycle_time, duty_cycle, boil_duty_cycle, set_point, boil_manage_temp, num_pnts_smooth, \
#            k_param, i_param, d_param
           
# def packParamGet(numTempSensors, myTempSensorNum, temp, tempUnits, elapsed, mode, cycle_time, duty_cycle, boil_duty_cycle, set_point, \
#                                  boil_manage_temp, num_pnts_smooth, k_param, i_param, d_param):
    
#     param.status["numTempSensors"] = numTempSensors
#     param.status["myTempSensorNum"] = myTempSensorNum
#     param.status["temp"] = temp
#     param.status["tempUnits"] = tempUnits
#     param.status["elapsed"] = elapsed
#     param.status["mode"] = mode
#     param.status["cycle_time"] = cycle_time
#     param.status["duty_cycle"] = duty_cycle
#     param.status["boil_duty_cycle"] = boil_duty_cycle
#     param.status["set_point"] = set_point
#     param.status["boil_manage_temp"] = boil_manage_temp
#     param.status["num_pnts_smooth"] = num_pnts_smooth
#     param.status["k_param"] = k_param
#     param.status["i_param"] = i_param
#     param.status["d_param"] = d_param

#     return param.status
        
# # Main Temperature Control Process
# def tempControlProc(myTempSensor, display, pinNum, readOnly, paramStatus, statusQ, conn):
    
#         mode, cycle_time, duty_cycle, boil_duty_cycle, set_point, boil_manage_temp, num_pnts_smooth, \
#         k_param, i_param, d_param = unPackParamInitAndPost(paramStatus)
    
#         p = current_process()
#         print('Starting:', p.name, p.pid)
        
#         #Pipe to communicate with "Get Temperature Process"
#         parent_conn_temp, child_conn_temp = Pipe()    
#         #Start Get Temperature Process        
#         ptemp = Process(name = "gettempProc", target=gettempProc, args=(child_conn_temp, myTempSensor))
#         ptemp.daemon = True
#         ptemp.start()   

#         #Pipe to communicate with "Heat Process"
#         parent_conn_heat, child_conn_heat = Pipe()    
#         #Start Heat Process      
#         pheat = Process(name = "heatProcGPIO", target=heatProcGPIO, args=(cycle_time, duty_cycle, pinNum, child_conn_heat))
#         pheat.daemon = True
#         pheat.start() 

#         temp_ma_list = []
#         manage_boil_trigger = False

#         tempUnits = xml_root.find('Temp_Units').text.strip()
#         numTempSensors = 0
#         for tempSensorId in xml_root.iter('Temp_Sensor_Id'):
#             numTempSensors += 1

#         temp_ma = 0.0

# 	#overwrite log file for new data log
#         ff = open("brewery" + str(myTempSensor.sensorNum) + ".csv", "wb")
#         ff.close()

#         readyPIDcalc = False

#         while (True):
#             readytemp = False
#             while parent_conn_temp.poll(): #Poll Get Temperature Process Pipe
#                 temp_C, tempSensorNum, elapsed = parent_conn_temp.recv() #non blocking receive from Get Temperature Process

#                 if temp_C == -99:
#                     print("Bad Temp Reading - retry")
#                     continue

#                 if (tempUnits == 'F'):
#                     temp = (9.0/5.0)*temp_C + 32
#                 else:
#                     temp = temp_C

#                 temp_str = "%3.2f" % temp
#                 display.showTemperature(temp_str)

#                 readytemp = True

#             if readytemp == True:
#                 if mode == "auto":
#                     temp_ma_list.append(temp)

#                     #smooth data
#                     temp_ma = 0.0 #moving avg init
#                     while (len(temp_ma_list) > num_pnts_smooth):
#                         temp_ma_list.pop(0) #remove oldest elements in list

#                     if (len(temp_ma_list) < num_pnts_smooth):
#                         for temp_pnt in temp_ma_list:
#                             temp_ma += temp_pnt
#                         temp_ma /= len(temp_ma_list)
#                     else: #len(temp_ma_list) == num_pnts_smooth
#                         for temp_idx in range(num_pnts_smooth):
#                             temp_ma += temp_ma_list[temp_idx]
#                         temp_ma /= num_pnts_smooth

#                     #print "len(temp_ma_list) = %d" % len(temp_ma_list)
#                     #print "Num Points smooth = %d" % num_pnts_smooth
#                     #print "temp_ma = %.2f" % temp_ma
#                     #print temp_ma_list

#                     #calculate PID every cycle
#                     if (readyPIDcalc == True):
#                         duty_cycle = pid.calcPID_reg4(temp_ma, set_point, True)
#                         #send to heat process every cycle
#                         parent_conn_heat.send([cycle_time, duty_cycle])
#                         readyPIDcalc = False
                    
#                 if mode == "boil":
#                     if (temp > boil_manage_temp) and (manage_boil_trigger == True): #do once
#                         manage_boil_trigger = False
#                         duty_cycle = boil_duty_cycle
#                         parent_conn_heat.send([cycle_time, duty_cycle])

#                 #put current status in queue
#                 try:
#                     paramStatus = packParamGet(numTempSensors, myTempSensor.sensorNum, temp_str, tempUnits, elapsed, mode, cycle_time, duty_cycle, \
#                             boil_duty_cycle, set_point, boil_manage_temp, num_pnts_smooth, k_param, i_param, d_param)
#                     statusQ.put(paramStatus) #GET request
#                 except Full:
#                     pass

#                 while (statusQ.qsize() >= 2):
#                     statusQ.get() #remove old status

#                 print("Current Temp: %3.2f deg %s, Heat Output: %3.1f%%" \
#                                                         % (temp, tempUnits, duty_cycle))

#                 logdata(myTempSensor.sensorNum, temp, duty_cycle)

#                 readytemp == False

#                 #if only reading temperature (no temp control)
#                 if readOnly:
#                     continue

#             while parent_conn_heat.poll(): #Poll Heat Process Pipe
#                 cycle_time, duty_cycle = parent_conn_heat.recv() #non blocking receive from Heat Process
#                 display.showDutyCycle(duty_cycle)
#                 readyPIDcalc = True

#             readyPOST = False
#             while conn.poll(): #POST settings - Received POST from web browser or Android device
#                 paramStatus = conn.recv()
#                 mode, cycle_time, duty_cycle_temp, boil_duty_cycle, set_point, boil_manage_temp, num_pnts_smooth, \
#                 k_param, i_param, d_param = unPackParamInitAndPost(paramStatus)

#                 readyPOST = True
#             if readyPOST == True:
#                 if mode == "auto":
#                     display.showAutoMode(set_point)
#                     print("auto selected")
#                     pid = PIDController.pidpy(cycle_time, k_param, i_param, d_param) #init pid
#                     duty_cycle = pid.calcPID_reg4(temp_ma, set_point, True)
#                     parent_conn_heat.send([cycle_time, duty_cycle])
#                 if mode == "boil":
#                     display.showBoilMode()
#                     print("boil selected")
#                     boil_duty_cycle = duty_cycle_temp
#                     duty_cycle = 100 #full power to boil manage temperature
#                     manage_boil_trigger = True
#                     parent_conn_heat.send([cycle_time, duty_cycle])
#                 if mode == "manual":
#                     display.showManualMode()
#                     print("manual selected")
#                     duty_cycle = duty_cycle_temp
#                     parent_conn_heat.send([cycle_time, duty_cycle])
#                 if mode == "off":
#                     display.showOffMode()
#                     print("off selected")
#                     duty_cycle = 0
#                     parent_conn_heat.send([cycle_time, duty_cycle])
#                 readyPOST = False
#             time.sleep(.01)
        

# def logdata(tank, temp, heat):
#     f = open("brewery" + str(tank) + ".csv", "a+")
#     f.write("%3.1f;%3.3f;%3.3f\n" % (getbrewtime(), temp, heat))
#     f.close()


# if __name__ == '__main__':

#     brewtime = time.time()
        
    
# The next two calls are not needed for January 2015 or newer builds (kernel 3.18.8 and higher)
# /boot/config.txt needs 'dtoverlay=w1-gpio' at the bottom of the file
# call(["modprobe", "w1-gpio"])
# call(["modprobe", "w1-therm"])
# call(["modprobe", "i2c-bcm2708"])
# call(["modprobe", "i2c-dev"])

# Retrieve root element from config.xml for parsing
tree = ET.parse('C:\\Users\msinclair\\Documents\\GitHub\\brewinator\\RasPiBrew\\config.xml')
xml_root = tree.getroot()
template_name = xml_root.find('Template').text.strip()

root_dir_elem = xml_root.find('RootDir')
# if root_dir_elem is not None:
#     os.chdir(root_dir_elem.text.strip())
# else:
#     print("No RootDir tag found in config.xml, running from current directory")

useLCD = xml_root.find('Use_LCD').text.strip()
if useLCD == "yes":
    tempUnits = xml_root.find('Temp_Units').text.strip()
    display = Display.LCD(tempUnits)
else:
    display = Display.NoDisplay()

# gpioNumberingScheme = xml_root.find('GPIO_pin_numbering_scheme').text.strip()
# if gpioNumberingScheme == "BOARD":
#     GPIO.setmode(GPIO.BOARD)
# else:
#     GPIO.setmode(GPIO.BCM)

gpioInverted = xml_root.find('GPIO_Inverted').text.strip()
if gpioInverted == "0":
    ON = 1
    OFF = 0
else:
    ON = 0
    OFF = 1

pinHeatList=[]
for pin in xml_root.iter('Heat_Pin'):
    pinHeatList.append(int(pin.text.strip()))
    #print(pin.text.strip())

print(pinHeatList)    

tempOffsetList=[]
for tempOffset in xml_root.iter('Temp_Offset'):
    tempOffsetList.append(int(tempOffset.text.strip()))
    #print(pin.text.strip())

print(tempOffsetList)    


pinGPIOList=[]
for pin in xml_root.iter('GPIO_Pin'):
    pinGPIOList.append(int(pin.text.strip()))
    #print(pin.text.strip())

# for pinNum in pinGPIOList:
#     GPIO.setup(pinNum, GPIO.OUT)

for tempSensorId in xml_root.iter('Temp_Sensor_Id'):
    myTempSensor = Temp1Wire.Temp1Wire(tempSensorId.text.strip())     
        
    if len(pinHeatList) >= myTempSensor.sensorNum + 1:
        pinNum = pinHeatList[myTempSensor.sensorNum]
        tempOffset = tempOffsetList[myTempSensor.sensorNum]
        readOnly = False
    else:
        pinNum = 0
        tempOffset = 0
        readOnly = True
    
    if myTempSensor.sensorNum >= 1:
        display = Display.NoDisplay()
            

    # if myTempSensor.sensorNum == 0:
        # statusQ = Queue(2) #blocking queue        
        # parent_conn, child_conn = Pipe()
        # p = Process(name = "tempControlProc", target=tempControlProc, args=(myTempSensor, display, pinNum, readOnly, \
        #                                                     param.status, statusQ, child_conn))
        # p.start()
        
    # if myTempSensor.sensorNum == 1:
        # statusQ_B = Queue(2) #blocking queue    
        # parent_connB, child_conn = Pipe()  
        # p = Process(name = "tempControlProc", target=tempControlProc, args=(myTempSensor, display, pinNum, readOnly, \
        #                                                     param.status, statusQ_B, child_conn))
        # p.start()
        
    # if myTempSensor.sensorNum == 2:
        # statusQ_C = Queue(2) #blocking queue 
        # parent_connC, child_conn = Pipe()     
        # p = Process(name = "tempControlProc", target=tempControlProc, args=(myTempSensor, display, pinNum, readOnly, \
        #                                                     param.status, statusQ_C, child_conn))
        # p.start()

    # app.debug = True 
    # app.run(use_reloader=False, host='0.0.0.0')