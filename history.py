from flask import g, request, flash, session, render_template, redirect, url_for, abort

def history():
	from model import User, History
	if not g.user:
		abort(401)
	hObj = History.query.order_by(History.edited_time.desc())

	sections = []
	for itm in hObj:
		uObj = User.query.filter_by(user_id = itm.edited_by_user_id).first()
		jj = (itm.edited_by_user_id, uObj.user_name, itm.subject_id, itm.edited_time, itm.stage, itm.action_name, itm.user_occupation) # content structure
		sections.append(jj)
	from rule import occupationTitle
	return render_template('history.html', sections = sections,  occupationTitle = occupationTitle)