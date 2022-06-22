from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config

Config.set('graphics', 'window_state', 'maximized')

class MainScreen(Screen):
	def check_out_button(self):
		self.manager.current = 'inv'
	def check_in_button(self):
		self.manager.current = 'inv'

class LoginScreen(Screen):
	pass

class PurchaseScreen(Screen):
	pass

class WindowManager(ScreenManager):
	pass

class reIMSApp(App):
	title = 'reIMS - REHAU Inventory Management System'

reIMSApp().run()