# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text


engine = sqlalchemy.create_engine('sqlite:////Users/xuxiaoyi/Documents/MD_records/telecomwork.db', 
	connect_args={'check_same_thread': False}, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

"""
CREATE TABLE "task" ( 
	"id" integer PRIMARY KEY AUTOINCREMENT NOT NULL, 
	"task_id" char(20) NOT NULL, 
	title" varchar(255), 
	"accept_time" char(14), 
	"version_time" char(14), 
	"memo" text(500), 
	"finish_status" char(10), 
	"sys" char(128) 
	)
"""

class Task(Base):
	__tablename__ = 'task'

	id = Column(Integer, primary_key=True)
	task_id = Column(String)
	title = Column(String)
	accept_time = Column(String)
	version_time = Column(String)
	finish_status = Column(String)
	memo = Column(String)
	sys = Column(String)


	def __repr__(self):
		return "<Task(id='%s' title='%s' accept_time='%s' version_time='%s' finish_status='%s')> \n" % (self.id, self.title , self.accept_time, self.version_time, self.finish_status)

	def to_array(self):
		return [self.id,self.task_id,self.title,self.accept_time,self.version_time,self.finish_status,self.memo,self.sys]


class TaskSession(object):
	"""
		operate table task
	"""

	def __init__(self):
		"""
			filter : None (All), 
			finish_status None (All) 
		"""

		self.mySession = Session()

