import sys

from pathlib import Path
home = str(Path.home())
path = home+'/Platform/'

sys.path.insert (0, path)

import argparse
import json

from ServiceManager.platform_input_stream import *
from ServiceManager.platform_output_stream import *
#from gateway_input_stream import *
#from gateway_output_stream import *

class DistanceAlarmService:
    def __init__(self, service_id, emergency_end, critical_end, run_on_gateway):
        self.service_id = service_id
        self.em_end = int(emergency_end)
        self.cr_end = int(critical_end)
        self.run_on_gateway = run_on_gateway


    def input_data_cb(self, ch, method, properties, input_data):
        if not isinstance(input_data, str):
            input_data = input_data.decode()

        data = json.loads(input_data)

        # DISTANCE_SENSOR data is received
        distance = int(data["content"])
        if distance < self.em_end:
            msg = f"EMERGENCY_STOP!!! {distance}"
        elif distance < self.cr_end:
            msg = f"CRITICAL!!! {distance}"
        else:
            msg = f"ALL FINE!!! {distance}"

        if self.run_on_gateway == "no":
            output_stream = PlatformOutputStream()
            output_stream.service_output_send(self.service_id, msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--service_id", default="-1")
    parser.add_argument("--run_on_gateway", default="no")
    parser.add_argument("--limits", default="100,200")
    parser.add_argument("--is_first_instance", default="no")

    (args, unknown) = parser.parse_known_args()

    emergency_end, critical_end = args.limits.split(',')
    distance_alarm_service = DistanceAlarmService(args.service_id, emergency_end, critical_end, args.run_on_gateway)

    sensor_name = "DISTANCE_SENSOR"


    if args.run_on_gateway == "no":
        input_stream = PlatformInputStream()

        if args.is_first_instance == "yes":
            input_stream.service_register_request(args.service_id, sensor_name, "default_rate")

        input_stream.service_recv_input_request(args.service_id, distance_alarm_service.input_data_cb)
