# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import sys
import socket
from colors import bcolors
from pprint import pprint
import random
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import random
import json
# from

import execnet


def call_python_version(Version, Module, Function, ArgumentList):
    gw = execnet.makegateway("popen//python=python%s" % Version)
    channel = gw.remote_exec("""
        from %s import %s as the_function
        channel.send(the_function(*channel.receive()))
        """ % (Module, Function))
    channel.send(ArgumentList)
    return channel.receive()


DHT_SENSOR_PIN = 4

ADDR = '172.16.10.106'
PORT = 10000
# Create a UDP socket
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (ADDR, PORT)

device_id = sys.argv[1]
print("device_id", device_id)
if not device_id:
    sys.exit('The device id must be specified.')

print('Bringing up device {}'.format(device_id))


# return message received
def SendCommand(sock, message, log=True):
    if log:
        print >> sys.stderr, 'sending: "%s"' % message
    sock.sendto(message, server_address)

    # Receive response
    if log:
        print >> sys.stderr, 'waiting for response'
    response, _ = sock.recvfrom(4096)
    if log:
        print >> sys.stderr, 'received: "%s"' % response

    return response


print('Bring up device 1')


def MakeMessage(device_id, action, data=None):
    if data:
        return '{{ "device" : "{}", "action":"{}", "data" : {} }}'.format(device_id, action, json.dumps(data))
    else:
        return '{{ "device" : "{}", "action":"{}" }}'.format(device_id, action)


def RunAction(action):
    message = MakeMessage(device_id, action)
    if not message:
        return
    print('Send data: {} '.format(message))
    event_response = SendCommand(client_sock, message)
    print("Response " + event_response)


try:
    random.seed()
    RunAction('detach')
    RunAction('attach')

    while True:
        # h, t = Adafruit_DHT.read_retry(22, DHT_SENSOR_PIN)
        h = random.randint(100, 200)
        t = random.randint(0, 50)
        t = t * 9.0 / 5 + 32

        result = call_python_version("3.5", "edgetpu.demo.classify_capture", "main",
                                     ['./edgetpu/test_data/inception_v2_224_quant_edgetpu.tflite',
                                      './edgetpu/test_data/imagenet_labels.txt'])

        print(result["val"])
        print(result["label"])

        value = "{:.3f}".format(result["val"])
        #    t = "{:.3f}".format(t)
        sys.stdout.write('\r >>' + bcolors.CGREEN + bcolors.BOLD +
                         'Object: {}, Val: {}'.format(result["label"], value) + bcolors.ENDC + ' <<')
        sys.stdout.flush()

        info = {'device': device_id}
        # info = json.dumps(info)

        message = MakeMessage(device_id=device_id, action='event', data=info)

        SendCommand(client_sock, message, False)
        time.sleep(2)


finally:
    print >> sys.stderr, 'closing socket'
    client_sock.close()
