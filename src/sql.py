import psycopg2
from os import getenv
from src.log import log

def create_cords_table(conn):
	try:
		cur = conn.cursor()

		query = f'''CREATE TABLE IF NOT EXISTS cords (
						item VARCHAR (255) PRIMARY KEY,
						amount INT NOT NULL,
						connector VARCHAR (255) NOT NULL,
						color VARCHAR (255) NOT NULL,
						type VARCHAR (255) NOT NULL,
						length INT NOT NULL,
						class VARCHAR (255) NOT NULL,
						mode VARCHAR (255)
					);'''

		cur.execute(query)
		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

def valid_code(conn, code: str) -> bool:
	try:
		cur = conn.cursor()
		query = 'SELECT item FROM cords;'
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
		query = f"SELECT amount FROM cords WHERE item='{item_code}';"
		cur.execute(query)
		res = cur.fetchone()[0]

		if mode == 0:
			if res == 0: 
				return
			res = res-amount
		elif mode == 1: 
			res = res+amount
		
		query = f"UPDATE cords SET amount={res} WHERE item='{item_code}';"
		cur.execute(query)

		cur.close()
		conn.commit()

	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

def connect():
	conn = None
	try:
		conn = psycopg2.connect(f'host={getenv("DB_HOST")} dbname={getenv("DB_NAME")} user={getenv("DB_USER")}')

		return conn
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)