from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from prams import db

class User(db.Model):
	user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	user_name = db.Column(db.String(80))
	occupation = db.Column(db.String(100))
	password_hash = db.Column(db.String(256))
	email = db.Column(db.String(256))

	def __init__(self, user_name, occupation, password_hash, email):
		self.user_name = user_name
		self.occupation = occupation
		self.password_hash = password_hash
		self.email = email

	# def __repr__(self):
	# 	return '<Post %r>' % self.title

class Subject(db.Model):
	subject_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	status = db.Column(db.String(256))
	establish_time = db.Column(db.DateTime)

	def __init__(self):
		from datetime import datetime
		self.status = 'f1b1'
		self.establish_time = datetime.now()
		
class f1b1(db.Model):
	subject_id = db.Column(db.Integer, primary_key = True)
	status = db.Column(db.Integer)
	field01 = db.Column(db.String(256))
	field02 = db.Column(db.String(256))
	field03 = db.Column(db.String(256))
	field04 = db.Column(db.String)
	field05 = db.Column(db.String)
	field06 = db.Column(db.String)
	field07 = db.Column(db.String(256))
	field08 = db.Column(db.String)
	field09 = db.Column(db.String)
	field10 = db.Column(db.Integer)
	field11 = db.Column(db.Integer)
	field12 = db.Column(db.String(256))
	field13 = db.Column(db.Integer)
	field14 = db.Column(db.Integer)
	field15 = db.Column(db.Integer)
	field16 = db.Column(db.Integer)
	field17 = db.Column(db.Integer)
	field18 = db.Column(db.Integer)
	field19 = db.Column(db.Integer)

	def __init__(self, subject_id):
		self.subject_id = subject_id
		self.status = 0

	# def __repr__(self):
	# 	return '<Post %r>' % self.title

class f1b2(db.Model):
	subject_id = db.Column(db.Integer, primary_key = True)
	status = db.Column(db.Integer)
	field01 = db.Column(db.Text)
	field02 = db.Column(db.String(256))
	field03 = db.Column(db.String(256))
	field04 = db.Column(db.String(256))
	field05 = db.Column(db.String(256))
	field06 = db.Column(db.String)

	def __init__(self, subject_id):
		self.subject_id = subject_id
		self.status = 0

	# def __repr__(self):
	# 	return '<Post %r>' % self.title

class f1b3(db.Model):
	subject_id = db.Column(db.Integer, primary_key = True)
	status = db.Column(db.Integer)
	field01 = db.Column(db.Integer)
	field02 = db.Column(db.String)
	field03 = db.Column(db.String)
	field04 = db.Column(db.Text)
	field05 = db.Column(db.String(256))
	field06 = db.Column(db.String)

	def __init__(self, subject_id):
		self.subject_id = subject_id
		self.status = 0

	# def __repr__(self):
	# 	return '<Post %r>' % self.title

class f1b4(db.Model):
	subject_id = db.Column(db.Integer, primary_key = True)
	status = db.Column(db.Integer)
	field01 = db.Column(db.Text)
	field02 = db.Column(db.String(256))
	field03 = db.Column(db.String)

	def __init__(self, subject_id):
		self.subject_id = subject_id
		self.status = 0

	# def __repr__(self):
	# 	return '<Post %r>' % self.title

class f1b5(db.Model):
	subject_id = db.Column(db.Integer, primary_key = True)
	status = db.Column(db.Integer)
	field01 = db.Column(db.String)
	field02 = db.Column(db.String)
	field03 = db.Column(db.String)
	field04 = db.Column(db.Text)
	

	def __init__(self, subject_id):
		self.subject_id = subject_id
		self.status = 0

	# def __repr__(self):
	# 	return '<Post %r>' % self.title

class f1b6(db.Model):
	subject_id = db.Column(db.Integer, primary_key = True)
	status = db.Column(db.Integer)
	field01 = db.Column(db.String)
	field02 = db.Column(db.String)
	field03 = db.Column(db.String)
	field04 = db.Column(db.Text)
	
	def __init__(self, subject_id):
		self.subject_id = subject_id
		self.status = 0

	# def __repr__(self):
	# 	return '<Post %r>' % self.title
## TODO: More table to be added

class PendingJob(db.Model):
	pending_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	from_user_id = db.Column(db.Integer)
	to_user_occupation = db.Column(db.String(256))
	subject_id = db.Column(db.Integer)
	stage = db.Column(db.String(100))
	status = db.Column(db.Integer)
	created_time = db.Column(db.DateTime)

	def __init__(self, from_user_id, to_user_occupation, subject_id, stage):
		self.from_user_id = from_user_id
		self.to_user_occupation = to_user_occupation
		self.subject_id = subject_id
		self.stage = stage
		self.status = 0 # 0 is ont be occupied, 1 is occupied
		from datetime import datetime
		self.created_time = datetime.now()

class History(db.Model):
	history_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	edited_by_user_id = db.Column(db.Integer)
	user_occupation = db.Column(db.String(256))
	action_name = db.Column(db.String)
	subject_id = db.Column(db.Integer)
	stage = db.Column(db.String(100))
	edited_time = db.Column(db.DateTime)

	def __init__(self, edited_by_user_id, user_occupation, action_name, subject_id, stage):
		self.edited_by_user_id = edited_by_user_id
		self.user_occupation = user_occupation
		self.action_name = action_name
		self.subject_id = subject_id
		self.stage = stage
		from datetime import datetime
		self.edited_time = datetime.now()		