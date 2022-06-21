from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config

Config.set('graphics', 'window_state', 'maximized')

class InventoryScreen(Screen):
	pass

class MainScreen(Screen):
	def check_out_button(self):
		self.manager.current = 'inv'
	def check_in_button(self):
		self.manager.current = 'inv'

class WindowManager(ScreenManager):
	pass

class reIMSApp(App):
	title = 'reIMS - REHAU Inventory Management System'
	pass

reIMSApp().run()