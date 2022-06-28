#!/usr/bin/python3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.config import Config
from kivy.clock import Clock, mainthread
from src.util import confirmation_popup, wait_popup, process_items
from src.usb import listen_to_rfid, listen_to_scanner
from collections import Counter
from dotenv import load_dotenv
import threading
import asyncio
import time

load_dotenv()
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

class SplashScreen(Screen):
	def on_enter(self):
		Clock.schedule_once(self.load)
	def load(self, _):
		self.manager.current = 'login'

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
	scan_label = StringProperty('SCANNED ITEMS: 0')
	scanned_items = StringProperty('SCANNED BARCODES:')
	scans = []
	thread = None
	stop_thread = threading.Event()

	def on_enter(self):
		Clock.schedule_once(self.start_thread)

	def start_thread(self, _):
		loop = asyncio.new_event_loop()
		thread = threading.Thread(target=self.await_scans, args=(loop,))
		thread.start()

	def await_scans(self, loop):
		asyncio.set_event_loop(loop)
		while not self.stop_thread.isSet():
			try:
				id = listen_to_scanner()
				self.scans.append(id)
				self.update_scan_list()
			except Exception: break

	@mainthread
	def update_scan_list(self):
		items = dict(Counter(self.scans))
		item_string = ' '.join([f'[{v}x {k}]' for k, v in items.items()])
		self.manager.get_screen('inv').scan_label = f'SCANNED ITEMS: {len(self.scans)}'
		self.manager.get_screen('inv').scanned_items = f'SCANNED BARCODES:\n\n{item_string}'
		
	def reset_values(self):
		self.scan_label = 'SCANNED ITEMS: 0'
		self.scanned_items = 'SCANNED BARCODES:'
		self.scans = []
		self.stop_thread = threading.Event()

	def logout(self):
		def yes(popup, _):
			popup.dismiss(animation=False)
			self.stop_thread.set()
			self.reset_values()
			self.manager.current = 'login'
		confirmation_popup('DO YOU WISH TO LOG OUT? (SCANNED ITEMS WILL BE DISCARDED)', yes)

	def back(self):
		def yes(popup, _):
			popup.dismiss(animation=False)
			self.stop_thread.set()
			self.reset_values()
			self.manager.current = 'main'
		confirmation_popup('DO YOU WISH TO GO BACK? (SCANNED ITEMS WILL BE DISCARDED)', yes)

	def confirm(self):
		def yes(popup, _):
			popup.dismiss(animation=False)
			self.stop_thread.set()
			pop = wait_popup()
			process_items(self.scans, App.get_running_app().mode)
			pop.dismiss(animation=False)
			self.reset_values()
			self.manager.current = 'login'
		confirmation_popup('DO YOU WISH TO CONFIRM THE TRANSACTION? (SCANNED ITEMS WILL BE PROCESSED)', yes)

class WindowManager(ScreenManager):
	stop = threading.Event()

class reIMSApp(App):
	def on_stop(self):
		self.root.stop.set()
	title = 'reIMS - REHAU Inventory Management System | SUPPORT: Adrian Fernandez Castro, reh 7667, EDU'
	mode = None
reIMSApp().run()