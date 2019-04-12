from mailbox import gmail

class EmergencyNotificationService:
    def __int__(self):
        pass
    
    def emergency_action_email(self, receiver_file_path, from_sensor):
        dist = get_distance(from_sensor)
        if dist < 200:
            G = gmail()
            sender_email = "sender_email"  # Enter your address
            sender_password = "sender_password"
            # receiver_email_list = ["receiver_email_list1", "receiver_email_list2"]  # Enter receiver address
            receiver_email_list = self.get_receiver_list(receiver_file_path)
            message = "Hi there I am testing email using python script."
            subject = "EMAIL TEST"
            G.send_email(sender_email, sender_password, receiver_email_list, message, subject)

    def get_receiver_list(self, receiver_file_path):
        return []#list


if __name__ == "__main__":
    emergency_notification_service = EmergencyNotificationService()
    emergency_notification_service.emergency_action_email()