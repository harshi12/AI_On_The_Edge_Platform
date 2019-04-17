import sys
sys.path.insert (0, '../')

import pandas as pd
import json
import requests
import time
import argparse

from RabbitMQ.message_queue import *
from ServiceManager.platform_input_stream import *


class FlowerAnalysisService:
    def __init__(self, service_id):
        self.service_id = service_id

    def input_data_cb(self, ch, method, properties, input_data):
        if not isinstance(input_data, str):
            input_data = input_data.decode()

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
        serving_addrs = "192.168.31.124:9500"
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

        print ("FlowerAnalysisService Inference:", flower)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--service_id", default="-1")
    parser.add_argument("--run_on_gateway", default="no")

    (args, unknown) = parser.parse_known_args()

    flower_analysis_service = FlowerAnalysisService(args.service_id)

    sensor_type = "FLOWER_ANALYSIS_SENSOR"

    if args.run_on_gateway == "no":
        input_stream = PlatformInputStream()
        input_stream.service_register_request(args.service_id, sensor_type, "default_rate")
        input_stream.recv_input_content(args.service_id, flower_analysis_service.input_data_cb)
