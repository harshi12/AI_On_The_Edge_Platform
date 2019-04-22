import sys
from pathlib import Path
home = str(Path.home())
path = home+'/Platform/'
sys.path.insert (0, path)
from queue_req_resp import *

import numpy as np
import json
import argparse
import pickle


from ServiceManager.platform_input_stream import *
from ServiceManager.platform_output_stream import *

class EarthquakeService:
    def __init__(self, service_id, run_on_gateway):
        self.service_id = service_id
        self.run_on_gateway = run_on_gateway

    def input_data_cb(self, ch, method, properties, input_data):
        if not isinstance(input_data, str):
            input_data = input_data.decode()

        data = json.loads(input_data)

        # content is a list received as a string e.g. "[a, b, c, d]"
        # converting it into an actual list
        print (f"[EarthquakeService] receiving data --> {data}")
        test = [data["content"][1:-1].split(', ')]
        #test = [ float(data["time"]) , float(data["latitude"]), float(data["longitude"])]

        with open("./earthquake_dir/earthquake_model", 'rb') as f:
            rf = pickle.load(f)

        pre = rf.predict(test)
        
        magnitude = pre[:,0]
        depth = pre[:,1]
        
        res = ''
        if depth > 400.:
            res += "Earthquake : LOW, Magnitude : " + str(magnitude) + " Depth : " + str(depth)
        else:
            if magnitude < 6.0:
                res += "Earthquake : MILD, Magnitude : " + str(magnitude) + " Depth : " + str(depth)
            else:
                res += "Earthquake : HIGH, Magnitude : " + str(magnitude) + " Depth : " + str(depth)

        if self.run_on_gateway == "no":
            output_stream = PlatformOutputStream()
            output_stream.service_output_send(self.service_id, res)
        # print (res)
            
       
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--service_id", default="-1")
    parser.add_argument("--run_on_gateway", default="no")
    parser.add_argument("--is_first_instance", default="no")

    (args, unknown) = parser.parse_known_args()

    earthquake_detect_service = EarthquakeService(args.service_id, args.run_on_gateway)

    sensor_name = "LOCATION_TIME_SENSOR"

    if args.run_on_gateway == "no":
        input_stream = PlatformInputStream()

        if args.is_first_instance == "yes":
            input_stream.service_register_request(args.service_id, sensor_name, "default_rate")

        input_stream.service_recv_input_request(args.service_id, earthquake_detect_service.input_data_cb)
