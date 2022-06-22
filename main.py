from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.config import Config

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
	pass

class InventoryScreen(Screen):
	mode_label = StringProperty()

class WindowManager(ScreenManager):
	pass

class reIMSApp(App):
	title = 'reIMS - REHAU Inventory Management System'
	mode = None

reIMSApp().run()