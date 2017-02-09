from flask import Flask, request, render_template
from flask import make_response
import pymysql, draw
import nonogram, random, database
from flask.ext.mysql import MySQL
from flask.ext.flask_bcrypt import Bcrypt
import ast

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
	conn = mysql.connect()
	puzzles = '<div id="puzzles">{0}</div>'
	for puzzle in database.get_all_puzzles(conn):
		data = ast.literal_eval(puzzle[2])
		width = puzzle[3]
		height = puzzle[4]
		puzz_id = puzzle[0]
		puzzles = puzzles.format(draw.puzzle_prev(puzz_id, data, width, height) + '{0}')
	puzzles.format('')
	return render_template("solve.html",puzzles=puzzles)

@app.route('/solve/<puzz_id>')
def solve_env(puzz_id):
	conn = mysql.connect()
	puzz_info = database.get_puzzle_with_id(puzz_id, conn)
	data = ast.literal_eval(puzz_info[0])
	width = puzz_info[1]
	height = puzz_info[2]
	return render_template("solve_env.html", puzzles=draw.puzz_temp(data, width, height))

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
