import sys
sys.path.insert (0, '../')

import argparse
import json

from ServiceManager.platform_input_stream import *
#from ServiceManager.platform_output_stream import *
#from gateway_input_stream import *
#from gateway_output_stream import *

class DistanceAlarmService():
    def __init__(self, emergency_end, critical_end):
        self.em_end = int(emergency_end)
        self.cr_end = int(critical_end)


    def input_data_cb(self, ch, method, properties, input_data):
        if not isinstance(input, str):
            input_data = input_data.decode()

        data = json.loads(input_data)

        # DISTANCE_SENSOR data is received
        distance = int(data["body"])
        if distance < self.em_end:
            print (f"EMERGENCY_STOP!!! {distance}")
        elif distance < self.cr_end:
            print (f"CRITICAL!!! {distance}")
        else:
            print (f"ALL FINE!!! {distance}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--service_id", default="-1")
    parser.add_argument("--run_on_gateway", default="no")
    parser.add_argument("--limits", default="100,200")

    (args, unknown) = parser.parse_known_args()

    emergency_end, critical_end = args.limits.split(',')
    distance_alarm_service = DistanceAlarmService(emergency_end, critical_end)

    sensor_type = "DISTANCE_SENSOR"

    if args.run_on_gateway == "no":
        input_stream = PlatformInputStream()
        input_stream.service_register_request(args.service_id, sensor_type, "default_rate", ["127.0.0.1:4445"])
        input_stream.recv_input_content(args.service_id, distance_alarm_service.input_data_cb)
