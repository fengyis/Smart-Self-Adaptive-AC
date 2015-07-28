############################################################
# IOT Poject
# Pulls the Weather forecast, Temperature, Pressure, Humidity
# Website for forecast: www.openweathermap.org
# Communication with lghtbulb.c happens over IPC communication port 50008
############################################################
import os
import json
import httplib2
import time
import socket
import traceback
import httplib
from decimal import Decimal
from threading import Thread
import datetime
import subprocess


# Update on Parse
def updateWeatherOnParse(weather, temperature):
	print city
	print country
	print weather
	print temperature
	if city != None and country != None and weather != None and temperature != None:

		print "weather temperatrue update start"
		
		connection = httplib.HTTPSConnection("api.parse.com", 443)
		connection.connect()
		connection.request('PUT', '/1/classes/WorkObject/mR8AWQdHL3', json.dumps({
       "Toutdoor": temperature
     }), {
       "X-Parse-Application-Id": "JxFyNYutkklDBpo2aCdaSsTmaDDRsFpk2h4L5Ewb",
       "X-Parse-REST-API-Key": "H6IpwFxLIfNzsMawX94Z80WrA8yuNzwaVHPhiNA5",
       "Content-Type": "application/json"
     })

		print "weather temperature update finish!!!!! " 

def weatherApi():
	h = httplib2.Http(".cache")
	h.add_credentials('', '')
	while(True):
		#resp, content = h.request(baseUrl  + city + "," + country, "GET")
		URL="http://api.openweathermap.org/data/2.5/weather?q=newyork,USA"
		resp,content=h.request(URL,"GET")
		try:
			contentJson = json.loads(content)
		except:
			print(traceback.format_exc())
			print "weather::main(): JSON Exception" 
			continue

		weather = contentJson["weather"][0]["main"]
		temK = contentJson["main"]["temp"]
		temperature = round((temK-273.15)*1.8+32, 2)
		pressure = contentJson["main"]["pressure"]
		humidity = contentJson["main"]["humidity"]
		

		localInfoText = city + "\n" + country + "\n" + weather + "\n" + str(temperature) + "\n"
		print "weather.py ::: "
		print temperature
		print localInfoText

		updateWeatherOnParse(weather, temperature)


		time.sleep(600)    #minute 10, 10*60 seconds


def cloudFunction():
	while(True):
                time.sleep(20)   #call cloudFunction every 20s
		connection = httplib.HTTPSConnection('api.parse.com', 443)
		connection.connect()
		connection.request('POST', '/1/functions/smartSet', json.dumps({

			}), {
		        "X-Parse-Application-Id": "JxFyNYutkklDBpo2aCdaSsTmaDDRsFpk2h4L5Ewb",
		        "X-Parse-REST-API-Key": "H6IpwFxLIfNzsMawX94Z80WrA8yuNzwaVHPhiNA5",
		        "Content-Type": "application/json"
		        })
		result = json.loads(connection.getresponse().read())
		print "cloudFunction:::"
		print result




if __name__== "__main__":

	city = "New York"
	country = "USA"
	try:

		weatherThread = Thread(target = weatherApi)
		weatherThread.daemon = True
	


	

		cloudThread = Thread(target = cloudFunction)
		#cloudThread.daemon = True

		weatherThread.start()
		cloudThread.start()


        	#p1 = subprocess.Popen('python ./ble.py', shell=True, preexec_fn=os.setsid)
	
	except KeyboardInterrupt:
		#weatherThread.
		p1.terminate()
		os.killpg(p1.pid, signal.SIGTERM)


 #    time.sleep(50)
 #    p1.terminate()
	# os.killpg(p2.pid, signal.SIGTERM)



    







