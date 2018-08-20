from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from passlib.hash import sha256_crypt
from functools32 import wraps
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)


#configure SQLAlchemy to connect to the db

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:eripsa141@localhost/plantapp'
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
Bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
admin = Admin(app) #setting up flask-admin instance of the app


#create Models

class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	username = db.Column(db.String(15), unique=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(80))

admin.add_view(ModelView(Users, db.session)) #adds the Users table to the admin console.

class Productcategories(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	category_name = db.Column(db.String(100))
	parent_category_id = db.Column(db.Integer)


admin.add_view(ModelView(Productcategories, db.session))

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	price = db.Column(db.Integer)
	parent_category_id = db.Column(db.Integer)

admin.add_view(ModelView(Product, db.session))

class productView(BaseView):
	myUser = session.query(Users).all()
	form_columns = ['name','price']
	@expose('/')
	def index(self):
		return self.render('admin/products.html', myUser=myUser)


admin.add_view(productView(name='Products and Services', endpoint='products'))

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
		#SQLAlchemy method
		username = request.form['username']
		password_candidate = request.form['password']
		user = Users.query.filter_by(username=form.username.data).first()
		if user: 
			password = user.password
			if sha256_crypt.verify(password_candidate, password):
				#password Passed
				session['logged in'] = True
				session['username'] = username

				flash('You are now logged in', 'success')
				return redirect(url_for('dashboard'));
				
			else:
				error = 'Invalid login'
				return render_template('login.html', error=error, form=form)
		else:
			error = 'Username not found'
			return render_template('login.html', error=error, form=form)


	return render_template('login.html', form=form)
	

	#User Registration
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = RegisterForm()

	if form.validate_on_submit():

		new_user = Users(
			name = form.name.data,
			username = form.username.data,
			email = form.email.data,
			password = sha256_crypt.encrypt(str(form.password.data))
		)
		db.session.add(new_user)
		db.session.commit()

		flash('You are now registerd and can login', 'success')

		redirect(url_for('index'))

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
	
