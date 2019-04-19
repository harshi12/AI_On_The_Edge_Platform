import sys

from pathlib import Path
home = str(Path.home())
path = home+'/Platform/'

sys.path.insert (0, path)

import pandas as pd
import json
import requests
import time
import argparse

from queue_req_resp import *
from ServiceManager.platform_input_stream import *
from ServiceManager.platform_output_stream import *


class FlowerAnalysisService:
    def __init__(self, service_id, run_on_gateway, serving_addrs, model):
        self.service_id = service_id
        self.run_on_gateway = run_on_gateway
        self.serving_addrs = serving_addrs
        self.model = model

    def input_data_cb(self, ch, method, properties, input_data):
        if not isinstance(input_data, str):
            input_data = input_data.decode()

        #print ("Received input: ", input_data)

        data = json.loads(input_data)

        req = {}
        req["signature_name"] = "predict"
        req["instances"] = []

        # content is a list received as a string e.g. "[a, b, c, d]"
        # converting it into an actual list
        data["content"] = data["content"][1:-1].split(', ')

        instance = {}
        instance["sepal_length"] = [float(data["content"][0])]
        instance["sepal_width"] = [float(data["content"][1])]
        instance["petal_length"] = [float(data["content"][2])]
        instance["petal_width"] = [float(data["content"][3])]

        req["instances"].append(instance)

        req_str = json.dumps(req)
        headers = {"content-type" : "application/json"}

        # get IP of the tensorflow serving from Service Manager
        serving_addrs = "192.168.43.30:9500"
        json_response = requests.post('http://' + serving_addrs + "/v1/models/iris:predict", data=req_str, headers=headers)
        json_response = json.loads(str(json_response.text))
        inference = json_response["predictions"][0]

        if inference['classes'] == ['0']:
            flower = "Iris-Setosa"
        elif inference['classes'] == ['1']:
            flower = "Iris-Virginica"
        elif inference['classes'] == ['2']:
            flower = "Iris-Versicolor"
        else:
            print ("It shouldn't reach here!!")
            sys.exit(1)

        if self.run_on_gateway == "no":
            output_stream = PlatformOutputStream()
            output_stream.service_output_send(self.service_id, flower)

        #print ("FlowerAnalysisService Inference:", flower)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--service_id", default="-1")
    parser.add_argument("--run_on_gateway", default="no")
    parser.add_argument("--is_first_instance", default="no")
    parser.add_argument("--serving_addrs", default="127.0.0.1:9500")
    parser.add_argument("--model", default="")

    (args, unknown) = parser.parse_known_args()

    flower_analysis_service = FlowerAnalysisService(args.service_id, args.run_on_gateway, args.serving_addrs, args.model)

    sensor_name = "FLOWER_ANALYSIS_SENSOR"

    if args.run_on_gateway == "no":
        input_stream = PlatformInputStream()

        if args.is_first_instance == "yes":
            input_stream.service_register_request(args.service_id, sensor_name, "default_rate")

        input_stream.service_recv_input_request(args.service_id, flower_analysis_service.input_data_cb)
