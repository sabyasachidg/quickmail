from flask import Flask, render_template, request
import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_emails', methods=['POST'])
def send_emails():
    # Get form data
    sender_name = request.form['senderName']
    sender_email = request.form['senderEmail']
    sender_password = request.form['senderPassword']
    email_subject = request.form['subject']
    email_body_file = request.files['bodyFile']
    recipient_file = request.files['recipientFile']

    # Save files
    email_body_file.save('email_body.txt')
    recipient_file.save('recipient_list.csv')

    # List of Recipients
    recipient_list = []

    # Reading CSV file containing recipients' information
    with open('recipient_list.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            recipient_list.append(row[0])

    # Reading email body from file
    with open('email_body.txt', 'r') as file:
        email_body = file.read()

    # Connecting to the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Looping through the recipient list and sending the email
    for recipient in recipient_list:
        # Setting up email components
        message = MIMEMultipart()
        message['From'] = f'{sender_name} <{sender_email}>'
        message['To'] = recipient
        message['Subject'] = email_subject
        message.attach(MIMEText(email_body, 'plain'))
        
        # Sending the email
        server.sendmail(sender_email, recipient, message.as_string())

        time.sleep(3)
        
    # Closing the SMTP server connection
    server.quit()

    return 'Emails sent successfully!'

if __name__ == '__main__':
    app.run(debug=True)
