from prams import app

@app.route('/')
def home():
	from flask import render_template, g
	from rule import occupationTitle
	return render_template('home.html', occupationTitle = occupationTitle)

from logon import login
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])

from logon import logout
app.add_url_rule('/logout', view_func = logout)

from logon import register
app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])

from subject import all_subjects
app.add_url_rule('/all_subjects', 'all_subjects', all_subjects, methods=['GET', 'POST'])

from subject import add_subject
app.add_url_rule('/all_subjects/add', view_func = add_subject, methods=['POST'])

from subject import delete_subject
app.add_url_rule('/all_subjects/<subject_id>/delete', view_func = delete_subject, methods=['POST'])

from subject import view_subject
app.add_url_rule('/all_subjects/<subject_id>', 'subject', view_subject, methods=['GET', 'POST'])

from subject import allocate_establishment_reference_number
app.add_url_rule('/all_subjects/<subject_id>/allocate', view_func = allocate_establishment_reference_number, methods=['POST'])

from subject import review_subject
app.add_url_rule('/all_subjects/<subject_id>/review', view_func = review_subject, methods=['POST'])

from subject import seal_subject
app.add_url_rule('/all_subjects/<subject_id>/seal', view_func = seal_subject, methods=['POST'])

from form import display_block
app.add_url_rule('/all_subjects/<subject_id>/<block_name>/<mode>', 'block', display_block)

from form import save_block
app.add_url_rule('/all_subjects/<subject_id>/<block_name>/save', view_func = save_block, methods=['POST'])

from form import submit_block
app.add_url_rule('/all_subjects/<subject_id>/<block_name>/submit', view_func = submit_block, methods=['POST'])

from form import exit_block
app.add_url_rule('/all_subjects/<subject_id>/exit', view_func = exit_block, methods=['POST'])

from pending import all_pendings
app.add_url_rule('/pending_jobs/', 'all_pendings', all_pendings, methods=['GET', 'POST'])

from history import history
app.add_url_rule('/history/', 'history', history, methods=['GET', 'POST'])

from staff import all_staff
app.add_url_rule('/all_staff/', 'all_staff', all_staff, methods=['GET'])