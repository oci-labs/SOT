# SOT

This demo illustrates an IoT solution for a security camera that detects faces locally and sends the detections using MQTT to Google's Cloud IoT Core. The system is composed of a smart camera with a built in edge ML capability and a router that enables multiple security cameras to be connected to Google Cloud over a secure LAN and via the public internet. The applicaiton on the camera will use a face detection ML predictor that will provide the bounding boxes for all detected faces within the image once per second. It will also collect the max, min and average number of faces detected over a defined time window. This data will be displayed via a dashboard in Google Cloud.

Security is provided via authentication for individual devices. For physical security of the device each of these devices has their own secure element to reduce the risk of tampering. The secure elements are to be acquired from a manufacturer (e.g., Microchip  ATECC608A) and the public keys registered in Google cloud IoT in support of the application to leverage these devices. These secure elements are soldered onto the printed circuit board of the cameras at manufacture time. The chip also will validate the firmware with code signature validation to offer a secure boot process. Additional steps for securing the device, such as on on Raspberry Pi can be found here: https://www.raspberrypi.org/documentation/configuration/security.md

## Standard Scenario:
* Monitor a secured area with a set of cameras - snapshot every second
* Detect faces in the image locally on the security camera using ML model executed using EdgeTPU 
* Send prediction from ML model to the cloud with an MQTT telemetry topic
* Process the stream of detections in DataFlow
* Store the detected objects & summary in Big Query
* Display a summary of the detections 

The following is a high level view of the architecture.

![SoT Architecture](/images/SecurityOfThings.png)

## Enable the following APIs:
```
gcloud services enable compute.googleapis.com
gcloud services enable dataflow.googleapis.com
gcloud services enable pubsub.googleapis.com
gcloud services enable cloudiot.googleapis.com
gcloud services enable bigquery-json.googleapis.com
```

## Configure Big Query

From the root directory, create the datasets and the tables using the schema provided in the bigquery directory.

```
bq mk --dataset security_dataset
bq mk --table security_dataset.sot_table bigquery/sot_table.json
bq mk --table security_dataset.sot_view_table bigquery/sot_view_table.json
```

## Configure Dataflow

We will use the PubSub to BigQuery template to load the data from the device into BigQuery.

```
gcloud dataflow jobs run JOB_NAME \
    --gcs-location gs://dataflow-templates/latest/PubSub_to_BigQuery \
    --parameters \
inputTopic=projects/securityofthings/topics/sot-topic,\
outputTableSpec=securityofthings:security_dataset.sot_table
 ```

## Create an IoT Registry
We will set up a registry with the name of sot-registry, in us-central1, with project_id of securityofthings. The pub/sub topic is set to sot-topic. 

## Create Device in Registry
Create a device with device_id of security-cam-oci in the registry and add the public key for that device -- the private key of the device should be stored locally on the device in the resources folder (SOT/cloud-iot-direct/resources). Add the CA certificates (root.pem) in (SOT/cloud-iot-direct/) folder.

## Setup Security Camera
Setup the Coral USB Accelerator which a USB device that provides an Edge TPU as a coprocessor for the Raspberry Pi. Follow the steps from here: https://coral.withgoogle.com/tutorials/accelerator/

```
cd SOT/cloud-iot-direct/
pip install -r requirements.txt
```

## Run the following python command (python 3.5): 

```
python3 security_cam_cloudiot.py --registry_id=sot-registry --cloud_region=us-central1 --project_id=securityofthings --device_id=security-cam-oci --algorithm=RS256 --private_key_file=resources/rsa_private.pem 
```
## Create a Data Studio View 

Here is an example of the Dashboard created for the camera.

![SoT Architecture](/images/DataStudioDashboard.png)

