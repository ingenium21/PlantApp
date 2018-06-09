from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('home.html')
	
@app.route('/About')
def about():
	return render_template('about.html')
	
@app.route('/ShoppingCart')
def PlantApp():
	return render_template('ShoppingCart.html')

@app.route('/contactForm')
def ContactForm():
	return render_template('contactForm.html')

@app.route('/Submit-Cart')
def submitCart():
	return render_template('submitCart.html')

if __name__ == "__main__":
	app.run()
	
