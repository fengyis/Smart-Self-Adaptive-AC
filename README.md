# Smart Self-Adaptive Air Conditioner

##[Visit our website!](https://smartac.parseapp.com)

##1.Raspberry Pi Bluetooth Discovery

This folder contains the python programm running on raspberry pi with linux operating system. The raspberry pi has to be equiped with bluetooth dongle and wifi module. Its purpose is to utilize bluetooth to detect the number of bluetooth devices within its range.
##2.Parse Cloud Function
This folder contains the Cloud code written in javascript.
This is the main cloud function which will be invoked in a arbitrary period. One of its puporse is to implement our algorithm in calculating the setthing temperature, working power and fan angle. The cloud function could be invoked through HTTP post request.

##3.Smart Things Hub Smart APP
This programm is our smart app written in groovy deployed on Smart Things Hub and its web IDLE. The function of the smart app is to extract the information from the device and push the data on cloud. 
It is supposed to work with the Smart Vent Device provided by Keen Home. For the reason of business confidentiality, we do not include the source code of the device. If you need it for some reason, feel free to email me and Keen Home.

##4. Website Source Code
This is our webpage demonstrating detailed description of the project.
