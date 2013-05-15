from flask import g
from prams import db

class FormStructure(object):
	def __init__(self):
		self.bsfr_list = [
		## block name, section name, form name, responsibility
		['f1b1', 'Section 1', 'Form A', 'HOD'], 
		['f1b2', 'Section 2', 'Form A', 'HOD'], 
		['f1b3', 'Section 3', 'Form A', 'HR'],
		['f1b4', 'Section 3', 'Form A', 'MA'],
		['f1b5', 'Section 3', 'Form A', 'DO'],
		['f1b6', 'Section 3', 'Form A', 'DP'],
		# extend rule
		['wait_to_allocate', 'extend' , 'extend' , 'HR'],
		['wait_to_review', 'extend' , 'extend' , 'HR'],
		['final_review', 'extend' , 'extend' , 'HOD MA']
		## more blocks if needed
		]

	def get_sectionName(self, block_name):
		for bsfr in self.bsfr_list:
			if bsfr[0] == block_name:
				return bsfr[1]
		return None

	def get_formName(self, block_name):
		for bsfr in self.bsfr_list:
			if bsfr[0] == block_name:
				return bsfr[2]
		return None

	def get_blocks(self, formName = None, sectionName = None):
		bl = []
		for bsfr in self.bsfr_list:
			if (formName == bsfr[2] or formName == None) and bsfr[2] != 'extend':
				if (sectionName == bsfr[1] or sectionName == None) and bsfr[1] != 'extend':
					bl.append(bsfr[0])
		return bl

	def get_responsibility(self, block_name):
		for bsfr in self.bsfr_list:
			if bsfr[0] == block_name:
				return bsfr[3]
		return None

