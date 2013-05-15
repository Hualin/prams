from flask import g, request, flash, session, render_template, redirect, url_for, abort

def all_subjects():
	from model import Subject, f1b1
	if not g.user:
		abort(401)
	sObjs = Subject.query.order_by(Subject.establish_time.desc()) ## TODO: per page, decrease
	subjects = []
	for itm in sObjs:
		bObj = f1b1.query.filter_by(subject_id = itm.subject_id).first()
		ss = [itm.subject_id, itm.status, itm.establish_time, bObj.field03]
		subjects.append(ss)
	return render_template('all_subject.html', subjects = subjects)

def add_subject():
	if not g.user:
		abort(401)
	from rule import StateMachine
	sm = StateMachine()
	if not sm.check('subject', g.user.occupation, 'add'):
		abort(403)

	from prams import db
	from model import Subject
	newSubject = Subject()
	db.session.add(newSubject)
	db.session.flush()
	db.session.refresh(newSubject)
	row_id = newSubject.subject_id
	sm.cur_subject_id = row_id

	from model import f1b1
	newFb = f1b1(row_id)
	db.session.add(newFb)

	from model import f1b2
	newFb = f1b2(row_id)
	db.session.add(newFb)

	from model import f1b3
	newFb = f1b3(row_id)
	db.session.add(newFb)

	from model import f1b4
	newFb = f1b4(row_id)
	db.session.add(newFb)

	from model import f1b5
	newFb = f1b5(row_id)
	db.session.add(newFb)

	from model import f1b6
	newFb = f1b6(row_id)
	db.session.add(newFb)

	# # To estabalish more blocks.

	db.session.commit()
	flash('A new subject has been added, subject ID is "%d"' %row_id)
	sm.update()
	return redirect(url_for('all_subjects'))

def view_subject(subject_id):
	if not g.user:
		abort(401)
	# basic information
	subject_info = {}
	subject_info['subject_id'] = subject_id
	from model import f1b1, Subject
	qObj = f1b1.query.filter_by(subject_id = subject_id).first()
	sObj = Subject.query.filter_by(subject_id = subject_id).first()
	subject_info['department'] = qObj.field01
	subject_info['title'] = qObj.field02
	subject_info['holder'] = qObj.field03
	subject_info['new'] = qObj.field04
	subject_info['subject_status'] = sObj.status

	extra_action = None
	done_before = False
	from rule import StateMachine
	sm = StateMachine(subject_id)
	if sObj.status in ('wait_to_allocate', 'wait_to_review', 'final_review'):
		extra_action = sObj.status
		from model import PendingJob
		done_before = (PendingJob.query.filter_by(subject_id = subject_id, stage = extra_action, to_user_occupation = g.user.occupation).first() == None)
	# form A table
	# order by: section, block responisbility action, status
	from rule import FormStructure
	import model
	fm = FormStructure()
	tb_fA = []
	for block_name in fm.get_blocks('Form A'):
		bClass = getattr(model, block_name)
		tb_fA.append([
			(block_name == sObj.status), # activated
			fm.get_sectionName(block_name), # section name
			block_name, # block name
			fm.get_responsibility(block_name), # responsibility
			sm.get_view_OR_edit(block_name, g.user.occupation), # action
			bClass.query.filter_by(subject_id = subject_id).first().status # block status
			])

	# form B table
	tb_fB = []
	# form C table
	tb_fC = []
	return render_template('subject.html', 
		subject_info = subject_info, 
		table_formA = tb_fA, 
		table_formB = tb_fB,
		table_formC = tb_fC,
		extra_action = extra_action,
		sm = sm,
		done_before = done_before
		)

def delete_subject(subject_id):
	if not g.user:
		abort(401)
	from rule import StateMachine
	sm = StateMachine(subject_id)
	if not sm.check('*', g.user.occupation, 'delete'):
		abort(403)
	from rule import FormStructure
	fm = FormStructure()
	from prams import db
	import model
	for bl in fm.get_blocks():
		bClass = getattr(model, bl)
		qObj = bClass.query.filter_by(subject_id = subject_id).first()
		db.session.delete(qObj)
		db.session.commit()
	sObj = model.Subject.query.filter_by(subject_id = subject_id).first()
	db.session.delete(sObj)
	db.session.commit()
	sm.update()
	flash('The Subject ' + subject_id + ' has been deleted.')
	return redirect(url_for('all_subjects'))

def allocate_establishment_reference_number(subject_id):
	from rule import StateMachine
	sm = StateMachine(subject_id)
	if not sm.check('wait_to_allocate', g.user.occupation, 'allocate'):
		abort(403)
	flash('Allocation operation completed.')
	sm.update()
	return redirect(url_for('subject', subject_id = subject_id))

def review_subject(subject_id):
	from rule import StateMachine
	sm = StateMachine(subject_id)
	if not sm.check('wait_to_review', g.user.occupation, 'review'):
		abort(403)
	flash('subject has been reviewed.')
	sm.update()
	return redirect(url_for('subject', subject_id = subject_id))

def seal_subject(subject_id):
	from rule import StateMachine
	sm = StateMachine(subject_id)
	if not sm.check('final_review', g.user.occupation, 'seal'):
		abort(403)
	flash('subject has been sealed.')
	sm.update()
	return redirect(url_for('subject', subject_id = subject_id))