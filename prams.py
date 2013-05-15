from flask import Flask, request, session, url_for, redirect, \
	 render_template, abort, g, flash
from flask_sqlalchemy import SQLAlchemy

# application
app = Flask(__name__)
from config import *
app.config.from_object(__name__)
db = SQLAlchemy(app) # create a db for this app

@app.before_request
def before_request():
	g.user = None
	if 'user_id' in session:
		from model import User
		g.user = User.query.filter_by(user_id = session['user_id']).first()

@app.teardown_request
def shutdown_session(exception=None):
	db.session.remove()

from init_route import *

if __name__ == '__main__':
	app.run()