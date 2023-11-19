import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def email_sender(to,name,message=None,subject=None):
    from_addr = 'no-replay@crimson-dragon.com'
    to_addr = to
    if message ==None:
        message = "Your registration is validated."
        subject = 'Validation Successful ..'
    # HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your Email Subject</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }

            .container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }

            .header {
                background-color: #3498db;
                color: #fff;
                text-align: center;
                padding: 20px;
            }

            .content {
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                margin-top: 20px;
            }

            .footer {
                text-align: center;
                margin-top: 20px;
                color: #777;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>SMVITM Bantakal</h1>
                <p>Connecting with you!</p>
            </div>
            <div class="content">
        <h2>Hello """
    s1=name
    s2 =""",</h2>
        <p>Welcome to our platform! </p>
        <h2>"""+message+"""</h2>
        <p>If you have any questions or need assistance, feel free to contact us.</p>
    </div>
            <div class="footer">
                <p>Thank you for choosing us!</p>
            </div>
        </div>
    </body>
    </html>
    """
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject

    # Attach HTML content
    body = MIMEText(html_content+s1+s2, 'html')
    msg.attach(body)
    server = smtplib.SMTP('smtp-relay.brevo.com', 587)
    server.login('ramachandraudupa2004@gmail.com', '8sNWDXfyM6mY5H3U')
    server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])
    server.quit()