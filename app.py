from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from passlib.hash import sha256_crypt
from functools import wraps


app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'eripsa141'
app.config['MYSQL_DB'] = 'plantapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#init MySQL
mysql = MySQL(app)


app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
Bootstrap = Bootstrap(app)

	#Login Form Class
class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=25)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
	remember = BooleanField('remember me')

	#Register Form Class
class RegisterForm(FlaskForm):
	name = StringField('name', validators=[InputRequired(), Length(min=3, max=50)])
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=25)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

	#Index
@app.route('/')
def index():
	return render_template('home.html')


	#User Login 
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		username = request.form['username']
		password_candidate = request.form['password']
				
		#return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

		#Create Cursor
		cur = mysql.connection.cursor()

		#Get user by username
		result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

		if result > 0:
			#Get stored hash/password
			data = cur.fetchone()
			password = data['password']

			#Compare the Passwords
			if sha256_crypt.verify(password_candidate, password):
				#password Passed
				session['logged in'] = True
				session['username'] = username

				flash('You are now logged in', 'success')
				return redirect(url_for('dashboard'))
				
			else:
				error = 'Invalid login'
				return render_template('login.html', error=error, form=form)

			#close connection
			cur.close()
		else:
			error = 'Username not found'
			return render_template('login.html', error=error, form=form)


	return render_template('login.html', form=form)
	

	#User Registration
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = RegisterForm()

	if form.validate_on_submit():
		name = form.name.data
		username = form.username.data
		email = form.email.data
		password = sha256_crypt.encrypt(str(form.password.data))

		# Create the Cursor
		cur = mysql.connection.cursor()

		#execute query
		cur.execute("INSERT INTO users(name,username, email, password) VALUES(%s,%s, %s, %s)", (name, username, email, password))

		#commit to DB
		mysql.connection.commit()

		#close connection
		cur.close()

		flash('You are now registerd and can login', 'success')

		redirect(url_for('index'))
		#return '<h1>' + form.username.data + ' ' + form.password.data + ' ' + form.email.data + '</h1>'

	return render_template ('signup.html', form=form)

#check if user logged in 
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

#Logout
@app.route('/logout')
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login'))


@app.route('/About')
def about():
	return render_template('about.html')

#shopping Cart app	
@app.route('/ShoppingCart')
def PlantApp():
	return render_template('ShoppingCart.html')

#Contact Form
@app.route('/contactForm')
def ContactForm():
	return render_template('contactForm.html')

#show Cart before submitting
@app.route('/Show-cart')
def showCart():
	return render_template('showCart.html')

#submitted cart
@app.route('/Submit-Cart')
def submitCart():
	return render_template('submitCart.html')

#dashboard
@app.route('/Dashboard')
@is_logged_in
def dashboard():
	return render_template('dashboard.html')

if __name__ == "__main__":
	app.run(debug=True)
	