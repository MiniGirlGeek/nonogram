from flask import Flask, request, render_template
import nonogram, sqlite3, random
from flask.ext.flask_bcrypt import Bcrypt

def generate_salt():
	chars = '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-=[];\,./`!@£$%^&*()_+}{:|<>?~"`'
	salt = ''
	for i in range(32):
		salt += random.choice(chars)
	return salt

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
		return render_template('index.html')

@app.route('/solve')
def solve():
		return render_template('solve.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
	if request.method == 'POST':
		return render_template('puzzle.html', puzzle=nonogram.populate_grid(request))
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
	if request.method == 'POST':
		try:
			nm = request.form['nm']
			unm = request.form['unm']
			salt = generate_salt()
			pswd = bcrypt.generate_password_hash(request.form['pswd'] + salt).decode('utf-8')
			dob = request.form['dob']

			with sqlite3.connect("nonogram/nonogram_database.db") as con:
				cur = con.cursor()
				cur.execute("INSERT INTO users (name,dob,username,password,salt) VALUES (?,?,?,?,?)",(nm,dob,unm,pswd,salt))
				con.commit()
				msg = "You have successfully created an account, please log in"
		except:
			con.rollback()
			msg = "please try again"

		finally:
			return render_template("result.html",msg = msg)
			con.close()

@app.route('/check_login',methods = ['POST', 'GET'])
def check_login():
	if request.method == 'POST':
		try:
			with sqlite3.connect("nonogram/nonogram_database.db") as con:
				unm = request.form['unm']
				cur = con.cursor()
				cur.execute("SELECT password, salt, name FROM users WHERE username=:who;", {'who':unm})
				user = cur.fetchone();
				salt = user[1]
				pswd = request.form['pswd'] + salt
				bcrypt.check_password_hash(user[0], pswd)
				msg = "Welcome " + user[2]
		except:
			con.rollback()
			msg = "error in insert operation"

		finally:
			return render_template("result.html",msg = msg)
			con.close()