class StateMachine(object):
	## magic here, don't touch anything
	rule_list = {
		# (stage, obligation, action): [update_function, ... argument]
		('subject', 'HOD', 'add'): ['on_add_subject'],
		('*', 'HOD', 'delete'): ['on_delete_subject'], # * mneas anything here

		('subject', 'ADM', 'add'): ['on_add_subject'],
		('*', 'ADM', 'delete'): ['on_delete_subject'],
		('*', 'ADM', 'edit'): ['on_edit_block'],

		('*', '*', 'view'): ['on_view_block'], # anyone at any stage could view the block
		
		('f1b1', 'HOD', 'edit'): ['on_edit_block'],
		('f1b1', 'HOD', 'save'): ['on_save_block'],
		('f1b1', 'HOD', 'submit'): ['on_submit_block', 'f1b2'], #the argument is next stage (or block to be filled)

		('f1b2', 'HOD', 'edit'): ['on_edit_block'],
		('f1b2', 'HOD', 'save'): ['on_save_block'],
		('f1b2', 'HOD', 'submit'): ['on_submit_block', 'f1b3'],

		('f1b3', 'HR', 'edit'): ['on_edit_block'],
		('f1b3', 'HR', 'save'): ['on_save_block'],
		('f1b3', 'HR', 'submit'): ['on_submit_block', 'wait_to_allocate'],

		('wait_to_allocate', 'HR', 'allocate'): ['on_allocate_number', 'f1b4'],

		('f1b4', 'MA', 'edit'): ['on_edit_block'],
		('f1b4', 'MA', 'save'): ['on_save_block'],
		('f1b4', 'MA', 'submit'): ['on_submit_block', 'f1b5'],

		('f1b5', 'DO', 'edit'): ['on_edit_block'],
		('f1b5', 'DO', 'save'): ['on_save_block'],
		('f1b5', 'DO', 'submit'): ['on_submit_block', {'Approved': 'wait_to_review', 'Declined': 'wait_to_review', 'To be referred to Deputy Principal': 'f1b6'}],

		('f1b6', 'DP', 'edit'): ['on_edit_block'],
		('f1b6', 'DP', 'save'): ['on_save_block'],
		('f1b6', 'DP', 'submit'): ['on_submit_block', {'Approved': 'wait_to_review', 'Declined': 'wait_to_review', 'To be referred to Planning Resources Committee': 'wait_to_review'}],

		('wait_to_review', 'HR', 'review'): ['on_reivew_subject', 'final_review'],

		('final_review', 'HOD', 'seal'): ['on_seal', 'sealed'],
		('final_review', 'MA', 'seal'): ['on_seal','sealed'],
		}

	def __init__(self, subject_id = None):
		## init the form status from db
		self.cur_subject_id = subject_id
		self.checked = False
		self.updated = False
		if subject_id == None: # a state machine without attaching to any subject
			return
		from model import Subject
		# set current status
		self.cur_status = Subject.query.filter_by(subject_id = subject_id).first().status

	def check(self, stage_name, occupation, action):
		self.cur_stage_name = stage_name
		self.cur_occupation = occupation
		self.cur_action = action
		rule_key = (self.cur_stage_name, self.cur_occupation, self.cur_action) # construct key for query rule_list

		if not self.rule_list.has_key(rule_key): # rule key validity hiarchy
			rule_key = ('*', self.cur_occupation, self.cur_action)
			if not self.rule_list.has_key(rule_key):
				rule_key = ('*', '*', self.cur_action)
				if not self.rule_list.has_key(rule_key):
					## not authorized accessing
					self.checked = True
					return False
		self.checked = True
		return True # access right granted

	def update(self):
		if not self.checked:
			raise('invalid calling order, update() should be called after check()!')

		rule_key = (self.cur_stage_name, self.cur_occupation, self.cur_action)
		if not self.rule_list.has_key(rule_key):
			rule_key = ('*', self.cur_occupation, self.cur_action)
			if not self.rule_list.has_key(rule_key):
				rule_key = ('*', '*', self.cur_action)
		update_func = getattr(self, self.rule_list[rule_key][0]) # use rule_key to obtain corresponding update function
		self.rule_key = rule_key # final_reviewly we get rule_key
		self.updated = True
		update_func()

	def get_view_OR_edit(self, block_name, occupation):
		# for a block, the user could edit, view or get these both option
		ret = ['view']
		if self.rule_list.has_key((block_name, occupation, 'edit')) and self.cur_status == block_name:
			ret.append('edit')
		else:
			ret.append('None')
		return ret

	def on_add_subject(self):
		if not self.checked:
			raise('invalid calling order, update() should be called after check()!')
		# give history
		# give pending
		from model import PendingJob
		newJob = PendingJob(g.user.user_id, 'HOD', self.cur_subject_id, 'f1b1')
		db.session.add(newJob)
		db.session.commit()

	def on_view_block(self):
		if not self.checked:
			raise('invalid calling order, update() should be called after check()!')
		# give history
		# from prams import db
		# import model
		# newSection = model.History(g.user.user_id, g.user.occupation, 'viewed', self.cur_subject_id, self.cur_status)
		# db.session.add(newSection)
		# db.session.commit()
		# TODO
		print 'it works', self.cur_action

	def on_delete_subject(self):
		if not self.checked:
			raise('invalid calling order, update() should be called after check()!')
		# delete the whole subject
		# give history
		# delete relavent all pending jobs
		from prams import db
		import model
		newSection = model.History(g.user.user_id, g.user.occupation, 'deleted', self.cur_subject_id, None)
		db.session.add(newSection)
		pObj = model.PendingJob.query.filter_by(subject_id = self.cur_subject_id).first()
		db.session.delete(pObj)
		db.session.commit()

	def on_edit_block(self):
		if not self.checked:
			raise('invalid calling order, update() should be called after check()!')
		# change block editing status
		# give history
		# TODO
		from prams import db
		import model
		newSection = model.History(g.user.user_id, g.user.occupation, 'edited', self.cur_subject_id, self.cur_status)
		db.session.add(newSection)
		db.session.commit()
		print 'it works', self.cur_action

	def on_save_block(self):
		if not self.checked:
			raise('invalid calling order, update() should be called after check()!')
		# chage block status
		# give history
		# give pending
		from prams import db
		import model
		bClass = getattr(model, self.cur_stage_name)
		qObj = bClass.query.filter_by(subject_id = self.cur_subject_id).first()
		qObj.status = 1 # 1 means the block has been modifiy but not been valided and submitted.
		newSection = model.History(g.user.user_id, g.user.occupation, 'saved', self.cur_subject_id, self.cur_status)
		db.session.add(newSection)
		db.session.add(qObj)
		db.session.commit()

	def on_submit_block(self):
		if not self.checked:
			raise('invalid calling order, update() should be called after check()!')
		# chage block status
		# give history
		# move to next stage
		# give pending
		from prams import db
		import model
		#delete: filter=select id and stage to choice the subject 
		pObj = model.PendingJob.query.filter_by(subject_id = self.cur_subject_id, stage = self.cur_stage_name).first()
		db.session.delete(pObj)
		db.session.commit()

		sObj = model.Subject.query.filter_by(subject_id = self.cur_subject_id).first()
		newSection = model.History(g.user.user_id, g.user.occupation, 'submited', self.cur_subject_id, self.cur_status)
		bClass = getattr(model, self.cur_stage_name)#getattr = get class by class name
		qObj = bClass.query.filter_by(subject_id = self.cur_subject_id).first()
		qObj.status = 2 # 2 means the block has been submitted and can not be changed anymore
		next = self.rule_list[self.rule_key][1]
		fm = FormStructure()
		if self.rule_key[0] != 'f1b5' and self.rule_key[0] != 'f1b6':
			sObj.status = next
		elif self.rule_key[0] == 'f1b5' or self.rule_key[0] == 'f1b6':
			# its really tricky here
			# here get the field01 key which are approved, decline or referr. the next key means go to next stage from the field01. fiedle01 has the stage from approved or decline/...
			nextKey = qObj.field01
			sObj.status = next[nextKey]
		else:
			raise("internal error")
		pObj = model.PendingJob(g.user.user_id, fm.get_responsibility(sObj.status), self.cur_subject_id, sObj.status)
		db.session.add(pObj)
		db.session.add(newSection)
		db.session.add(sObj)
		db.session.add(qObj)
		db.session.commit()

	def on_allocate_number(self):
		# give history
		# delete previous pending job
		# give next pending job
		if not self.checked:
			raise('invalid calling order, update() should be called after check()!')
		from prams import db
		import model
		pObj = model.PendingJob.query.filter_by(subject_id = self.cur_subject_id, stage = self.cur_stage_name).first()
		db.session.delete(pObj)
		db.session.commit()

		from rule import FormStructure
		fm = FormStructure()
		sObj = model.Subject.query.filter_by(subject_id = self.cur_subject_id).first()
		newSection = model.History(g.user.user_id, g.user.occupation, 'allocated', self.cur_subject_id, self.cur_status)
		next = self.rule_list[self.rule_key][1]
		sObj.status = next
		pObj = model.PendingJob(g.user.user_id, fm.get_responsibility(next), self.cur_subject_id, next)
		db.session.add(newSection)
		db.session.add(pObj)
		db.session.add(sObj)
		db.session.commit()

	def on_reivew_subject(self):
		# give history
		# delete previous pending job
		# give next pending job
		if not self.checked:
			raise('invalid calling order, update() should be called after check()!')
		from prams import db
		import model
		pObj = model.PendingJob.query.filter_by(subject_id = self.cur_subject_id, stage = self.cur_stage_name).first()
		db.session.delete(pObj)
		db.session.commit()

		from rule import FormStructure
		fm = FormStructure()
		sObj = model.Subject.query.filter_by(subject_id = self.cur_subject_id).first()
		newSection = model.History(g.user.user_id, g.user.occupation, 'reviewed', self.cur_subject_id, self.cur_status)
		next = self.rule_list[self.rule_key][1]
		sObj.status = next
		a, b = fm.get_responsibility(next).split(' ')
		paObj = model.PendingJob(g.user.user_id, a, self.cur_subject_id, next)
		pbObj = model.PendingJob(g.user.user_id, b, self.cur_subject_id, next)
		db.session.add(newSection)
		db.session.add(paObj)
		db.session.add(pbObj)
		db.session.add(sObj)
		db.session.commit()

	def on_seal(self):
		# give history
		# delete previous pending job
		# give next pending job
		if not self.checked:
			raise('invalid calling order, update() should be called after check()!')
		from prams import db
		import model
		pObj = model.PendingJob.query.filter_by(subject_id = self.cur_subject_id, stage = self.cur_stage_name, to_user_occupation = g.user.occupation).first()
		db.session.delete(pObj)
		db.session.commit()

		from rule import FormStructure
		fm = FormStructure()
		sealers = set(fm.get_responsibility(self.cur_status).split(' '))
		sealers.remove(g.user.occupation)

		newSection = model.History(g.user.user_id, g.user.occupation, 'sealed', self.cur_subject_id, self.cur_status)

		apObj = model.PendingJob.query.filter_by(subject_id = self.cur_subject_id, stage = self.cur_stage_name, to_user_occupation = sealers.pop()).first()
		if apObj == None:
			next = self.rule_list[self.rule_key][1]
			sObj = model.Subject.query.filter_by(subject_id = self.cur_subject_id).first()
			db.session.add(sObj)
			sObj.status = next
		db.session.add(newSection)
		db.session.commit()
		
