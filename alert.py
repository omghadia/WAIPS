import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import requests

def send_alert(input_text, attacker_ip, user_agent):
    sender_email = "kamradhruv0@gmail.com"
    receiver_email = "om.ghadia@somaiya.edu"
    password = "pfve ifrn rjae nuse"
    
    subject = "Alert: Malicious Activity Detected on Website"
    body = f"""
    <html>
    <body>
        <p style="color: red; font-size: 24px;">
            <strong>A possible attack has been detected on the website!</strong>
        </p>
        
        <p style="font-size: 18px; font-weight: bold;">
      Here are the details:
    </p>
        
<table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif;">
            <tr style="background-color: #f2f2f2;">
                <th style="text-align: left;">Detail</th>
                <th style="text-align: left;">Value</th>
            </tr>
            <tr>
                <td><strong>Timestamp:</strong></td>
                <td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
            </tr>
            <tr>
                <td><strong>Attacker's Input</strong></td>
                <td>{input_text}</td>
            </tr>
            <tr>
                <td><strong>Attacker's IP Address</strong></td>
                <td>{attacker_ip}</td>
            </tr>
            <tr>
                <td><strong>Location</strong></td>
                <td>{get_ip_location(attacker_ip)}</td>
            </tr>
            <tr>
                <td><strong>User Agent (Browser/OS)</strong></td>
                <td>{user_agent}</td>
            </tr>
        </table>

        <p>Please investigate this activity as soon as possible.</p>
    </body>
    </html>
    """
    
    # Create a MIMEText object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))
    
    try:
        # Establish a connection with the email server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Replace with your SMTP server details
        # server.starttls()  # Secure the connection
        server.login(sender_email, password)  # Login to the email server
        
        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
        
        # Close the connection
        server.quit()
        
        print("Alert sent to the administrator.")
    except Exception as e:
        print(f"Failed to send alert: {e}")

# Function to determine if the IP is private
def is_private_ip(ip):
    private_ip_ranges = [
        (167772160, 184549375),  # 10.0.0.0 - 10.255.255.255
        (2886729728, 2887778303),  # 172.16.0.0 - 172.31.255.255
        (3232235520, 3232301055),  # 192.168.0.0 - 192.168.255.255
    ]
    ip_as_int = int(''.join(f'{int(octet):08b}' for octet in ip.split('.')), 2)
    return any(lower <= ip_as_int <= upper for lower, upper in private_ip_ranges)

# Function to get location of the IP
def get_ip_location(ip):
    if is_private_ip(ip):
        return "Private IP, location not available."
    
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return f"{data['city']}, {data['regionName']}, {data['country']}"
        else:
            return "Location not found."
    except Exception as e:
        return "Could not retrieve location."