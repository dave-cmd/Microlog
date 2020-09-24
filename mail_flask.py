import os
from flask import Flask, render_template
from flask_mail import Mail, Message
import logging

logging.basicConfig(filename='sample.log',level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)

def create_app():
    
    with app.app_context():
        pass
    return app
    

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
app.config['MAX_EMAIL'] = 2
app.config['MAIL_SUPPRESS_SEND'] = False 
app.config['MAIL_ASCII_ATTACHMENTS'] = False


mail = Mail(app)



class People():
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname
        
        logging.info(f"{self.full_name} {self.email}")
        
    def __repr__(self):
        return f"{self.email}, {self.full_name}"
    
    @property
    def email(self):
        return f"{self.fname}.{self.lname}.mail.com"
    @property
    def full_name(self):
        return f"{self.fname} {self.lname}"
        





@app.route("/mailer")
def mailer():
    msg = Message('Manyiel', recipients=['kanjurus@yahoo.com', 'kanjurus30@gmail.com'])
    msg.html = '<h1>This is html Today<h1>'
    mail.send(msg)
    return "Message sent."

@app.route("/")
@app.route("/index")
def home():
    people = []
    a = People(fname='David', lname='Kanjuru')
    b = People(fname='Richard', lname='Mwai')
    people.append(a)
    people.append(b)
    
    print(os.environ.get('MAIL_USERNAME'))
    return render_template('home.html', people=people)

    


if __name__ == "__main__":
    app.run(debug=True)