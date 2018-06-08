import prettytable
import click
import WorkToolkitDB

itsmCols = ["id","task_id","title","accept_time","version_time","finish_status","memo","sys"]
pt = prettytable.PrettyTable(itsmCols)
pt.align["title"] = "l" # Left align city names
myTaskOp = WorkToolkitDB.db.TaskOp()




@click.command()
@click.option('--catalog', default=0, prompt='query catalog [0/1/2/3] : ' , help='0:all/1:unfinished/2:finished/3:nextweek unfinished' )
def itsm_show(catalog):
	data = myTaskOp.mySession.query(WorkToolkitDB.db.Task).order_by('version_time').all()
	for record in data:
		#record_arr = record.to_array()
		pt.add_row(record.to_array())

	click.echo(pt)


itsm_show()
