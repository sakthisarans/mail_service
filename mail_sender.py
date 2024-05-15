from flask import Flask,request,json
import smtplib,datetime
import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app,resources={r'/sendemail':{"origins":["http://127.0.0.1:5500/",
                                             "http://www.sakthisaran.site",
                                             "https://www.sakthisaran.site",
                                             "http://sakthisaran.site",
                                             "https://sakthisaran.site"]}})
def mailHandler(name,email,subject,body):
    smtp_server = smtplib.SMTP(config.smtp_server,config.smtp_port)
    smtp_server.starttls()
    smtp_server.login(config.sender_add, config.password)
    message = MIMEMultipart('alternative')
    message['Subject'] = "Email From Portfolio"
    message['From'] = config.sender_add
    message['To'] = config.receiver_add

    html=f'''<!DOCTYPE html>
<html>
<head>
    <title>Email Details</title>
</head>
<body>
    <table border="1">
        <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Subject</th>
            <th>Message</th>
            <th>Time</th>
        </tr>
        <tr>
            <td>{name}</td>
            <td>{email}</td>
            <td>{subject}</td>
            <td>{body}</td>
            <td>{datetime.datetime.now()}</td>
        </tr>
    </table>
</body>
</html>
'''
    messagetosend = MIMEText(html, 'html')
    message.attach(messagetosend)
    smtp_server.sendmail(config.sender_add, config.receiver_add, message.as_string())
    smtp_server.quit()
    return ""

@app.route('/ping', methods=['GET'])
def ping():
    return "OK",200

@app.route('/sendemail', methods=['POST'])
@cross_origin()
def send_email():
    try:
        data = request.get_json()
        name=data['name']
        email=data['email']
        subject=data['subject']
        content=data['body']
        mailHandler(name=name,subject=subject,email=email,body=content)
        return "mail sent",200
    except:
        return "Bad Request",400
    
app.run (port=80,host="0.0.0.0")









