import psycopg2

def create_cords_table(conn):
	try:
		cur = conn.cursor()

		query = f'''CREATE TABLE IF NOT EXISTS cords (
						item_name VARCHAR (255) PRIMARY KEY,
						item_code VARCHAR (255) NOT NULL,
						amount INT NOT NULL
					);'''

		cur.execute(query)
		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

def valid_code(conn, code: str) -> bool:
	try:
		cur = conn.cursor()
		query = 'SELECT item_code FROM cords;'
		cur.execute(query)
		res = cur.fetchall()
		cur.close()
		result = [x[0] for x in res]
		if code in result: return True
		else: return False

	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

def update_amount(conn, item_code: str, amount: int, mode: int):
	try:
		cur = conn.cursor()
		query = f"SELECT amount FROM cords WHERE item_code='{item_code}';"
		cur.execute(query)
		res = cur.fetchone()[0]

		if mode == 0:
			if res == 0: 
				return
			res = res-amount
		elif mode == 1: 
			res = res+amount
		
		query = f"UPDATE cords SET amount={res} WHERE item_code='{item_code}';"
		cur.execute(query)

		cur.close()
		conn.commit()

	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

def connect():
	conn = None
	try:
		print('Connecting to the PostgreSQL database...')
		conn = psycopg2.connect('dbname=reims user=pi')

		return conn
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)