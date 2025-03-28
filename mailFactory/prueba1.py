import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import msal

# Azure App Configuration
client_id = '96ad03ca-af91-4bc2-9b8d-7743ac4841d8'
client_secret = "_st8Q~UvflNGqADhTPdbaBQfAcCTKu6ayVZbFcLV"
tenant_id = 'consumers'  # Use 'common' for personal Microsoft accounts

# Email Configuration
sender_email = 'marrondaniel20@gmail.com'
recipient_email = 'dmarron@unsa.edu.pe'
subject = 'Hello from Python'
message = 'This is an HTML email sent using OAuth2.'

# Acquire Access Token
authority = f'https://login.microsoftonline.com/{tenant_id}'
scope = ["https://graph.microsoft.com/SMTP.Send"]
app = msal.ConfidentialClientApplication(
    client_id=client_id,
    client_credential=client_secret,
    authority=authority
)
result = app.acquire_token_for_client(scopes=scope)

if 'access_token' not in result:
    print("Error acquiring token:", result.get('error_description', 'Unknown error'))
    exit()

access_token = result['access_token']

# Create Email Message
msg = MIMEMultipart('alternative')
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = subject

text = 'This is a plain text email.'
html = f'<html><body><h1>{message}</h1></body></html>'

msg.attach(MIMEText(text, 'plain'))
msg.attach(MIMEText(html, 'html'))

# SMTP Server Configuration
smtp_server = 'smtp.office365.com'
smtp_port = 587

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Authenticate using XOAUTH2
    auth_string = f'user={sender_email}\x01auth=Bearer {access_token}\x01\x01'
    auth_string = base64.b64encode(auth_string.encode()).decode()
    server.docmd('AUTH', 'XOAUTH2 ' + auth_string)

    server.sendmail(sender_email, recipient_email, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
finally:
    server.quit()