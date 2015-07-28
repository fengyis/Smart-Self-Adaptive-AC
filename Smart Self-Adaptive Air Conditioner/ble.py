import sys,pexpect,subprocess
import traceback,time
from threading import Thread
import httplib
import json
import DeviceData


class Device:
  def __init__(self,name,bdaddr):
    self.name=name
    self.BdAddr=bdaddr
    self.timeStamp = time.time()
  def ToString(self):
    return "Name: "+self.name+" Addr "+self.BdAddr
class wicedsense:
  # Init function to connect to wiced sense using mac address
  # Blue tooth address is obtained from blescan.py 
  def __init__( self, bluetooth_adr ):
    self.con = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive')
    self.con.expect('\[LE\]>', timeout=600)
    print "Preparing to connect. You might need to press the side button..."
    self.con.sendline('connect')
    
    self.con.expect('Connection successful.*\[LE\]>')
    print "Connection successful"

    return


def pushData():
  while True:
    time.sleep(60)#put data every 10 minutes
    global count
    print "count is "+str(count)
    baseUrl = "api.parse.com"
    connection = httplib.HTTPSConnection(baseUrl, 443)
    connection.connect()
    connection.request('PUT', '/1/classes/WorkObject/mR8AWQdHL3', json.dumps({
         "FlowRate": count
         
     }), {
         "X-Parse-Application-Id": "JxFyNYutkklDBpo2aCdaSsTmaDDRsFpk2h4L5Ewb",
         "X-Parse-REST-API-Key": "H6IpwFxLIfNzsMawX94Z80WrA8yuNzwaVHPhiNA5",
         "Content-Type": "application/json"
     })
    print "put successfully"

# def pushNotification(Situation):
#   connection = httplib.HTTPSConnection('api.parse.com', 443)
#   connection.connect()
#   connection.request('POST', '/1/push', json.dumps({
#            "where": {
#              "channels": "bulb"
#            },
#            "data": {
#              "Situation": Situation
#            }
#          }), {
#            "X-Parse-Application-Id": "tDqgJgXy6F4s7imyPGuPEFyLFkeEkm3B1kEUMg8D",
#            "X-Parse-REST-API-Key": "oB1DseqDiajKRJsOsQ56cDCBYuMgYkFi5hPm9VEd",
#            "Content-Type": "application/json"
#          })
#   result = json.loads(connection.getresponse().read())
#   print result

def Scan():

  print "start scanning"
  bleScanProcess = subprocess.Popen(['sudo','hcitool', 'lescan'], stdout=subprocess.PIPE,stderr=subprocess.PIPE, bufsize=0)

  line = bleScanProcess.stdout.readline()
  while line:
    #print line
    lineData = line.strip("\n")
    name = lineData.split(' ',1)[1]
    
    bdAddr = lineData.split(' ')[0]
    
    #if (name == "WICED Sense Kit"):
    # print "in loop"      
    obj=BluetoothDevice.FindObject(bdAddr)
    
    if not obj:
            
      print "Add device "+name
      
      print "Device address "+bdAddr
      btObj=Device(name,bdAddr)
      btObj.name=name
      btObj.BdAddr=bdAddr
      BluetoothDevice.devices.append(btObj)
      BluetoothDevice.count+=1
      global count
      count+=1
      print "No. of Devices "+str(count)
    else:
      obj.timeStamp=time.time()
    line = bleScanProcess.stdout.readline()

  #fp=open("Device.txt","w")
  #fp.write(str(devices))
  #fp.close()    
  print "exit"

def BTScan():
  while True:
    
    print "start BT scanning"
    bleScanProcess = subprocess.Popen(['sudo','hcitool', 'scan'], stdout=subprocess.PIPE,stderr=subprocess.PIPE, bufsize=0)

    line = bleScanProcess.stdout.readline()
    while line:
      print line
      lineData = line.strip("\n")
      if len(lineData.split(" ")) >1: 
        name = lineData.split(" ")[1]
        
        bdAddr = lineData.split(" ")[0]
        
        #if (name == "WICED Sense Kit"):
        # print "in loop"      
        obj=BluetoothDevice.FindObject(bdAddr)
        
        if not obj:
                
          print "Add device "+name
          
          print "Device address "+bdAddr
          btObj=Device(name,bdAddr)
          btObj.name=name
          btObj.BdAddr=bdAddr
          BluetoothDevice.devices.append(btObj)
          BluetoothDevice.count+=1
          global count
          count+=1
          print "No. of Devices "+str(count)
        else:
          obj.timeStamp=time.time()
      
      line = bleScanProcess.stdout.readline()

    time.sleep(60)  
  print "exit"
    

def handleTimeOut():
  while True:
    # Check if 3 * timeout has passed for each neighbors
    time.sleep(120)
    for sense in BluetoothDevice.devices:
      if((time.time()-sense.timeStamp) > 240):
        print "timedout\n"
        print sense.name+" removed"
	BluetoothDevice.devices.remove(sense)
        global count
        count-=1

def writeDevice():
  while True:
    time.sleep(120)
    fp=open("Device.txt","w")
    
    for i in BluetoothDevice.devices:
      print i.name
      fp.write(i.ToString())
    #fp.write(str(BluetoothDevice.devices))
    fp.close()  



if __name__ == "__main__":
  global count
  count=0
  devices=[]
  BluetoothDevice=DeviceData.DeviceData()

  subprocess.call(["sudo","hciconfig","hci0","down"])
  subprocess.call(["sudo","hciconfig","hci0","up"])
  scanThread = Thread(target = Scan, name = 'lescan')

  btscanThread = Thread(target = BTScan, name = 'btscan')
  writeThread = Thread(target = writeDevice, name = 'writetoFile')
  pushThread=Thread(target=pushData,name='putParse')
  timeOutThread = Thread(target = handleTimeOut, name = 'timeout')
  scanThread.start()
  btscanThread.start()
  writeThread.start()
  pushThread.start()
  timeOutThread.start()
  

 

