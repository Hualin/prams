# for rebuilding the user data set again
# first you should delete prams.db!!!
from prams import db
from model import *
db.create_all()
db.session.commit()

# user_name, password, occupation
test_users = [
	['Jose', 'bacon', 'HOD', 'jose@cs.xxxx.ac.uk'],
	['Fang', 'ddddd', 'HR', 'fang@gmail.com'],
	['Judy', 'ddddd', 'MA', 'judy@gmail.com'],
	['Echo', 'ddddd', 'DO', 'Echo@sina.com'],
	['Popy', 'ddddd', 'DP', 'popy@hotmail.com'],
	['Siyu', 'ddddd', 'ADM', 'siyu@outlook.com'],
	]
from model import User
from werkzeug import check_password_hash, generate_password_hash

for tu in test_users:
	newUsr = User(	tu[0],
			tu[2],
			generate_password_hash(tu[1]),
			tu[3])
	db.session.add(newUsr)
	db.session.commit()

print 'all done'
