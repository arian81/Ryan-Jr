import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(email, token):
    port = 465
    smtp_server_domain_name = "smtp.gmail.com"
    sender_mail = "1xc3.verify@gmail.com"
    password = "daxjvhxyaguxxace"

    ssl_context = ssl.create_default_context()
    service = smtplib.SMTP_SSL(
        smtp_server_domain_name, port, context=ssl_context)
    service.login(sender_mail, password)

    mail = MIMEMultipart('alternative')
    mail['Subject'] = '1XC3 Discord Server Email Verification'
    mail['From'] = sender_mail
    mail['To'] = email
    username = email.split("@")[0]

    text_template = f"""
        Hey there {username},\n
        You have requested for your email to be verified through our discord
        bot. Use the code below to verify your account\n
        {token}
                    """
    html_template = f"""
        <div style="background-color: #5cdb95; border-radius: 0.8em; padding: 2em">
            <div style="text-align: center">
                <h3
                    style="
                        padding: 0 2em;
                        color: #05386b;
                        font-family: Helvetica, sans-serif;
                    "
                >
                    Hey there {username},
                </h3>
                <p
                    style="
                        padding: 0em 2em 2em 3em;
                        color: #05386b;
                        font-family: Helvetica, sans-serif;
                    "
                >
                    You have requested for your email to be verified through our discord
                    bot. Use the code below to verify your account
                </p>
            </div>

            <div
                style="
                    background-color: #edf5e1;
                    border-radius: 4em;
                    margin: auto;
                    overflow-wrap: break-word;
                "
            >
                <p style="padding: 2em; color: #379683;text-align:center;">
                    {token}
                </p>
            </div>
        </div>
                """

    html_content = MIMEText(
        html_template, 'html')
    text_content = MIMEText(
        text_template, 'plain')

    mail.attach(text_content)
    mail.attach(html_content)

    service.sendmail(sender_mail, email, mail.as_string())

    service.quit()
