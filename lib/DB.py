import MySQLdb

class DB:
	conn = None

	def connect(self):
		config = {}
		execfile("config.conf",config)
		
		self.conn = MySQLdb.connect(
			host=config['db_host'],
			user=config['db_user'],
			passwd=config['db_pass'],
			db=config['db_data']
		)

		self.conn.autocommit(True)	
		self.conn.set_character_set('utf8')

	def query(self, sql, args=None):
		try:
			cursor = self.conn.cursor()
			cursor.execute(sql, args)
		except (AttributeError, MySQLdb.OperationalError):
			self.connect()
			cursor = self.conn.cursor()
			cursor.execute(sql, args)

		return cursor