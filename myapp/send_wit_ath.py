import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from .qr_creation import generate_qr_code

def send_email_ath(to,name,user,event):
    from_addr = 'no-replay@crimson-dragon.com'
    to_addr = to
    subject = 'Registration Successful ..'

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
        <p>Welcome to our platform!, please follow the steps below:</p>
        <ol>
            <li>Download the QR code attached to this email.</li>
            <li>Your Q_r code will be verified at the event spot</li>
        </ol>
        <p>Click the button below to cancel your registration</p>
        <a href="link_to_download_qr_code" style="text-decoration: none;">
            <button style="background-color: #3498db; color: #fff; padding: 10px; border: none; border-radius: 4px; cursor: pointer;">cancel registration</button>
        </a>
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

    # Attach image
    image_filename = generate_qr_code(user,event)
    with open(image_filename, 'rb') as image_file:
        image_attachment = MIMEImage(image_file.read(), name=basename(image_filename))
        image_attachment.add_header('Content-ID', '<image_attachment>')
        image_attachment.add_header('Content-Disposition', 'inline', filename=basename(image_filename))
        msg.attach(image_attachment)

    server = smtplib.SMTP('smtp-relay.brevo.com', 587)
    server.login('ramachandraudupa2004@gmail.com', '8sNWDXfyM6mY5H3U')
    server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])
    server.quit()
    return True
