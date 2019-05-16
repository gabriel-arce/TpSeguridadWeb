from flask import Flask, g

#@app.before_request
#def before_request():
#    """
#    Load a user object into `g.user` before each request.
#    """
#    if auth.oidc.user_loggedin:
#        g.user = auth.okta_client.get_user(auth.oidc.user_getfield("sub"))
#    else:
#        g.user = None

app = Flask(__name__)

#Blueprint
app.register_blueprint(auth.bp)
app.register_blueprint(app.bp)

#Directivas
__author__      = "Gabriel Arce (arce.gerardogabriel@gmail.com"
__copyright__   = "Copyright (C) 2019 Gabriel Arce"
__license__     = "GPL 3.0"

@app.errorhandler(404)
def page_not_found(e):
    """Render a 404 page."""
    return render_template("404.html"), 404


@app.errorhandler(403)
def insufficient_permissions(e):
    """Render a 403 page."""
    return render_template("403.html"), 403