fieldTitle = {
# here are the dictionray
	'f1b1': {
		#fieldname ,  real title, html input type
		'subject_id': ['Establishment ID', 'TEXT'],
		'status': ['Status', 'TEXT'],
		'field01': ['Department/ School',  'TEXT'],
		'field02': ['Post Title',  'TEXT'],
		'field03': ['Current/Previous post holder\'s name', 'TEXT'],
		'field04': ['Is this a new post?',  'RADIO', ['Yes', 'No']],
		'field05': ['Is this a change or extension to the existing post?', 'RADIO', ['Yes', 'No']],
		'field06': ['Is this a replacement of an existing post holder?', 'RADIO', ['Yes', 'No']],
		'field07': ['Post reports to', 'TEXT'],
		'field08': ['Effective date', 'DATE'],
		'field09': ['End date if temporary',  'DATE'],
		'field10': ['Hours per week',  'TEXT'],
		'field11': ['Weeks per year',  'TEXT'],
		'field12': ['Grade & point',  'TEXT'],
		'field13': ['Rate of pay', 'TEXT'],
		'field14': ['Funding source: College',  'TEXT'],
		'field15': ['Funding source: External',  'TEXT'],
		'field16': ['Funding source: Departmental',  'TEXT'],
		'field17': ['Accout code/s: (3)',  'TEXT'],
		'field18': ['Accout code/s: (3)',  'TEXT'],
		'field19': ['Accout code/s: (8)', 'TEXT']},

	'f1b2': {
		'subject_id': ['Establishment ID', 'TEXT'],
		'status': ['Status', 'TEXT'],
		'field01': ['Please detail below the strategic and operational importance of this post', 'TEXT'],
		'field02': ['Job Description', 'TEXT'],
		'field03': ['Person Specification', 'TEXT'],
		'field04': ['Departmental Structure chart', 'TEXT'],
		'field05': ['Head of Department\'s Signature', 'TEXT'],
		'field06': ['Date', 'DATE']},

	'f1b3': {
		'subject_id': ['Establishment ID', 'TEXT'],
		'status': ['Status', 'TEXT'],
		'field01': ['Post Number', 'TEXT'],
		'field02': ['At Risk Register Checked', 'RADIO', ['Yes', 'No']],
		'field03': ['HERA Grade Checked', 'RADIO', ['Yes', 'No']],
		'field04': ['Comments & HR Implications', 'TEXT'],
		'field05': ['Signed', 'TEXT'],
		'field06': ['Date', 'DATE']},

	'f1b4': {
		'subject_id': ['Establishment ID', 'TEXT'],
		'status': ['Status', 'TEXT'],
 		'field01': ['Comments & Financial implications', 'TEXT'],
		'field02': ['Signed', 'TEXT'],
		'field03': ['Date', 'DATE']},

	'f1b5': {
		'subject_id': ['Establishment ID', 'TEXT'],
		'status': ['Status', 'TEXT'],
		'field01': [' ', 'RADIO', ['Approved', 'Declined', 'To be referred to Deputy Principal']],
		'field02': ['Comments', 'TEXT'],
		'field03': ['Signed', 'TEXT'],
		'field04': ['Date', 'DATE']},

	'f1b6': {
		'subject_id': ['Establishment ID', 'TEXT'],
		'status': ['Status', 'TEXT'],
		'field01': [' ', 'RADIO', ['Approved', 'Declined', 'To be referred to Planning Resources Committee']],
		'field02': ['Comments', 'TEXT'],
		'field03': ['Signed', 'TEXT'],
		'field04': ['Date', 'DATE']},
	## more block and form in the format of above could be added here
	}

occupationTitle = {
	'HOD': 'Head of Department',
	'HR': 'Human Resources',
	'MA': 'Management Accout',
	'DO': 'Director of Operations & Registrar/Faculty Dean',
	'DP': 'Deputy Principal',
	'ADM': 'Administractor'
	# more user type could be added here, but to remember to add corresponding rule in statemachine
}