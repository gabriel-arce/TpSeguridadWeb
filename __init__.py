import json
import lib
import jinja2
import jinja2.utils
from flask import Flask, g, request, render_template_string, render_template

import sys
sys.path.append('./lib')


app = Flask(__name__)


# Directivas
__author__ = "Gabriel Arce (arce.gerardogabriel@gmail.com"
__copyright__ = "Copyright (C) 2019 Gabriel Arce"
__license__ = "GPL 3.0"

# Carpetas


# Inicializacion
#config = {}
# execfile("config.conf",config)
#db = DB()
#notifications = None
#app.secret_key = 'SomeRandomStringHere'
