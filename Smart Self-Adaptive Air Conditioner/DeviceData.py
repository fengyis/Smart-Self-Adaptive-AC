class DeviceData:

  devices = []
  count = 0
	
  timeOutValue = 0 

  def __init__(self):

		
    self.timeOutValue = 10

  
  def FindObject(self,bluetoothAddress):
    for obj in self.devices:
      if(obj.BdAddr == bluetoothAddress):
        return obj

		
