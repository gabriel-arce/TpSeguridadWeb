from flask 	import Flask, render_template, session, redirect, url_for, escape, request

import bcrypt
import MySQLdb

ROUNDS = 10

USER_ID 		= 0
USER_NAME 		= 1
USER_USERNAME   = 2
USER_PASSWORD	= 3
USER_EMAIL		= 4

class ServerError(Exception): pass 

def loginForm(db, form):
	error = None

	try:
		usename 	= form['username'] 
		cursor		= db.query("SELECT COUNT(*) FROM tbl_users WHERE user_name = %s", [form['username'] ])

		if not cursor.fetchone()[0]:
			raise ServerError('Incorrect username / password')

		password 	= form['password']
		cursor		= db.query("SELECT * FROM tbl_users WHERE user_name = %s", [form['username'] ])

		for row in cursor.fetchall():
			#if bcrypt.hashpw(form['password'].encode('utf-8'), row[0]) == row[0]:
			if form['password'] == row[USER_PASSWORD]:
				session['username'] = form['username']
				return error

		raise ServerError('Incorrect username / password')

	except ServerError as e:
		error = str(e)
		return error


def registerUser(db, form):
	error = None

	try:
		username 	= form['username']
		password 	= form['password']
		email		= form['email']

		if not username or not password or not email:
			raise ServerError('Fill in all fields')

		password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(ROUNDS))

		cursor 	= db.query("SELECT COUNT(1) FROM tbl_users WHERE user_name = %s", [username])
		data	= cursor.fetchone()

		if data[0] == 0:
			cursor	= db.query("INSERT INTO tbl_users ('user_name', 'user_password', 'user_email') VALUES (%s, %s, %s)", [username, password, email])
			return None

		else:
			return "User exists"

	except ServerError as e:
		error = str(e)
		return error


def getUsers(db):
	error = None

	try:
		userlist = []

		cursor 	= db.query("SELECT user_name, user_username, user_email FROM tbl_users")

		for row in cursor.fetchall():
			userlist.append({'user_name': row[0], 'user_username': row[1], 'user_email': row[2]})

		return userlist

	except:
		error = "Failed"
		return error


def deleteUser(db, user):
	error = None

	print user 

	try:
		cursor 	= db.query("DELETE FROM tbl_users WHERE user_username like %s", [user])
		return None

	except:
		error = "Failed"
		return error





