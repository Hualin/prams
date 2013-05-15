from flask import g, request, flash, session, render_template, redirect, url_for, abort
from werkzeug import check_password_hash, generate_password_hash

def login():
	from model import User
	"""Logs the user in."""
	if g.user:
		return redirect(url_for('home'))
	error = None
	if request.method == 'POST':
		curUsr = User.query.filter_by(user_name=request.form['user_name']).first()

		if curUsr is None:
			error = 'Invalid username'
		elif not check_password_hash(curUsr.password_hash,
									 request.form['password']):
			error = 'Invalid password'
		else:
			flash('You were logged in')
			session['user_id'] = curUsr.user_id
			return redirect(url_for('home'))
	return render_template('login.html', error=error)

def logout():
	"""Log the user out."""
	flash('You were logged out')
	session.pop('user_id', None)
	return redirect(url_for('home'))

def register():
	from model import User
	"""Registers the user."""
	if g.user:
		flash('To set up, please log out and register a new one.')
		return redirect(url_for('home'))
	error = None
	if request.method == 'POST':
		if not request.form['user_name']:
			error = 'You have to enter a username'
		elif not request.form['occupation']:
			error = 'You have to enter an occupation'
		elif not request.form['password']:
			error = 'You have to enter a password'
		elif request.form['password'] != request.form['password2']:
			error = 'The two passwords do not match'
		elif User.query.filter_by(user_name=request.form['user_name']).first() is not None:
			error = 'The username is already taken'
		else:
			newUsr = User(request.form['user_name'], 
				request.form['occupation'], 
				generate_password_hash(request.form['password']),
				request.form['e-mail'])
			from prams import db
			db.session.add(newUsr)
			db.session.commit()
			flash('You were successfully registered and can login now')
			return redirect(url_for('login'))
	return render_template('register.html', error=error)