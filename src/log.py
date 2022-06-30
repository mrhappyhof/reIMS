from os import path
from io import TextIOWrapper
from datetime import datetime

def log(data: str) -> None:
	file_path = 'reIMS.log'

	if path.exists(file_path):
		with open(file_path, 'a', newline='') as f:
				write_entry(f,data)
	else: 
		with open(file_path, 'w', newline='') as f:
				write_entry(f,data)

def write_entry(f: TextIOWrapper, x: str) -> None:
	time = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
	f.write(f'[{time}]\n{x}\n\n')