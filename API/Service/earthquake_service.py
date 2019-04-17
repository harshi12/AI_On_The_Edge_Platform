import sys
sys.path.insert (0, '../')

import numpy as np
import json
import argparse
import pickle
from ServiceManager.platform_input_stream import *

class EarthquakeService:
    def __init__(self, service_id):
        self.service_id = service_id

    def input_data_cb(self, ch, method, properties, input_data):
        if not isinstance(input_data, str):
            input_data = input_data.decode()

        data = json.loads(input_data)

        # content is a list received as a string e.g. "[a, b, c, d]"
        # converting it into an actual list
        test = [ float(data["time"]) , float(data["latitude"]), float(data["longitude"])]

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
        # TODO
        print (res)
            
       


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--service_id", default="-1")
    parser.add_argument("--run_on_gateway", default="no")

    (args, unknown) = parser.parse_known_args()

    earthquake_detect_service = EarthquakeService(args.service_id)

    sensor_type = "LOCATION_TIME_SENSOR"

    if args.run_on_gateway == "no":
        input_stream = PlatformInputStream()
        input_stream.service_register_request(args.service_id, sensor_type, "default_rate")
        input_stream.recv_input_content(args.service_id, earthquake_detect_service.input_data_cb)
