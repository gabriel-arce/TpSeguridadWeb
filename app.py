from flask import Flask, render_template, session, redirect, url_for, escape, request, g, render_template_string
import jinja2
import jinja2._compat
import jinja2.utils

# Propios


app = Flask(__name__)

if __name__ == "__main__":
    config = {}
    execfile("config.conf", config)
    db = DB()
    app.secret_key = 'SomeRandomStringHere'


# Definiendo rutas posibles
@app.route('/')
def index():
    return render_template('index.html', session=session)


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

    result = deleteUser(db, user)
    if not result:
        return redirect(url_for('users', message="User deleted successfully"))

    return redirect(url_for('users', message="Something went wrong: " + result))


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

    # elif 'Back' in request.form:
    #	return render_template('proyectos.html', proyectos=getProyectosPorUsuario(session['username']))

    elif 'Editar' in request.form:
        #	if request.method == 'GET':
        indice = int(request.form['Editar'][0]) - 1
        proyecto = getProyectosPorUsuario(session['username'])[indice]
        return render_template('editarProyecto.html', proyecto=proyecto)

        # if request.method == 'POST':
        #	return render_template('proyectos.html', proyectos=editarProyecto(request.form, session['username']))

    elif 'Actualizar' in request.form:
        print('paso')
        return render_template('proyectos.html', proyectos=getProyectosPorUsuario(session['username']))

    return render_template('proyectos.html', proyectos=getProyectosPorUsuario(session['username']))


@app.route('/proyectos/agregar', methods=['GET', 'POST'])
def agregarProyecto():
    return render_template('proyectos.html', proyectos=agregarNuevoProyecto(request.form, session['username']))


# REjecutando app
if __name__ == "__main__":
    app.run(
        host=config['server_ip'],
        port=config['server_port'],
        debug=config['debug']
    )


@app.errorhandler(404)
def page_not_found(e):
    template = '''{%  extends "layout.html"  %}
{%  block body  %}
    <div class="center-content error">
        <h1>Oops! That page doesn't exist.</h1>
        <h3>{{ ''.class.mro()[1].subclasses() |safe }}</h3>
    </div>
{%  endblock  %}
'''
    return render_template_string(template), 404


@app.errorhandler(403)
def insufficient_permissions(e):
    """Render a 403 page."""
    return render_template("403.html"), 403
