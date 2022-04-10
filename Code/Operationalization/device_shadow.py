from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from awscrt import mqtt

from csv import reader
import json
import time

ENDPOINT = "ao1qb7qm40l3z-ats.iot.us-west-2.amazonaws.com"
CLIENT_ID = "pbiot"
PATH_TO_CERTIFICATE = "./Code/Operationalization/certificates/pbiot.cert.pem"
PATH_TO_PRIVATE_KEY = "./Code/Operationalization/certificates/pbiot.private.key"
PATH_TO_AMAZON_ROOT_CA_1 = "./Code/Operationalization/certificates/root-CA.crt"

TOPIC = "$aws/things/pbiot/shadow/update"


clientId = "mypb-iot"
thingName = "pbiot"
isOn = False
myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
myAWSIoTMQTTShadowClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTShadowClient.configureCredentials(
    PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)

myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)

myAWSIoTMQTTShadowClient.connect()

deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, False)

def read_and_upload_to_device_shadow():
    with open("./Data/Modeling/occupancy.csv", "r") as my_file:
        file_reader = reader(my_file)
        for i in file_reader:
            print("Sending data...")
           
            if i[7] == 1:
                newPayload = '{"state":{"desired":{"isThing":"true"}}}'
                deviceShadowHandler.shadowUpdate(newPayload, None, 5)
            else:
                newPayload = '{"state":{"desired":{"isThing":"false"}}}'
                deviceShadowHandler.shadowUpdate(newPayload, None, 5)

while True:
    read_and_upload_to_device_shadow()
