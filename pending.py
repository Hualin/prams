from flask import g, request, flash, session, render_template, redirect, url_for, abort

def all_pendings():
	from model import User, PendingJob
	if not g.user:
		abort(401)
	pObj = PendingJob.query.filter_by(to_user_occupation = g.user.occupation).order_by(PendingJob.created_time.desc())
	# pObj = PendingJob.query.filter_by(to_user_occupation = g.user.occupation)
	jobs = []
	for itm in pObj:
		uObj = User.query.filter_by(user_id = itm.from_user_id).first()
		jj = (itm.subject_id, itm.created_time, itm.stage, uObj.user_name, uObj.occupation, itm.status)
		jobs.append(jj)
	from rule import occupationTitle
	return render_template('all_pending.html', jobs = jobs,  occupationTitle = occupationTitle)