from mailbox import gmail

class EmergencyNotificationService:
    def __int__(self):
        dist = get_distance(from_sensor)
        if dist < 200:
            G = gmail()
            sender_email = "sender_email"  # Enter your address
            sender_password = "sender_password"
            receiver_email_list = ["receiver_email_list1", "receiver_email_list2"]  # Enter receiver address
            message = "Hi there I am testing email using python script."
            subject = "EMAIL TEST"
            G.send_email(sender_email, sender_password, receiver_email_list, message, subject)
