from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage
import csv

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<page_name>')
def works(page_name='index.html'):
    return render_template(page_name)


@app.route('/thanks.html')
def thanks(data):
    emailing(data)
    writing(data)
    return render_template('thanks.html', name=data)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        return thanks(data)
    else:
        return 'Oops, something went wrong!\nTry again later'


def emailing(data):
    email = EmailMessage()
    email['from'] = data['name']
    sub = f"{data['message']}\n\nEmail: {data['email']}"
    email['subject'] = data['subject']
    email['to'] = 'devangsharmadj@gmail.com'
    email.set_content(sub)

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('zerotomasterydj@gmail.com', 'NDDGisgr8!')
        smtp.send_message(email)


def writing(data):
    name = data['name']
    subject = data['subject']
    message = data['message']
    email = data['email']
    with open('database.csv', 'a') as db:
        writer = csv.writer(db)
        writer.writerow([name, email, subject, message])
