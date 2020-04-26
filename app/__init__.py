# Import flask and template operators
from flask import Flask
from app.mod_print_covid.PrintCovidController import mod_print_covid

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Register blueprint(s)
app.register_blueprint(mod_print_covid)


@app.errorhandler(404)
def not_found(error):
    return '<h1>404 Page not Found</h1>', 404



