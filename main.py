#!/usr/bin/python3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.config import Config
from kivy.clock import Clock
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
	def on_enter(self):
		Clock.schedule_once(self.login)
	def login(self, _):
		user = listen_to_rfid()
		if user != None: 
			self.manager.get_screen('inv').login_label = f'LOGGED IN AS: {user}'
			self.manager.current = 'main'

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