########################################################################################
# This file contains all the fuctions to do with passing data to and from the database #
########################################################################################

import time

def test(conn):
	'''A test fuction, if I need to check my connection to the database is working.'''
	cursor = conn.cursor()
	cursor.execute("INSERT INTO test (testdata) VALUES (\'{0}\');".format("banana"))
	conn.commit()

def create_user(conn, username, name, dob, password, email, salt):
	'''Takes data about a user and inserts it into a new record in the users table.'''
	cursor = conn.cursor()
	cursor.execute("INSERT INTO users (name, dob, username, password, salt, email) VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\')".format(name, dob, username, password, salt, email))
	conn.commit()

def check_login(conn, username, password, bcrypt):
	'''Retrieves the salt associated with that username from the database,
	   and then checks that if it hashes the password that it gets the same
	   result as the stored password. If the results are different it raises an
	   error, if not it returns their name.'''
	cursor = conn.cursor()
	cursor.execute("SELECT password, salt, name FROM users WHERE username=\'{0}\';".format(username))
	user = cursor.fetchone()
	salt = user[1]
	pswd = password + salt
	valid = bcrypt.check_password_hash(user[0], pswd)
	if not valid:
		raise NameError('invalid password')
	return user[2]

def submit_new_puzzle(conn, authorID, title, template, answer, width, height):
	'''Creates a new record in the puzzles table using the data passed in'''
	cursor = conn.cursor()
	cursor.execute("INSERT INTO puzzles (authorID, title, template, answer, width, height) VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', {4}, {5})".format(authorID, title, template, answer, width, height))
	conn.commit()

def add_cookie(conn, cookie, username):
	'''Adds a new record to the cookies table. The expiration_date is set to an
	   hour from now. This means that users will automatically be logged out after
	   this time. Each cookie is associated with the userID of the username entered'''
	cursor = conn.cursor()
	expire = time.time() + 3600 #3600 is the time in seconds the cookie is valid for
	cursor.execute("SELECT usersID FROM users WHERE username=\'{0}\';".format(username))
	userID = cursor.fetchone()[0]
	cursor.execute('''INSERT INTO cookies (cookie, usersID, expiration_date) 
		              VALUES (\'{0}\', {1}, {2})'''.format(cookie, userID, expire))
	conn.commit()

def getuserID(conn, cookie):
	'''Tries to get the userID, but also checks to see if the login cookie has
	expired'''
	cursor = conn.cursor()
	cursor.execute("SELECT usersID, expiration_date FROM cookies WHERE cookie=\'{0}\';".format(cookie))
	result = cursor.fetchone()
	userID = result[0]
	expire = float(result[1])
	cursor.execute("SELECT username FROM users WHERE usersID={0};".format(userID))
	username = cursor.fetchone()[0]
	if (expire - time.time()) >= 0:
		signedin = True
	else:
		signedin = False
	return signedin, userID, username

def get_all_puzzles(conn):
	'''Returns a list of all the puzzles in the database, and all the data required
	to draw it's preview frame'''
	cursor = conn.cursor()
	cursor.execute("SELECT puzzleID, authorID, template, width, height FROM puzzles")
	result = cursor.fetchall()
	return result

def get_puzzle_with_id(puzz_id, conn):
	'''Returns the information required to draw a puzzle with the specified ID.'''
	cursor = conn.cursor()
	cursor.execute("SELECT template, width, height, answer FROM puzzles WHERE puzzleid={0};".format(puzz_id))
	result = cursor.fetchone()
	return result

def log_out_of_site(conn, cookie):
	'''Update's the user's cookie's expiration_date to the current time, logging them out'''
	cursor = conn.cursor()
	cursor.execute("UPDATE cookies SET expiration_date={0} WHERE cookie=\'{1}\';".format(time.time(), cookie))
	conn.commit()
