# SOT

This demo illustrates an IoT solution for a security camera that detects faces locally and sends the detections using MQTT to Google's Cloud IoT Core. The system is composed of a smart camera with a built in edge ML capability and a router that enables multiple security cameras to be connected to Google Cloud over a secure LAN and via the public internet. Security is provided via authentication for individual devices.

For physical security of the device each of these devices has their own secure element to reduce the risk of tampering. The secure elements are to be acquired from a manufacturer (e.g., Microchip  ATECC608A) and the public keys registered in Google cloud IoT in support of the application to leverage these devices. These secure elements are soldered onto the printed circuit board of the cameras at manufacture time. The chip also will validate the firmware with code signature validation to offer a secure boot process.

Standard Scenario:
* Monitor a secured area with a set of cameras - snapshot every N minutes
* Detect faces in the image locally on the security camera using ML model executed using EdgeTPU 
* Send prediction from ML model to the cloud with an MQTT telemetry topic
* Process the stream of detections in DataFlow
* Store the detected objects & summary in Big Query
* Display a summary of the detections 

The following is a high level view of the architecture.

![SoT Architecture](/images/SecurityOfThings.png)
