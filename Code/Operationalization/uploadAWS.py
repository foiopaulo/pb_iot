from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
from csv import reader
import json
import time as t

ENDPOINT = "ao1qb7qm40l3z-ats.iot.us-west-2.amazonaws.com"
CLIENT_ID = "pbiot"
PATH_TO_CERTIFICATE = "./Code/Operationalization/certificates/pbiot.cert.pem"
PATH_TO_PRIVATE_KEY = "./Code/Operationalization/certificates/pbiot.private.key"
PATH_TO_AMAZON_ROOT_CA_1 = "./Code/Operationalization/certificates/root-CA.crt"

TOPIC = "pbiot/occupancy"


def connect_aws_iot_core():
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        cert_filepath=PATH_TO_CERTIFICATE,
        pri_key_filepath=PATH_TO_PRIVATE_KEY,
        ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
        client_bootstrap=client_bootstrap,
        client_id=CLIENT_ID,
        clean_session=False,
        keep_alive_secs=6)

    connection_future = mqtt_connection.connect()
    connection_future.result()
    return mqtt_connection


def read_and_upload_to_aws():
    with open("./Data/Processed/ocuppancy_processed.csv", "r") as my_file:
        mqtt_connection = connect_aws_iot_core()
        file_reader = reader(my_file)
        for i in file_reader:
            message = {"date": i[1],
                       "temperature": i[2],
                       "humidity": i[3],
                       "light": i[4],
                       "co2": i[5]}
            print("Sending data: {}".format(message))
            mqtt_connection.publish(topic=TOPIC,
                                    payload=json.dumps(message),
                                    qos=mqtt.QoS.AT_LEAST_ONCE)
            t.sleep(.01)
        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()

read_and_upload_to_aws()
