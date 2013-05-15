from flask import g, request, flash, session, render_template, redirect, url_for, abort

def display_block(mode, subject_id, block_name):
	if not g.user:
		abort(401)#401 means unauthorize
	from rule import StateMachine
	sm = StateMachine(subject_id)
	if not sm.check(block_name, g.user.occupation, mode): # always use state machine to implement access control. mode = action
		abort(403)#403 means forbidden

	import model
	bClass = getattr(model, block_name) # get block class by its name given by string
	block_info = bClass.query.filter_by(subject_id = subject_id).first()
	sort_block_info = [] # sorting field by its name and return
	sort_block_info.append(['subject_id', block_info.subject_id])
	sort_block_info.append(['status', block_info.status])
	keys = sorted(block_info.__dict__.keys())
	keys = keys[1:-2]
	for key in keys:
		sort_block_info.append([key, getattr(block_info, key)]) # append the key and its value
	from rule import fieldTitle

	sm.update()
	return render_template('block.html', 
		mode = mode, 
		subject_id = subject_id,
		block_name = block_name,
		block_info = sort_block_info,
		title_map = fieldTitle[block_name])

def save_block(subject_id, block_name):
	if not g.user:
		abort(401)
	from rule import StateMachine
	sm = StateMachine(subject_id)
	if not sm.check(block_name, g.user.occupation, 'save'):
		abort(403)

	from prams import db
	import model
	bClass = getattr(model, block_name)
	qObj = bClass.query.filter_by(subject_id = subject_id).first()
	from rule import fieldTitle
	for fn in fieldTitle[block_name].iterkeys(): # fn is for field name
		# TODO: check data type before put into db
		if request.form.has_key(fn):
			content = request.form[fn]
			if content == 'None':
				content = None
		else:
			content = None
		setattr(qObj, fn, content) # set attribute by name
	db.session.add(qObj)
	db.session.commit()
	flash('The Form sheet has been saved')
	sm.update()
	return redirect(url_for('subject', subject_id = str(subject_id))) # note: end_point is the HTML for the view_func, you are redirecting the current view to a page, thus it must have a template to remnder.

def submit_block(subject_id, block_name):
	if not g.user:
		abort(401)
	from rule import StateMachine
	sm = StateMachine(subject_id)
	if not sm.check(block_name, g.user.occupation, 'submit'):
		abort(403)

	# check for validation and update the subject status
	from prams import db
	import model
	sObj = model.Subject.query.filter_by(subject_id = subject_id).first()
	bClass = getattr(model, block_name)
	qObj = bClass.query.filter_by(subject_id = subject_id).first()
	if qObj.status == 2:
		flash('THe block had been submitted and can\'t be submitted again.')
		return redirect(url_for('subject', subject_id = str(subject_id)))

	from rule import fieldTitle
	for fn in fieldTitle[block_name].iterkeys(): # fn is for field name
		if not request.form.has_key(fn): # some field would be None if it is not be filled.
			flash('The form is not completed.')
			return redirect(url_for('subject', subject_id = str(subject_id)))
		content = request.form[fn]
		# check data type before put into db
		if content == 'None':
			flash('The form is not completed.')
			return redirect(url_for('subject', subject_id = str(subject_id)))
		setattr(qObj, fn, content)
	## update the status
	db.session.add(qObj)
	db.session.commit()
	sm.update()
	flash('The form has been submitted.')
	return redirect(url_for('subject', subject_id = str(subject_id)))

def exit_block(subject_id):
	return redirect(url_for('subject', subject_id = str(subject_id)))