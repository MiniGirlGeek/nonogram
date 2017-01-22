from flask import Flask, request, render_template
from flask import make_response
import pymysql
import nonogram, random, database
from flask.ext.mysql import MySQL
from flask.ext.flask_bcrypt import Bcrypt

def generate_salt():
	chars = '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-=[];\,./`!@£$%^&*()_+}{:|<>?~"`'
	salt = ''
	for i in range(32):
		salt += random.choice(chars)
	return salt

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = "localhost"
app.config['MYSQL_DATABASE_USER'] = "nonogramuser"
app.config['MYSQL_DATABASE_PASSWORD'] = "puzzle"
app.config['MYSQL_DATABASE_DB'] = "nonogram"
bcrypt = Bcrypt(app)
mysql.init_app(app)

@app.route('/')
def index():
		return render_template('index.html')

@app.route('/solve')
def solve():
		return render_template('solve.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
	if request.method == 'POST':
		try:
			conn = mysql.connect()
			cookie = request.cookies.get('user')
			data = database.getuserID(conn, cookie)
			expired = data[0]
			authorID = data[1]
		except:
			mg = "Please log in."
			return render_template("result.html",msg=mg)
		if not expired:
			authorID = 5
			title = request.form['title']
			width = int(request.form['width'])
			height = int(request.form['height'])
			answer = request.form['data']
			data = nonogram.process(request.form['data'], width, height)
			puzztemplate = nonogram.turn_into_template(data, width, height)
			database.submit_new_puzzle(conn, authorID, title, puzztemplate, answer, width, height)
			mg = "Success! Thank you for your contribution."
			return render_template("result.html",msg=mg)
		else:
			mg = 'Your session has expired, please log in again.'
			return render_template("result.html",msg=mg)
			#return render_template('puzzle.html', puzzle=nonogram.populate_grid(request))
	else:
		return render_template('create.html')

@app.route('/login')
def login():
		return render_template('login.html')

@app.route('/sign-up')
def signup():
		return render_template('signup.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
	'''runs the SQL to make a new user, then renders a page
	   based upon whether it was successful or not'''
	if request.method == 'POST':
		try:
			conn = mysql.connect()
			nm = request.form['nm']
			unm = request.form['unm']
			pswd = request.form['pswd']
			dob = request.form['dob']
			email = request.form['email']
			salt = generate_salt()
			password = bcrypt.generate_password_hash(pswd + salt).decode('utf-8')
			database.create_user(conn, unm, nm, dob, password, email, salt)
			msg = "Sucess!"
		except pymysql.err.IntegrityError:
			msg = "Sorry that username is already taken! Please try again."
		finally:
			conn.close()
			return  render_template("result.html",msg = msg)



@app.route('/check_login',methods = ['POST', 'GET'])
def check_login():
	if request.method == 'POST':
		try:
			unm = request.form['unm']
			pswd = request.form['pswd']
			conn = mysql.connect()
			cookie = generate_salt()
			mg = "Welcome " + database.check_login(conn, unm, pswd, bcrypt)
			response = make_response(render_template("result.html",msg = mg))
			database.add_cookie(conn, cookie, unm)
			response.set_cookie('user', cookie)
		except TypeError:
			mg = "That username does not exist."
			response = make_response(render_template("result.html",msg = mg))
			conn.rollback()
		finally:
			return response
