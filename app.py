from flask import Flask, render_template, session, redirect, url_for, escape, request, g

import MySQLdb

import sys
sys.path.append('./lib')

import json
import Users 		as Users
import Proyectos 	as Proyectos

app = Flask(__name__)

class DB:
	conn = None

	def connect(self):
		config = {}
		execfile("config.conf",config)
		
		self.conn = MySQLdb.connect(
			host=config['db_host'],
			user=config['db_user'],
			passwd=config['db_pass'],
			db=config['db_data']
		)

		self.conn.autocommit(True)	
		self.conn.set_character_set('utf8')

	def query(self, sql, args=None):
		try:
			cursor = self.conn.cursor()
			cursor.execute(sql, args)
		except (AttributeError, MySQLdb.OperationalError):
			self.connect()
			cursor = self.conn.cursor()
			cursor.execute(sql, args)

		return cursor


if __name__ == "__main__":
	config = {}
	execfile("config.conf",config)	
	db = DB()
	notifications = None 
	app.secret_key = 'SomeRandomStringHere'


#Definiendo rutas posibles
@app.route('/')
def index():
	messages = None
	global notifications

	if notifications:
		message 		= notifications
		notifications 	= None

	return render_template('index.html', session=session)

@app.route('/users')
def users():
	messages = None
	global notifications

	if notifications:
		message 		= notifications
		notifications 	= None

	if 'username' not in session:
		message = {'message': 'Please log in', 'type': 'warning'}
		return redirect(url_for('login'))

	if session['username'] != 'admin':
		return redirect(url_for('index', message='Admin only page'))

	users = Users.getUsers(db)
	if not users:
		notifications = {'message': 'Failed to retrieve users', 'type': 'error'}
		return render_template('users.html', message=message)

	return render_template('users.html', users=users)


@app.route('/users/edit/<user>')
def editUser(user='<user'):
	return 'Se edita el usuario: ' + user


@app.route('/users/delete/<user>')
def deleteUser(user='<user'):
	global notifications

	if 'username' not in session:
		notifications = {'message': 'Please log in', 'type': 'warning'}
		return redirect(url_for('login'))

	if session['username'] != 'admin':
		notifications = {'message': 'Admin only page', 'type': 'error'}
		return redirect(url_for('index'))

	result = Users.deleteUser(db,user)
	if not result:
		notifications = {'message': 'User deleted successfully', 'type': 'success'}
		return redirect(url_for('users', message="User deleted successfully"))

	print result

	notifications = {'message': 'Something went wrong: ' + result, 'type': 'error'}
	return redirect(url_for('users', message="Something went wrong: " + result))	


@app.route('/login', methods=['GET', 'POST'])
def login():
	message = None
	global notifications

	if notifications:
		message 		= notifications
		notifications 	= None

	if 'username' in session:
		return redirect(url_for('index'))

	if request.method == 'POST':
		result = Users.loginForm(db, request.form)

		if not result:
			notifications = {'message': 'Logged in', 'type': 'success'}
			g.user 		  = 'username'
			return redirect(url_for('proyectos'))	

		else:
			message = {'message': 'Failed to log in', 'type': 'error'}
			return redirect(url_for('login', message=message))	


	return render_template('login.html', message=message)	


@app.route('/logout')
def logout():
	global notifications

	if 'username' not in session:
		return redirect(url_for('login'))

	session.pop('username', None)
	notifications = {'message': 'Logged out', 'type': 'success'}
	return redirect(url_for('login'))	


@app.route('/register', methods=['GET', 'POST'])
def register():
	message = None
	global notifications

	if notifications:
		message 		= notifications
		notifications 	= None

	if request.method == 'POST':
		result = Users.registerUser(db, request.form, config['pw_rounds'])
		if not result:
			notifications = {'message': 'Registration successful', 'type': 'success'}

			#if session['username'] == 'admin':
			#	return redirect(url_for('register'))

			#else:	
			return redirect(url_for('login'))

		else:
			notifications = {'message': 'Something went wrong: ' + result, 'type': 'error'}
			return render_template('register', message=message)

	#if session['username'] == 'admin':
	#	return render_template('register.html')

	return render_template('register.html')


@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')


@app.route('/proyectos')
def proyectos():
	#proyectos = Proyectos.getProyectosPorUsuario(session['username']) 
	return render_template('proyectos.html', proyectos=Proyectos.getProyectosPorUsuario(session['username']))


@app.route('/proyectos/agregar', methods=['POST'])
def agregarProyecto():
	
	return render_template('proyectos.html', proyectos=Proyectos.agregarProyecto(request.form, session['username']))

#REjecutando app
if __name__ == "__main__":
	app.run(
			host=config['server_ip'],
			port=config['server_port'],
			debug=config['debug']
		)









