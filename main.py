#!/usr/bin/python3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.config import Config
from kivy.clock import Clock, mainthread
from src.util import confirmation_popup, process_items, gen_item_string
from src.usb import listen_to_rfid, listen_to_scanner
from src.log import log
from collections import Counter
from dotenv import load_dotenv
import threading
import asyncio
import time

load_dotenv()
Config.set('graphics', 'window_state', 'maximized')

class SplashScreen(Screen):
	def on_enter(self):
		Clock.schedule_once(self.load)
	def load(self, _):
		self.manager.current = 'login'

class LoginScreen(Screen):
	user = None
	def on_enter(self):
		Clock.schedule_once(self.login)

	def login(self, _):
		self.user = listen_to_rfid()
		if self.user != None: 
			self.manager.get_screen('main').login_label = f'LOGGED IN AS: {self.user}'
			self.manager.current = 'main'
			log(f'{self.user} logged in')

class MainScreen(Screen):
	mode_label = StringProperty('SCAN MODE: CHECK-OUT')
	login_label = StringProperty()
	scan_label = StringProperty('SCANNED ITEMS: 0')
	scanned_items = StringProperty('SCANNED BARCODES:')
	item_string = None
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
		self.item_string = gen_item_string(self.scans)
		self.manager.get_screen('main').scan_label = f'SCANNED ITEMS: {len(self.scans)}'
		self.manager.get_screen('main').scanned_items = f'SCANNED BARCODES:\n\n{self.item_string}'
		
	def check_out_button(self):
		App.get_running_app().mode = 0
		self.ids.in_btn.disabled = False
		self.ids.out_btn.disabled = True
		self.mode_label = 'SCAN MODE: CHECK-OUT'

	def check_in_button(self):
		App.get_running_app().mode = 1
		self.ids.out_btn.disabled = False
		self.ids.in_btn.disabled = True
		self.mode_label = 'SCAN MODE: CHECK-IN'

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
			log(f'{self.manager.get_screen("login").user} logged out')
		confirmation_popup('DO YOU WISH TO LOG OUT? (SCANNED ITEMS WILL BE DISCARDED)', yes)

	@mainthread
	def confirm(self):
		def yes(popup, _):
			mode = App.get_running_app().mode
			popup.dismiss(animation=False)
			self.stop_thread.set()
			process_items(self.scans, mode)
			self.reset_values()
			self.manager.current = 'login'

			if mode == 0: log(f'{self.manager.get_screen("login").user} removed:\n{self.item_string}')
			elif mode == 1: log(f'{self.manager.get_screen("login").user} added:\n{self.item_string}')
			log(f'{self.manager.get_screen("login").user} logged out')
		confirmation_popup('DO YOU WISH TO CONFIRM THE TRANSACTION? (SCANNED ITEMS WILL BE PROCESSED)', yes)

class WindowManager(ScreenManager):
	stop = threading.Event()

class reIMSApp(App):
	def on_stop(self):
		self.root.stop.set()
	title = 'reIMS - REHAU Inventory Management System | SUPPORT: Adrian Fernandez Castro, reh 7667, EDU'
	mode = 0
reIMSApp().run()