import imaplib
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time

# Email account credentials
EMAIL_ADDRESS = 'rajpathak.er@gmail.com'
EMAIL_PASSWORD = 'dhro eqpo ofbz zudn'
SMTP_SERVER = 'imap.gmail.com'
SMTP_PORT = 993

# Function to read emails from the specified sender and subject
def read_emails():
    mail = imaplib.IMAP4_SSL(SMTP_SERVER, SMTP_PORT)
    mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    mail.select('inbox')

    # Search for emails from flow@shopify.com with the subject containing "Order Data V2O Sports Order #"
    status, response = mail.search(None, '(FROM "flow@shopify.com" SUBJECT "Order Data V2O Sports Order #")')
    email_ids = response[0].split()

    orders_to_process = []

    for e_id in email_ids:
        status, msg_data = mail.fetch(e_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        subject = msg['subject']
        if "Order Data V2O Sports Order #" in subject:
            order_number = subject.split('#')[-1]
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    if "Prescription type: Prescription - Distance - Single Vision" in body:
                        # Use your own email for testing
                        customer_email = 'rajpathak.freelancer@gmail.com'
                        orders_to_process.append((order_number, customer_email))

    mail.logout()
    return orders_to_process

# Function to send email
def send_email(order_number, customer_email):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = customer_email
    msg['Cc'] = EMAIL_ADDRESS
    msg['Subject'] = f"Regarding your Order #{order_number}"

    body = """\
    Thank you for your order! We will be ordering the lenses ASAP.
    As you have ordered varifocals or bifocals, we would benefit from understanding the relevant heights. To do this, we would request you send us a portrait style (front on) close up picture of your face wearing some glasses where your eyes are open and visible. A ‘selfie’ would work well. Please do send this asap as it will help us understand how to set the lenses.
    Please don’t hesitate with any questions and we look forward to your reply.
    Best regards,
    Tom
    Admin@v2ogroup.com
    """
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL_ADDRESS, [customer_email, EMAIL_ADDRESS], text)
    server.quit()

# Function to process new orders and send emails
def process_orders():
    orders_to_process = read_emails()
    for order_number, customer_email in orders_to_process:
        send_email(order_number, customer_email)

# Schedule the task to run every 45 minutes
schedule.every(45).minutes.do(process_orders)

while True:
    schedule.run_pending()
    time.sleep(1)