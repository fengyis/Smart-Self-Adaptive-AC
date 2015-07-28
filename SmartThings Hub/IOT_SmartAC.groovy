/**
 *  IOT_SmartAC
 *
 *  Copyright 2015 IoT
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 *  in compliance with the License. You may obtain a copy of the License at:
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 *  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License
 *  for the specific language governing permissions and limitations under the License.
 *
 */
definition(
    name: "IOT_SmartAC",
    namespace: "",
    author: "Fengyi Song",
    description: "SmartAC",
    category: "My Apps",
    iconUrl: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience.png",
    iconX2Url: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience@2x.png",
    iconX3Url: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience@2x.png",
    oauth: true)


preferences {

    section("Allow Endpoint to Control These Things...") {
        input "vents", "capability.temperatureMeasurement", multiple: true
        //input "vent_2", "capability.Battery", multiple: false
        //input "configuration","capability.configuration",multiple:false
      //  href "http://keenhome.io"
    }
}

def installed() {
	log.debug "Installed with settings: ${settings}"

	initialize()
}

def updated() {
	log.debug "Updated with settings: ${settings}"

	unsubscribe()
	initialize()
}

def initialize() {
	// TODO: subscribe to attributes, devices, locations, etc.
 
    subscribe(vents, "level", handleLevel)
   
    subscribe(vents,"temperature", handleTemperature)
    
    sendEvent(name: "level",value:50)
   
    
    
    
}



// TODO: implement event handlers


def handleLevel(evt) {
    log.trace "handleLevel()"
    log.debug "current evt is ${evt.name}"
    log.debug "current level is ${evt.numericValue}"
    runIn(60*2,getFromParse)
    //runEvery5Minutes(getFromParse)
}


def handleTemperature(evt) {
    log.trace "handleTemperature()"
    sendEventData(evt, "temperature", evt.numericValue)
    sendEvent(name: "level",value:50)
}

def sendEventData(evt, tag, value) {
    log.trace "sendEventData()"
    
    def vent = vents.find { it.id == evt.deviceId }
    def zigbeeId = vent.currentValue("zigbeeId")
    log.debug "\tdeviceId: ${evt.deviceId}"
    log.debug "\tzigbeeId: ${zigbeeId}"
    log.debug "\tdevice name:  ${evt.displayName }"
//    log.devug "\tvalue: ${value}"

    putOnParse(value)

   



}

def getFromParse(){
  try {
	httpGet("https://JxFyNYutkklDBpo2aCdaSsTmaDDRsFpk2h4L5Ewb:javascript-key=AJC0OzLmMarZEwuGxsX4ymxIGwrqakRQerrC16PM@api.parse.com/1/classes/WorkObject/mR8AWQdHL3") 
        { 
        resp ->   
            log.debug "response data: ${resp.data}"
            log.debug "response contentType: ${resp.contentType}"

            log.debug "Level is ${resp.data['Level']}"
            state.Level=resp.data['Level']
            vents.setLevel(resp.data['Level'])

        }
    } catch (e) {
        log.error "something went wrong: $e"
    }


}

def putOnParse(value){
try {
    def params = [
    uri: "https://JxFyNYutkklDBpo2aCdaSsTmaDDRsFpk2h4L5Ewb:javascript-key=AJC0OzLmMarZEwuGxsX4ymxIGwrqakRQerrC16PM@api.parse.com/1/classes/WorkObject/mR8AWQdHL3",
    body: [
        "Tindoor":value
    ]
]
    httpPutJson(params) { resp ->
        resp.headers.each {
            log.debug "${it.name} : ${it.value}"
        }
        log.debug "response contentType: ${resp.contentType}"
    }
} catch (e) {
    log.debug "something went wrong: $e"
}


}


