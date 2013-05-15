from flask import g, request, flash, session, render_template, redirect, url_for, abort

def all_staff():
	from model import User
	if not g.user:
		abort(401)
	sObjs = User.query.order_by(User.user_name) ## TODO: per page, decrease
	staff_dict = []
	for itm in sObjs:
		staff_dict.append((itm.user_name, itm.user_id, itm.occupation, itm.email))
	return render_template('all_staff.html', staff_dict = staff_dict)