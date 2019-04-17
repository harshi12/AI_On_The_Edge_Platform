import sys
sys.path.insert (0, '../')

import argparse
import json

from ServiceManager.platform_input_stream import *
from mailbox import gmail

class EmergencyNotificationService:
    def __init__(self, service_id, emergency_distance_threshold):
        self.service_id = service_id
        self.emergency_distance_threshold = int(emergency_distance_threshold)

    def input_data_cb(self, ch, method, properties, input_data):
        if not isinstance(input, str):
            input_data = input_data.decode()

        data = json.loads(input_data)

        # DISTANCE_SENSOR data is received
        distance = int(data["content"])
    
        print (f"EmergNotifService received distance: {distance}")
        if distance < self.emergency_distance_threshold:
            print ("Sending emails to 200 receipients!!")

            # send output to PlatformOutputStream, so that 200 emails could be sent

            #G = gmail()
            #sender_email = "sender_email"  # Enter your address
            #sender_password = "sender_password"
            # receiver_email_list = ["receiver_email_list1", "receiver_email_list2"]  # Enter receiver address
            #receiver_email_list = self.get_receiver_list(receiver_file_path)
            #message = "Hi there I am testing email using python script."
            #subject = "EMAIL TEST"
            #G.send_email(sender_email, sender_password, receiver_email_list, message, subject)

    #def get_receiver_list(self, receiver_file_path):
    #    return []#list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--service_id", default="-1")
    parser.add_argument("--run_on_gateway", default="no")
    parser.add_argument("--limit", default="200")

    (args, unknown) = parser.parse_known_args()

    emergency_notification_service = EmergencyNotificationService(args.service_id, args.limit)

    sensor_name = "DISTANCE_SENSOR"

    if args.run_on_gateway == "no":
        input_stream = PlatformInputStream()

        input_stream.service_register_request(args.service_id, sensor_name, "default_rate")
        input_stream.service_recv_input_request(args.service_id, emergency_notification_service.input_data_cb)
