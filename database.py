import time

def test(conn):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test (testdata) VALUES (\'{0}\');".format("banana"))
    conn.commit()

def create_user(conn, username, name, dob, password, email, salt):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, dob, username, password, salt, email) VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\')".format(name, dob, username, password, salt, email))
    conn.commit()

def check_login(conn, username, password, bcrypt):
    cursor = conn.cursor()
    cursor.execute("SELECT password, salt, name FROM users WHERE username=\'{0}\';".format(username))
    user = cursor.fetchone()
    salt = user[1]
    pswd = password + salt
    bcrypt.check_password_hash(user[0], pswd)
    return user[2]

def submit_new_puzzle(conn, authorID, title, template, answer, width, height):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO puzzles (authorID, title, template, answer, width, height) VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', {4}, {5})".format(authorID, title, template, answer, width, height))
    conn.commit()

def add_cookie(conn, cookie, username):
    cursor = conn.cursor()
    expire = time.time() + 3600
    cursor.execute("SELECT usersID FROM users WHERE username=\'{0}\';".format(username))
    userID = cursor.fetchone()[0]
    cursor.execute("INSERT INTO cookies (cookie, usersID, expiration_date) VALUES (\'{0}\', {1}, {2})".format(cookie, userID, expire))
    conn.commit()

def getuserID(conn, cookie):
    cursor = conn.cursor()
    cursor.execute("SELECT usersID, expiration_date FROM cookies WHERE cookie=\'{0}\';".format(cookie))
    result = cursor.fetchone()
    userID = result[0]
    expire = float(result[1])
    if (expire - time.time()) >= 0:
        expired = False
        print('false')
    else:
        expired = True
        print('true')
    return expired, userID

def get_all_puzzles(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT puzzleID, authorID, template, width, height FROM puzzles")
    result = cursor.fetchall()
    return result
