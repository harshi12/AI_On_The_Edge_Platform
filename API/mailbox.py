# # Python code to illustrate Sending mail from  
# # your Gmail account  

import smtplib, ssl
class gmail:
   #https://www.google.com/settings/security/lesssecureapps
   port = 465  # For SSL
   smtp_server = "smtp.gmail.com"

   def send_email(self, sender_email, sender_password, receiver_email_list, message = '', subject = ''):
      msg = "Subject: " + subject + "\n\n" + message

      context = ssl.create_default_context()
      with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
         try: 
            server.login(sender_email, passwsender_passwordord)
            print("loggedin")
            for receiver_email in receiver_email_list:
               server.sendmail(sender_email, receiver_email, msg)
         except:
            print("Error sending mail, to set insecure apps to use gmail service go to https://www.google.com/settings/security/lesssecureapps.")