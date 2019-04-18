import sys

from pathlib import Path
home = str(Path.home())
path = home+'/Platform/'

sys.path.insert (0, path)

import argparse
import json

from ServiceManager.platform_input_stream import *
from mailbox import gmail

class EmergencyNotificationService:
    def __init__(self, service_id, emergency_distance_threshold, sender_email, sender_password, receiver_email_list):
        self.service_id = service_id
        self.emergency_distance_threshold = int(emergency_distance_threshold)
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email_list = receiver_email_list

    def input_data_cb(self, ch, method, properties, input_data):
        if not isinstance(input, str):
            input_data = input_data.decode()

        data = json.loads(input_data)

        # DISTANCE_SENSOR data is received
        distance = int(data["content"])
    
        #print (f"EmergNotifService received distance: {distance}")
        if distance < self.emergency_distance_threshold:
            print ("Sending emails..")

            # send output to PlatformOutputStream, so that 200 emails could be sent
            G = gmail()
            message = "Distance: " + str(distance) + ", immediate action needed. "
            subject = "EMERGENCY NOTIFICATION SERVICE"
            G.send_email(self.sender_email, self.sender_password, self.receiver_email_list, message, subject)

    #def get_receiver_list(self, receiver_file_path):
    #    return []#list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--service_id", default="-1")
    parser.add_argument("--run_on_gateway", default="no")
    parser.add_argument("--limit", default="200")
    parser.add_argument("--sender_email", default="rajatverma00009@gmail.com")
    #parser.add_argument("--sender_email", default="bhavi.dhingra@gmail.com")
    parser.add_argument("--sender_password", default="rj.gmail@910")
    parser.add_argument("--receiver_email_list", default='ravi.jakhania@students.iiit.ac.in')


    (args, unknown) = parser.parse_known_args()
    print(args.receiver_email_list)
    recv_list = args.receiver_email_list.split(',')
    print(type(recv_list))
    print(recv_list)

    emergency_notification_service = EmergencyNotificationService(args.service_id, args.limit, args.sender_email, args.sender_password, recv_list)

    sensor_name = "DISTANCE_SENSOR"

    if args.run_on_gateway == "no":
        input_stream = PlatformInputStream()

        input_stream.service_register_request(args.service_id, sensor_name, "default_rate")
        input_stream.service_recv_input_request(args.service_id, emergency_notification_service.input_data_cb)
