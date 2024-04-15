from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)

# Configure email settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'abdulwahid72009@gmail.com'
app.config['MAIL_PASSWORD'] = 'vtis kxde yadk duls'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SECRET_KEY'] = "secret"

# Initialize Flask-Mail
mail = Mail(app)

s = URLSafeTimedSerializer(app.config["SECRET_KEY"])

# List of domains to deny
DENIED_DOMAINS = ["yahoo.com"]

# Function to check if email is private
def is_private_email(email):
    domain = email.split('@')[-1]
    return domain in DENIED_DOMAINS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        token = s.dumps(email, salt='email-confirmation-key')

        confirmation_link = url_for('confirm_email', token=token, _external=True)
        msg = Message('Confirmation Email', sender='abdulwahid72009@gmail.com', recipients=[email])
        msg.body = f"Click the link to confirm your email: {confirmation_link}"
        mail.send(msg)

        if is_private_email(email):
            return "Sorry, private email domains are not allowed."

        return redirect(url_for('thank_you'))

    return render_template('index.html')

@app.route('/thank-you')
def thank_you():
    return "Thank you for submitting the form. Check your email for confirmation."

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirmation-key', max_age=60)
    except Exception as err:
        return "<h1>LINK EXPIRED</h1>"
    return "<h1>Confirmation Done</h1>"

if __name__ == '__main__':
    app.run(debug=True)
