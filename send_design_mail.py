import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configuration import my_conf


def send_mail(title: str, html_message: str, image_objects: list):
    # Email configuration
    sender_email = my_conf['sender_email']
    sender_password = my_conf['sender_password']
    subject = title

    # SMTP server configuration (for Gmail)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    message = MIMEMultipart()
    message['From'] = sender_email
    message['Subject'] = subject

    for image in image_objects:
        message.attach(image)

    message.attach(MIMEText(html_message, 'html'))

    # make a mailing list by txt file
    with open('mailing_list.txt', 'r', encoding='utf-8') as f:
        all_recipients_emails = [mail.replace('\n', '') for mail in f.readlines() if '@' in mail]

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)

            # send a message for each in rhe list
            for mail in all_recipients_emails:
                message = MIMEMultipart()
                message['From'] = sender_email
                message['Subject'] = subject

                for image in image_objects:
                    message.attach(image)

                message.attach(MIMEText(html_message, 'html'))

                message['To'] = mail
                server.sendmail(sender_email, mail, message.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
