from flask import Flask, request, render_template
from flask import make_response
import pymysql, draw
import nonogram, random, database
from flask.ext.mysql import MySQL
from flask.ext.flask_bcrypt import Bcrypt
import ast


app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = "localhost"
app.config['MYSQL_DATABASE_USER'] = "nonogramuser"
app.config['MYSQL_DATABASE_PASSWORD'] = "puzzle"
app.config['MYSQL_DATABASE_DB'] = "nonogram"
bcrypt = Bcrypt(app)
mysql.init_app(app)

loggedin = '''<li><a href="/create">create</a></li>
			  <li><a href="/logout">logout</a></li>'''

loggedout = '''<li><a href="/login">login</a></li>
			   <li><a href="/sign-up">sign up</a></li>'''

def check_for_cookie():
	try:
		conn = mysql.connect()
		cookie = request.cookies.get('user')
		data = database.getuserID(conn, cookie)
		signedin = data[0]
		authorID = data[1]
		username = data[2]
		if signedin:
			return loggedin, authorID, username
		else:
			return loggedout, authorID, username
	except:
		return loggedout, None, None

def generate_salt():
	chars = '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-=[];\,./`!@£$%^&*()_+}{:|<>?~"`'
	salt = ''
	for i in range(32):
		salt += random.choice(chars)
	return salt

@app.route('/')
def index():
	return render_template('index.html', links=check_for_cookie()[0])

@app.route('/puzzle-gallery/<puzz_index>')
def get_puzzles(puzz_index):
	puzz_index = int(puzz_index)
	conn = mysql.connect()
	puzzles = database.get_all_puzzles(conn)
	puzz_temp = '<div id="puzzle">{0}</div>'
	puzzle = puzzles[puzz_index]
	data = ast.literal_eval(puzzle[2])
	width = puzzle[3]
	height = puzzle[4]
	puzz_id = puzzle[0]
	puzz_temp = puzz_temp.format(draw.puzzle_prev(puzz_index, len(puzzles), puzz_id, data, width, height))
	return render_template("solve.html",puzzle=puzz_temp, links=check_for_cookie()[0])

@app.route('/solve/<puzz_id>', methods=['POST', 'GET'])
def solve_env(puzz_id):
	if request.method == "POST":
		conn = mysql.connect()
		their_solution = request.form['data']
		puzz_info = database.get_puzzle_with_id(puzz_id, conn)
		solution = puzz_info[3]
		if their_solution == solution:
			mg = "<h1>Success</h1>"
		else:
			mg = "<h1>Sorry, Try Again</h1>"
		return render_template("result.html", msg=mg, links=check_for_cookie()[0])
	else:
		conn = mysql.connect()
		puzz_info = database.get_puzzle_with_id(puzz_id, conn)
		data = ast.literal_eval(puzz_info[0])
		width = puzz_info[1]
		height = puzz_info[2]
		thisrows = []
		newrow = []
		for cell in range(width):
			newrow.append(0)
		for row in range(height):
			thisrows.append(newrow)
		return render_template("solve_env.html", puzzles=draw.puzz_temp(data, width, height), links=check_for_cookie()[0], rows={'rows':thisrows})

@app.route('/create', methods=['POST', 'GET'])
def create():
	if request.method == 'POST':
		conn = mysql.connect()
		result = check_for_cookie()
		userID = result[1]
		title = request.form['title']
		width = int(request.form['width'])
		height = int(request.form['height'])
		answer = request.form['data']
		data = nonogram.process(request.form['data'], width, height)
		puzztemplate = nonogram.turn_into_template(data, width, height)
		database.submit_new_puzzle(conn, userID, title, puzztemplate, answer, width, height)
		mg = "Success! Thank you for your contribution."
		return render_template("result.html", msg=mg, links=check_for_cookie()[0])
	else:
		return render_template('create.html', links=check_for_cookie()[0])

@app.route('/login')
def login():
		return render_template('login.html', links=check_for_cookie()[0])

@app.route('/sign-up')
def signup():
		return render_template('signup.html', links=check_for_cookie()[0])

@app.route('/addrec', methods=['POST', 'GET'])
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
			return render_template("result.html",msg=msg, links=check_for_cookie()[0])

@app.route('/check_login', methods=['POST', 'GET'])
def check_login():
	if request.method == 'POST':
		try:
			unm = request.form['unm']
			pswd = request.form['pswd']
			conn = mysql.connect()
			cookie = generate_salt()
			mg = "Welcome " + database.check_login(conn, unm, pswd, bcrypt)
			database.add_cookie(conn, cookie, unm)
			response = make_response(render_template("result.html",msg = mg, links=loggedin))
			response.set_cookie('user', cookie)
		except NameError:
			mg = "That password is incorrect."
			response = make_response(render_template("result.html",msg = mg, links=check_for_cookie()[0]))
		except TypeError:
			mg = "That username does not exist."
			response = make_response(render_template("result.html",msg = mg, links=check_for_cookie()[0]))
		finally:
			conn.rollback()
			return response

@app.route('/logout')
def log_out():
	conn = mysql.connect()
	cookie = request.cookies.get('user')
	database.log_out_of_site(conn, cookie)
	msg = "<h1>Success</h1> <p>You've been successfully logged out.</p>"
	return render_template("result.html", msg=msg, links=check_for_cookie()[0])
