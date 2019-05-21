from flask import Flask, g


import sys
sys.path.append('./lib')

import lib
import MySQLdb
import json


app = Flask(__name__)

#Blueprint
app.register_blueprint(auth.bp)
app.register_blueprint(app.bp)

#Directivas
__author__      = "Gabriel Arce (arce.gerardogabriel@gmail.com"
__copyright__   = "Copyright (C) 2019 Gabriel Arce"
__license__     = "GPL 3.0"

#Carpetas


#Inicializacion
#config = {}
#execfile("config.conf",config)	
#db = DB()
#notifications = None 
#app.secret_key = 'SomeRandomStringHere'


@app.errorhandler(404)
def page_not_found(e):
    """Render a 404 page."""
    return render_template("404.html"), 404


@app.errorhandler(403)
def insufficient_permissions(e):
    """Render a 403 page."""
    return render_template("403.html"), 403