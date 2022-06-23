from functools import partial
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

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