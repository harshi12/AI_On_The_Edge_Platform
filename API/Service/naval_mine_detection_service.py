import sys
sys.path.insert (0, '../')
sys.path.insert (0, '../../')

import pandas as pd
import json
import requests
import time
import argparse
import numpy as np

from queue_req_resp import *
from ServiceManager.platform_input_stream import *


class SonarService:
    def __init__(self, service_id, run_on_gateway):
        self.service_id = service_id
        self.run_on_gateway = run_on_gateway

    def input_data_cb(self, ch, method, properties, input_data):
        if not isinstance(input_data, str):
            input_data = input_data.decode()

        data = json.loads(input_data)
        # print (data)
        req = {}
        req["signature_name"] = "model"
        req["instances"] = []

        # content is a list received as a string e.g. "[a, b, c, d,...]"
        # converting it into an actual list
        data["content"] = data["content"][1:-1].split(', ')
        data = [data["content"]]
        data = np.array(data)
        data = data.astype(float)
        data = data[0].tolist()

        req["instances"].append(data)

        req_str = json.dumps(req)
        headers = {"content-type" : "application/json"}

        # get IP of the tensorflow serving from Service Manager
        serving_addrs = "10.2.133.230:9500"
        json_response = requests.post('http://' + serving_addrs + "/v1/models/sonar_model:predict", data=req_str, headers=headers)

        # print (json.loads(json_response.text))
        predictions = json.loads(json_response.text)["predictions"]

        predictions = np.array(predictions)
        if np.argmax(predictions, axis=1)[0] == 1:
            print ("Sonar service inference: ", np.argmax(predictions, axis=1)[0] , "Rock")
        else:
            print ("Sonar service inference: ", np.argmax(predictions, axis=1)[0] , "Mine")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--service_id", default="-1")
    parser.add_argument("--run_on_gateway", default="no")
    parser.add_argument("--is_first_instance", default="no")

    (args, unknown) = parser.parse_known_args()

    sonar_service = SonarService(args.service_id, args.run_on_gateway)

    sensor_name = "SONAR_SENSOR"

    if args.run_on_gateway == "no":
        input_stream = PlatformInputStream()

        if args.is_first_instance == "yes":
            input_stream.service_register_request(args.service_id, sensor_name, "default_rate")

        input_stream.service_recv_input_request(args.service_id, sonar_service.input_data_cb)
