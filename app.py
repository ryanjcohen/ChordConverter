from flask import Flask
from flask import render_template
app = Flask(__name__)
app.static_folder='static'
   
@app.route("/")
def converter():
	return render_template("converter.html")