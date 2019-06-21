from flask import Flask, render_template, session, redirect, url_for, escape, request, g, render_template_string

#Propios
from lib.Users  	import getUsers, deleteUser, loginForm, registerUser
from lib.Proyectos 	import getProyectosPorUsuario, agregarNuevoProyecto, borrarProyectoPorIndice, editarProyecto
from lib.DB 		import DB 
from lib.config		import *

from jinja2 import Environment

app = Flask(__name__)
Jinja2 = Environment()

if __name__ == "__main__":
	config = {}
	execfile("config.conf",config)	
	db = DB()
	app.secret_key = 'SomeRandomStringHere'


#Definiendo rutas posibles
@app.route('/')
def index():
	username = request.values.get('username')
	
	return render_template('index.html', session=session, username=username)
	#return Jinja2.from_string('Hola' + str(username)).render()

#@app.route('/?<username>', methods=['POST', 'GET'])
#def render():
#	return render_template_string('index.html', username=username)

@app.route('/users')
def users():
	if 'username' not in session:
		return redirect(url_for('login'), message='Please log in')

	if session['username'] != 'admin':
		return redirect(url_for('index', message='Admin only page'))

	users = getUsers(db)
	if not users:
		return render_template('users.html', message='Failed to retrieve users')

	return render_template('users.html', users=users)


@app.route('/users/edit/<user>')
def editUser(user='<user'):
	return 'Se edita el usuario: ' + user


@app.route('/users/delete/<user>')
def deleteUser(user='<user'):
	if 'username' not in session:
		return redirect(url_for('login'), message='Please log in')

	if session['username'] != 'admin':
		return redirect(url_for('index'), message='Admin only page')

	result = deleteUser(db,user)
	if not result:
		return redirect(url_for('users', message="User deleted successfully"))

	return redirect(url_for('users', message="Something went wrong: " + result))	


@app.route('/login', methods=['GET', 'POST'])
def login():
	proyectos = []

	username = str(request.values.get('username'))
	#return render_template_string('Hello' + username)

	if 'username' in session:
		return redirect(url_for('index'))

	if request.method == 'POST':
		result = loginForm(db, request.form)

		if not result:
			proyectos = getProyectosPorUsuario(request.form['username'])
			print proyectos

			return redirect(url_for('index', username=username))
			#return render_template('index.html', username=username)

		else:
			return redirect(url_for('login'))	
			
	return render_template('login.html')	


@app.route('/logout', methods=['GET', 'POST'])
def logout():
	if 'username' not in session:
		return redirect(url_for('login'))

	session.pop('username', None)

	return redirect(url_for('login'), 'Logged out')	


@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		result = registerUser(db, request.form, config['pw_rounds'])
		if not result:
			return redirect(url_for('login'))

		else:
			return render_template('register', message='Something went wrong')

	return render_template('register.html')


@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')


@app.route('/proyectos', methods=['GET', 'POST'])
def proyectos():

	if 'Eliminar' in request.form:
		return render_template('proyectos.html', proyectos=borrarProyectoPorIndice(request.form))

	#elif 'Back' in request.form:
	#	return render_template('proyectos.html', proyectos=getProyectosPorUsuario(session['username']))

	elif 'Editar' in request.form:
	#	if request.method == 'GET':
		indice 		=  int(request.form['Editar'][0]) - 1
		proyecto 	= getProyectosPorUsuario(session['username'])[indice]
		return render_template('editarProyecto.html', proyecto=proyecto)

		#if request.method == 'POST':
		#	return render_template('proyectos.html', proyectos=editarProyecto(request.form, session['username']))

	elif 'Actualizar' in request.form:
		print 'paso'
		return render_template('proyectos.html', proyectos=getProyectosPorUsuario(session['username']))


	return render_template('proyectos.html', proyectos=getProyectosPorUsuario(session['username']))


@app.route('/proyectos/agregar', methods=['GET', 'POST'])
def agregarProyecto():
	return render_template('proyectos.html', proyectos=agregarNuevoProyecto(request.form, session['username']))


@app.route('/<path:page>')
def custom_page(page):
  if page == 'favicon.ico': return ''

  try:
    template = open(page).read()

  except Exception as e:
    #template = render_template("404.html", urlErronea=str(e))
    template = str(e)

  #template += "\n<!-- page: %s, src: %s -->\n" % (page, __file__)

  return render_template_string(template, name='test')



#Manejo de Errores
@app.errorhandler(404)
def page_not_found(e):
    """Render a 404 page."""

    #return render_template("404.html", urlErronea=(request.url)), 404
    template = '''{ extends "layout.html" }

	{ block title }Page Not Found{ endblock }
	{ block body }
  	<h1 class="text-center">Page Not Found</h1>
  	<p class="text-center">Whatever you did, it's not working :( </p>
  	<br>
  	<p class="text-center">%s</p>
	{ endblock } ''' % (request.url)

    print template

    return render_template_string(template), 404


@app.errorhandler(403)
def insufficient_permissions(e):
    """Render a 403 page."""
    return render_template("403.html"), 403


#REjecutando app
if __name__ == "__main__":
	app.run(
			host=config['server_ip'],
			port=config['server_port'],
			debug=config['debug']
		)