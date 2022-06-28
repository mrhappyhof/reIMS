from functools import partial
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from collections import Counter
from src.sql import connect, create_cords_table, valid_code, update_amount

def confirmation_popup(title_text, doit):
	layout = BoxLayout(orientation = 'horizontal', spacing=10, padding=10)
	btn1 = Button(text='YES',font_size= 0.9 * layout.height, color= '#000000',background_color= '#FF0000',background_normal= '',background_pressed= '')
	btn2 = Button(text='NO',font_size= 0.9 * layout.height, color= '#000000',background_color= '#00FF00',background_normal= '',background_pressed= '')
	layout.add_widget(btn1)
	layout.add_widget(btn2)

	pop = Popup(title=title_text,title_size=0.3 * layout.height,content=layout,size_hint=(.6, .6))

	def no(_):
		pop.dismiss(animation=False)

	btn1.bind(on_press=partial(doit, pop))
	btn2.bind(on_press=no)

	pop.open()

def wait_popup() -> Popup:
	layout = BoxLayout(spacing=10, padding=10)
	img = Image(source='res/img/loading.gif',size_hint_x=0.4 * layout.height,anim_delay=0.1,mipmap= True,allow_stretch=False)
	layout.add_widget(img)
	pop = Popup(title='PLEASE WAIT. OPERATION IN PROGRESS.',title_size=0.4 * layout.height,content=layout,size_hint=(.6, .6))
	pop.open()
	return pop

def process_items(scans: list, mode: int):
	items = dict(Counter(scans))
	ex_items = {}

	conn = connect()
	create_cords_table(conn)

	for k,v in items.items():
		if not valid_code(conn,k): continue
		ex_items[k] = v

	for k,v in ex_items.items():
		update_amount(conn,k,v,mode)

	conn.close()
	print('Database connection closed.')