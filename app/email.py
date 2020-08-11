import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app import app
from datetime import date
from flask import render_template
from threading import Thread


def convert_content_to_html(content):
    html = []
    html.append("<html><body><p>")
    for line in content: 
        html.append(str(line))
        html.append("<br>")
    
    html.append("</p></body></html>")
    html = "".join(html)
    return html

def send_email(title, recipient, text_body, html_body):
    #today = str(date.today().strftime('%Y-%m-%d'))
    me = app.config["MAIL_USERNAME"]
    my_password = app.config["MAIL_PASSWORD"]
    you = recipient

    msg = MIMEMultipart('alternative')
    msg['Subject'] = title #"Food at dining halls on " + today
    msg['From'] = me
    msg['To'] = you
    msg.attach(MIMEText(html_body, 'html'))
    msg.attach(MIMEText(text_body, 'plain'))

    # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # uncomment if interested in the actual smtp conversation
    # s.set_debuglevel(1)
    # do the smtp auth; sends ehlo if it hasn't been sent already
    s.login(me, my_password)
    s.sendmail(me, you, msg.as_string())
    s.quit()

def make_send_async_email(title, recipient, text_body, html_body):
    #today = str(date.today().strftime('%Y-%m-%d'))
    me = app.config["MAIL_USERNAME"]
    my_password = app.config["MAIL_PASSWORD"]
    you = recipient

    msg = MIMEMultipart('alternative')
    msg['Subject'] = title #"Food at dining halls on " + today
    msg['From'] = me
    msg['To'] = you
    msg.attach(MIMEText(html_body, 'html'))
    msg.attach(MIMEText(text_body, 'plain'))
    Thread(target=send_async_email, args=(app, msg, recipient)).start()

    

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    make_send_async_email(title='[Dining hall App] Reset Your Password',
                recipient=user.email,
                text_body=render_template('email/reset_password.txt',
                                          user=user, token=token),
                html_body=render_template('email/reset_password.html',
                                          user=user, token=token))

def send_async_email(app, msg, recipient):
    with app.app_context():
        me = app.config["MAIL_USERNAME"]
        my_password = app.config["MAIL_PASSWORD"]
        you = recipient
        # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # uncomment if interested in the actual smtp conversation
        # s.set_debuglevel(1)
        # do the smtp auth; sends ehlo if it hasn't been sent already
        s.login(me, my_password)
        s.sendmail(me, you, msg.as_string())
        s.quit()
        #assert(0)