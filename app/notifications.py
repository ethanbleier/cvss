import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class NotificationSystem:
    def __init__(self, sender_email, sender_password, recipient_email):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email

    def send_email(self, subject, body):
        try:
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = self.recipient_email
            message['Subject'] = subject

            message.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print("Notification email sent successfully")
        except Exception as e:
            print(f"Error sending notification email: {e}")

def main():
    # Example usage
    sender_email = "motiondetection555.system@gmail.com"
    sender_password = ""  # Use an app password for Gmail
    recipient_email = ""

    notification_system = NotificationSystem(sender_email, sender_password, recipient_email)
    notification_system.send_email("Motion Detected", "Motion has been detected in your monitored area.")

if __name__ == "__main__":
    main()
