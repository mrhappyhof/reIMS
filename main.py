#!/usr/bin/python3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.config import Config
from kivy.lang import Builder
from src.util import confirmation_popup
from src.usb import listen_to_rfid

Config.set('graphics', 'window_state', 'maximized')

class MainScreen(Screen):
	def check_out_button(self):
		App.get_running_app().mode = 0
		self.manager.get_screen('inv').mode_label = 'MODE: CHECK-OUT ITEMS'
		self.manager.current = 'inv'
	def check_in_button(self):
		App.get_running_app().mode = 1
		self.manager.get_screen('inv').mode_label = 'MODE: CHECK-IN ITEMS'
		self.manager.current = 'inv'

class LoginScreen(Screen):
	def login(self):
		self.clear_widgets()

		lay0 = FloatLayout()
		lay1 = AnchorLayout(anchor_x='center',anchor_y='top')
		lay2 = AnchorLayout(anchor_x='center',anchor_y='bottom')
		lay1.add_widget(Label(text='PLEASE LOG IN WITH YOUR KEYCARD',font_size= 0.7 * lay1.height,height=150,size_hint=(None, None)))
		lay2.add_widget(Image(source='res/img/keycard.png',size_hint=(.7, .7)))
		lay0.add_widget(lay1)
		lay0.add_widget(lay2)
		self.add_widget(lay0)
	
		user = listen_to_rfid()
		if user != None: 
			self.manager.get_screen('inv').login_label = f'LOGGED IN AS: {user}'
			self.manager.current = 'main' 
	def help(self):
		pass

class InventoryScreen(Screen):
	mode_label = StringProperty()
	login_label = StringProperty()

	def logout(self):
		def yes(popup, _):
			popup.dismiss(animation=False)
			self.manager.current = 'login'
		confirmation_popup('DO YOU WISH TO LOG OUT? (SCANNED ITEMS WILL BE DISCARDED)', yes)

	def back(self):
		def yes(popup, _):
			popup.dismiss(animation=False)
			self.manager.current = 'main'
		confirmation_popup('DO YOU WISH TO GO BACK? (SCANNED ITEMS WILL BE DISCARDED)', yes)

	def confirm(self):
		def yes(popup, _):
			popup.dismiss(animation=False)
		confirmation_popup('DO YOU WISH TO CONFIRM THE TRANSACTION? (SCANNED ITEMS WILL BE PROCESSED)', yes)

class WindowManager(ScreenManager):
	pass

class reIMSApp(App):
	title = 'reIMS - REHAU Inventory Management System'
	mode = None

reIMSApp().run()