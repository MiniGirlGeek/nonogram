#################################################################################################
# This is the main python script that is run on the server, all other scripts are called by it. #
# It defines the behaviour of each page.                                                        #
#################################################################################################

#imports from flask libary and flask compatible libraries
from flask import Flask, request, render_template
from flask import make_response
import pymysql
from flask.ext.mysql import MySQL
from flask_bcrypt import Bcrypt

#imports from the python standard library
import ast, random

#imports from other python files I've written and are part of this application
import nonogram, random, database, draw

#setting up flask
app = Flask(__name__)
#setting up MySQL
mysql = MySQL()
#setting up the database credentials and getting the MySQL library to work with the flask libray
app.config['MYSQL_DATABASE_HOST'] = "localhost"
app.config['MYSQL_DATABASE_USER'] = "nonogramuser"
app.config['MYSQL_DATABASE_PASSWORD'] = "puzzle"
app.config['MYSQL_DATABASE_DB'] = "nonogram"
mysql.init_app(app)
#setting up the bcrpt library to work with flask
bcrypt = Bcrypt(app)

#links for check for cookie
loggedin = '''<li><a href="/create">create</a></li>
			  <li><a href="/logout">logout</a></li>'''

loggedout = '''<li><a href="/login">login</a></li>
			   <li><a href="/sign-up">sign up</a></li>'''

###############################
# Functions used within pages #
###############################

def check_for_cookie():
	'''Checks to see if a cookie has been set (and not expired), if it
	has it returns the links for a user that is logged in and the data
	associated with that cookie, if not it returns the links for logged
	out user'''
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
	'''generates a salt to add to passwords'''
	chars = '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-=[];\,./`!@£$%^&*()_+}{:|<>?~"`'
	salt = ''
	for i in range(32):
		salt += random.choice(chars)
	return salt

#######################
# Functions for pages #
#######################

@app.route('/')
def index():
	'''Defines the behaviour for the index page'''
	return render_template('index.html', links=check_for_cookie()[0])

@app.route('/puzzle-gallery/<puzz_index>')
def get_puzzles(puzz_index):
	'''Defines the behaviour for the puzzle gallery page.'''

	#retrieves the information about the puzzle specified by the URL
	puzz_index = int(puzz_index)
	conn = mysql.connect()
	puzzles = database.get_all_puzzles(conn)
	puzz_temp = '<div id="puzzle">{0}</div>'
	if len(puzzles) < puzz_index:
		error = '''<H1> Error </H1> <p> Sorry that puzzle doesn't exist, please use the buttons to navigate the puzzle gallery.'''
		return render_template("result.html", msg=error, links=check_for_cookie()[0])

	#reorganises the data
	puzzle = puzzles[puzz_index]
	data = ast.literal_eval(puzzle[2])
	width = puzzle[3]
	height = puzzle[4]
	puzz_id = puzzle[0]

	#generates the SVG prieview of that template
	puzz_temp = puzz_temp.format(draw.puzzle_prev(puzz_index, len(puzzles), puzz_id, data, width, height))
	return render_template("solve.html",puzzle=puzz_temp, links=check_for_cookie()[0])

@app.route('/solve/<puzz_id>', methods=['POST', 'GET'])
def solve_env(puzz_id):
	'''Defines the behaviour of the solve environment'''

	#Handles the POST method
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

	#Handles the initial loading of the page
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
	'''Defines the behaviour of the create page'''

	#Handles the POST method
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

	#Handles the initial loading of the page
	else:
		return render_template('create.html', links=check_for_cookie()[0])

@app.route('/login')
def login():
	'''Defines the behaviour of the login page'''
	return render_template('login.html', links=check_for_cookie()[0])

@app.route('/sign-up')
def signup():
	'''Defines the behaviour of the sign up page'''
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
			msg = "	success!"
		except pymysql.err.IntegrityError:
			msg = "Sorry that username is already taken! Please try again."
		finally:
			conn.close()
			return render_template("result.html",msg=msg, links=check_for_cookie()[0])

@app.route('/check_login', methods=['POST', 'GET'])
def check_login():
	'''Defines the behaviour of the chcek login page,
	   This page is called by the login page and is used to verify the users credentials'''
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
	'''Defines the behaviour of the logout page, the expirary time of the user cookie is set to the current time.'''
	conn = mysql.connect()
	cookie = request.cookies.get('user')
	database.log_out_of_site(conn, cookie)
	msg = "<h1>Success</h1> <p>You've been successfully logged out.</p>"
	return render_template("result.html", msg=msg, links=check_for_cookie()[0])
