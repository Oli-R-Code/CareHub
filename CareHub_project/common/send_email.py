import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .database import get_admin_emails, get_user_email

def send_email(subject, body, to_email):
    from_email = "your_email@example.com"  # Replace with your email
    password = "your_password"  # Replace with your email password or app password
    
    # Set up the server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    
    # Log in to the server
    server.login(from_email, password)
    
    # Create the email
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    
    # Send the email
    server.sendmail(from_email, to_email, msg.as_string())
    
    # Disconnect from the server
    server.quit()

def notify_admin_of_pending_request(appointment_details):
    admin_emails = get_admin_emails()  # Fetch all admin emails dynamically from DB
    if not admin_emails:
        print("No admin emails found.")
        return

    subject = "New Appointment Request Pending"
    body = (
        f"A new appointment request has been made.\n\n"
        f"Details:\n"
        f"Doctor: {appointment_details['doctor_id']}\n"
        f"Date: {appointment_details['date']}\n"
        f"Time: {appointment_details['time']}\n"
        f"Status: Pending"
    )

    for email in admin_emails:
        send_email(subject, body, email)
        
def notify_user_of_appointment_status(userID, status):
    user_email = get_user_email(userID)  # Fetch user email dynamically from DB
    subject = "Your Appointment Request Status"
    body = f"Your appointment request has been {status}.\n\nStatus: {status}"
    send_email(subject, body, user_email)

if __name__ == "__main__":
    pass