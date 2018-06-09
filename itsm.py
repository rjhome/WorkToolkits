# coding utf-8

import argparse
import prettytable
import WorkToolkitDB


#get opt
parser = argparse.ArgumentParser()
parser.add_argument('operate', metavar='operate_type', type=str, choices=['s','u'], default='s', help='s: show ; u: update')
parser.add_argument('-f', nargs='?', metavar='finish_status', type=str, choices=['0','1'], default=0, help='0: unfinished ; 1: finished' )
parser.add_argument('-bt', nargs='?', metavar='begin_time', type=str, help='begin time : yyyymmdd (>=)')
parser.add_argument('-et', nargs='?', metavar='end_time', type=str, help='endtime : yyyymmdd (<)')
parser.add_argument('-id', nargs='?', metavar='ID', type=int, help='update itsm id : ID')
myOpt = parser.parse_args()


#get db session
myTaskSession = WorkToolkitDB.db.TaskSession().mySession

#config prettytable
itsmCols = ["id","task_id","title","accept_time","version_time","finish_status","memo","sys"]
pt = prettytable.PrettyTable(itsmCols)
pt.align["title"] = "l" # Left align city names



def show():
	"""show itsm task"""
	query = myTaskSession.query(WorkToolkitDB.db.Task)

	#filter finish_status 0/1/all
	if myOpt.f:
		query = query.filter(WorkToolkitDB.db.Task.finish_status == myOpt.f)

	#filter time >= bt and < et
	if myOpt.bt:
		query = query.filter(WorkToolkitDB.db.Task.version_time >= myOpt.bt)

	if myOpt.et:
		query = query.filter(WorkToolkitDB.db.Task.version_time < myOpt.et)
	
	data = query.order_by('version_time').all()

	for record in data:
			#record_arr = record.to_array()
			pt.add_row(record.to_array())

	print(pt)

	return 0

def update():
	"""set itsm task finished"""
	query = myTaskSession.query(WorkToolkitDB.db.Task)

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

	return 0


	#update id 



#main operate
if myOpt.operate == 's':
	show()
elif myOpt.operate =='u':
	update()














