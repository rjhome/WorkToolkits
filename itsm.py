# coding utf-8

import argparse
import prettytable
import WorkToolkitDB
import re
import datetime


#get opt
parser = argparse.ArgumentParser()
parser.add_argument('operate', metavar='operate_type', type=str, choices=['s','u','a','d'], default='s', help='s: show ; u: update ; a: add ; d: delete')
parser.add_argument('-f', nargs='?', metavar='finish_status', type=str, choices=['0','1'], default=0, help='0: unfinished ; 1: finished' )
parser.add_argument('-bt', nargs='?', metavar='begin_time', type=str, help='begin_time : yyyymmdd (>=)')
parser.add_argument('-et', nargs='?', metavar='end_time', type=str, help='end_time : yyyymmdd (<)')
parser.add_argument('-abt', nargs='?', metavar='accept_time', type=str, help='accept_time (begin): yyyymmdd (>=) | 0 for today')
parser.add_argument('-aet', nargs='?', metavar='accept_time', type=str, help='accept_time (end): yyyymmdd (<)')
parser.add_argument('-id', nargs='?', metavar='ID1,ID2,ID3...', type=str, help='update/delete itsm id : [id1,id2,id3....]')
myOpt = parser.parse_args()


#get db session
myTaskSession = WorkToolkitDB.db.TaskSession().mySession

#config prettytable
itsmCols = ["id","task_id","title","accept_time","version_time","finish_status","memo","sys"]
pt = prettytable.PrettyTable(itsmCols)
pt.align["title"] = "l" # Left align city names



def _show():
	"""show itsm task"""
	query = myTaskSession.query(WorkToolkitDB.db.Task)

	#filter finish_status 0/1/all
	if myOpt.f:
		query = query.filter(WorkToolkitDB.db.Task.finish_status == myOpt.f)

	#filter versopm_time >= bt and < et
	if myOpt.bt:
		query = query.filter(WorkToolkitDB.db.Task.version_time >= myOpt.bt)
	if myOpt.et:
		query = query.filter(WorkToolkitDB.db.Task.version_time < myOpt.et)

	#filter accept_time >= abt < aet
	if myOpt.abt:
		if myOpt.abt == '0':
			myOpt.abt = datetime.datetime.now().strftime('%Y%m%d')
		query = query.filter(WorkToolkitDB.db.Task.accept_time >= myOpt.abt)
	if myOpt.aet:
		query = query.filter(WorkToolkitDB.db.Task.accept_time < myOpt.aet)

	#filter id
	if myOpt.aet:
		query = query.filter(WorkToolkitDB.db.Task.accept_time < myOpt.aet)

	#print(myOpt)
	data = query.order_by('version_time').all()

	for record in data:
			#record_arr = record.to_array()
			pt.add_row(record.to_array())

	print(pt)

	return 0

def _update():
	"""set itsm task finished"""
	query = myTaskSession.query(WorkToolkitDB.db.Task)

	IDStr = myOpt.id
	IDs = re.split(',', IDStr)

	if len(IDs) == 0:
		print('ERR: no add task input')
		return 1

	#set default finsih_status if not given
	if not myOpt.f:
		myOpt.f = 1

	for ID in IDs:
		query.filter(WorkToolkitDB.db.Task.id == ID).update({WorkToolkitDB.db.Task.finish_status: myOpt.f})

	#commit
	myTaskSession.commit()

	"""
	#ERR: not given itsm id for update 
	if not myOpt.id:
		print('Error: no itsm id given for update finish_status to 1')
		return 1
	#set default finsih_status if not given
	if not myOpt.f:
		myOpt.f = 1

	
	query.filter(WorkToolkitDB.db.Task.id == myOpt.id).update({'finish_status': myOpt.f})
	myTaskSession.commit()

	
	data = query.filter(WorkToolkitDB.db.Task.id == myOpt.id).all()
	for record in data:
			#record_arr = record.to_array()
			pt.add_row(record.to_array())

	print(pt)
	"""

	return 0

def _add():
	"""add one itsm task"""
	query = myTaskSession.query(WorkToolkitDB.db.Task)
	myTask = WorkToolkitDB.db.Task()

	addDataStr = input('输入记录 格式: "task_id","title","version_time","memo","sys" :\n    >')
	addData = re.split('\s',addDataStr)

	if len(addData) != 5:
		print('ERR: no add task input')
		return 1

	#create record
	myTask.task_id = addData[0]
	myTask.title = addData[1]
	myTask.version_time = addData[2]
	myTask.memo = addData[3]
	myTask.sys = addData[4]

	#init accept_time , finish_status
	myTask.accept_time = datetime.datetime.now().strftime('%Y%m%d')
	myTask.finish_status = 0

	myTaskSession.add_all([myTask])
	myTaskSession.commit()

	return 0


def _delete():
	"""add one itsm task"""
	query = myTaskSession.query(WorkToolkitDB.db.Task)

	IDStr = myOpt.id
	IDs = re.split(',', IDStr)

	if len(IDs) == 0:
		print('ERR: no deleting id input')
		return 1

	for ID in IDs:
		myTask = query.get(ID)
		myTaskSession.delete(myTask)

	
	myTaskSession.commit()

	return 0




#main operate
if myOpt.operate == 's':
	_show()
elif myOpt.operate =='u':
	_update()
elif myOpt.operate == 'a':
	_add()
elif myOpt.operate == 'd':
	_delete()
















