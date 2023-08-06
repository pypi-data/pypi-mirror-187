# 2023.1.19
import fileinput, sqlite3,traceback,sys,time

class Sqlsi(object): 
	def __init__(self, dbfile):  # gzjc.sqlsi 
		self.conn  =	sqlite3.connect(dbfile, check_same_thread=False) 
		self.conn.execute(f"create table if not exists si( s varchar(64) not null primary key, i int not null default 0) without rowid")
		self.conn.execute(f"create table if not exists st( s varchar(64) not null primary key, t text, cnt int not null default 0) without rowid")
		self.conn.execute('PRAGMA synchronous=OFF')
		self.conn.execute('PRAGMA case_sensitive_like = 1')
		self.conn.commit()

	def incr(self, s, i=1):
		try:
			if len(s) <= 64: 
				self.conn.execute(f"INSERT INTO si(s,i) VALUES(?,?) ON CONFLICT(s) DO UPDATE SET i = i + {i}", (s,i))
		except Exception as e:
			print ("ex:", e, s, i) 
			exc_type, exc_value, exc_obj = sys.exc_info() 	
			traceback.print_tb(exc_obj)

	def update(self, s, t):
		try:
			if len(s) <= 64: 
				self.conn.execute(f"INSERT OR IGNORE INTO st(s,t) VALUES (?,?)", (s,t))
		except Exception as e:
			print ("ex:", e, s, i) 
			exc_type, exc_value, exc_obj = sys.exc_info() 	
			traceback.print_tb(exc_obj)
	
	def commit(self):
		self.conn.commit() 

class util(object):
	def __init__(self): pass 

	def mynac(self, infile, host='127.0.0.1', port=3309,user='root',password='cikuutest!',db='nac' ): 
		''' submit gzjc.sqlsi(sqlite) to nac (mysql)  '''
		import pymysql
		my_conn = pymysql.connect(host=host,port=port,user='root',password='cikuutest!',db='nac')
		name = infile.split('.')[0]
		start = time.time()
		print ("started:", infile , name, flush=True)
		db = Sqlsi(infile) 
		with my_conn.cursor() as cursor: 
			cursor.execute(f"create table if not exists corpuslist( name varchar(100) not null primary key, en varchar(100), zh varchar(100), sntnum int not null default 0, lexnum int not null default 0) engine=myisam")
			cursor.execute(f"drop TABLE if exists {name}")
			cursor.execute(f"CREATE TABLE if not exists {name}(name varchar(64) COLLATE latin1_bin not null, attr varchar(128) COLLATE latin1_bin not null, count int not null default 0, primary key(name,attr) ) engine=myisam  DEFAULT CHARSET=latin1 COLLATE=latin1_bin") # not null default ''

			for sid, row in enumerate(db.conn.execute("select * from si")): 
				s,i = row
				arr = s.strip().split(':')
				cursor.execute(f"insert ignore into {name}(name, attr, count) values(%s, %s, %s)", (':'.join(arr[0:-1]), arr[-1], i))
				if (sid) % 100000 == 0 : 
					print (f"sid = {sid}, \t| {row} \t", round(time.time() - start,1), flush=True)
					my_conn.commit()
		print ( "finished:", infile) 

if __name__	== '__main__':
	import fire 
	fire.Fire(util)		


