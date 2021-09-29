import time
import getpass
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import http.client
import socket
import os
import pprint

# importamos librerias necesarias para las funciones
import re

# importamos funciones de selenium
from kiwiscripts import fsel

# importamos variables globales
from globales import *

# importamos funciones custom
import func_os
import func_selenium
import func_texto

def run():
	os.system("taskkill /im chrome.exe /f")
	chromeOptions = Options()
	chromeOptions.add_argument("--start-maximized")
	chromeOptions.add_argument(f"--user-data-dir=C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Google\\Chrome\\User Data")
	chromeOptions.add_argument(f"--profile-directory=Default")
	global driver
	driver = webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions)
	driver.implicitly_wait(15)
	driver.get('https://google.com/')
	writeSession(driver)
	print('Finished Initiating Chrome')

def writeSession(driver):
	url = driver.command_executor._url
	session_id = driver.session_id
	f = open("sessioninfo.txt", "w")
	f.write(f"{url}\n")
	f.write(f"{session_id}")
	f.close()
	print('Wrote webdriver session details')

class Scraper():
	def __init__(self):
	  self.driver = attachToSession()

	def getCopyAi(self):
		try:
			driver = self.driver
			driver.get("https://www.copy.ai/app")
			time.sleep(1)
		except Exception as e:
			raise e

	def getCopyAiCompleto(self, keyword):
		try:
			'''
			if func_os.is_chrome_running() is None:
				# si ya hay una instancia de chrome
				# matamos y ejecutamos /run
				driver = run(iniciar)
			'''

			driver = self.driver
			action = ActionChains(driver)

			# cargamos URL
			self.getCopyAi()

			titulos_validos = []
			
			# copyai
			titulos_ai = self.getCopyAiTitulos(keyword)
			if len(titulos_ai) > 0:
				# comprobamos titulos
				i = 0
				while i < len(titulos_ai):
					if func_texto.comprobarKwEnTexto(keyword, titulos_ai[i]):
						titulos_validos.append(titulos_ai[i])
					i += 1
			else:
				# do something
				return 'por hacer titulos_ai'

			# google
			preguntas_google = func_selenium.getPreguntasGoogle(keyword, driver)
			if preguntas_google is not None and len(preguntas_google) > 0:
				# comprobamos titulos
				i = 0
				while i < len(preguntas_google):
					if func_texto.comprobarKwEnTexto(keyword, preguntas_google[i]):
						titulos_validos.append(preguntas_google[i])
					i += 1
			else:
				return 'por hacer preguntas_google'

			'''
			# underdash google
			preguntas_underdash = func_selenium.getPreguntasGoogleUnderDash(keyword, driver)
			if len(preguntas_underdash) > 0:
				# comprobamos titulos
				i = 0
				while i < len(preguntas_underdash):
					if func_texto.comprobarKwEnTexto(keyword, preguntas_underdash[i]):
						titulos_validos.append(preguntas_underdash[i])
					i += 1
			else:
				return 'por hacer preguntas_underdash'
			'''

			if len(titulos_validos) > 0:
				i = 0
				while i < len(titulos_validos):
					if func_texto.is_question(titulos_validos[i]) is None:
						titulos_validos.pop(i)
					else:
						i += 1

			if len(titulos_validos) > 0:
				# iteramos array
				result = ''
				for titulo in titulos_validos:
					# sacamos texto por cada titulo
					respuesta = self.getCopyAiTexto(titulo)
					result += f"<h2>{titulo}</h2>{respuesta}"

				# devolvemos result
				return result
			else:
				return None

		except Exception as e:
			print(e)
			raise e

	def getCopyAiTitulos(self, termino):
		try:
			driver = self.driver
			action = ActionChains(driver)

			# cargamos URL
			self.getCopyAi()

			# fb headlines.
			fsel.click(driver, "//a[@data-name='Facebook Headlines']")

			# idiomas
			fsel.hover(driver, "//div[@id='w-dropdown-toggle-1']", 1)
			fsel.ver(driver, "//nav[@id='w-dropdown-list-1']/a[@data-code='ES']")
			fsel.click(driver, "//nav[@id='w-dropdown-list-1']/a[@data-code='ES']", 1)

			fsel.hover(driver, "//div[@id='w-dropdown-toggle-2']", 1)
			fsel.ver(driver, "//nav[@id='w-dropdown-list-2']/a[@data-code='ES']")
			fsel.click(driver, "//nav[@id='w-dropdown-list-2']/a[@data-code='ES']", 1)
			
			# kw
			fsel.clear(driver, "//textarea[@id='product-description']")
			fsel.escribir(driver, "//textarea[@id='product-description']", termino, 1)
			fsel.click(driver, "//a[@id='create-button']", 1)

			# datos
			time.sleep(5)
			while True:
				try:
					driver.find_element_by_xpath("//body")
					titulos = driver.find_elements_by_xpath("//div[contains(@id, 'idea-') and contains(@class,'new-')]")
					break
				except Exception as e:
					print("aun no hay resultados, esperando 5seg mas")
					time.sleep(5)

			# creamos array
			result = []
			for titulo in titulos:
				try:
					tit = titulo.find_element_by_xpath('.').get_attribute('original_text')
					result.append(tit)
				except Exception as e:
					print(e)
					continue

			return result

		except Exception as e:
			print(e)
			raise e

	def getCopyAiTexto(self, keyword):
		try:
			driver = self.driver
			action = ActionChains(driver)
			
			# cargamos URL
			self.getCopyAi()

			# blog intros
			fsel.click(driver, "//a[@data-name='Blog Intros']")

			# idiomas
			fsel.hover(driver, "//div[@id='w-dropdown-toggle-1']")
			fsel.click(driver, "//nav[@id='w-dropdown-list-1']/a[@data-code='ES']")

			fsel.hover(driver, "//div[@id='w-dropdown-toggle-2']")
			fsel.click(driver, "//nav[@id='w-dropdown-list-2']/a[@data-code='ES']")
			
			# kw
			fsel.clear(driver, "//textarea[@id='product-description']")
			fsel.escribir(driver, "//textarea[@id='product-description']", keyword)
			fsel.click(driver, "//a[@id='create-button']")

			time.sleep(5)
			while True:
				try:
					driver.find_element_by_xpath("//body")
					titulos = driver.find_elements_by_xpath("//div[contains(@id, 'idea-') and contains(@class,'new-')]")
					break
				except Exception as e:
					print("aun no hay resultados, esperando 5seg mas")
					time.sleep(5)

			# creamos cadena
			result = ''
			for titulo in titulos:
				try:
					texto = titulo.find_element_by_xpath('.').get_attribute('original_text')
					result += f"<p>{texto}</p>"
				except Exception as e:
					print(e)
					continue

			return result

		except Exception as e:
			print(e)
			raise e


def attachToSession():
	# Code Reference : https://stackoverflow.com/a/48194907/11217153
	# The stackover flow answer was adapted. 
	f = open("sessioninfo.txt", "r")
	lines = f.readlines()
	url = lines[0]
	session_id = lines[1]
	session_id.strip()
	original_execute = WebDriver.execute
	def new_command_execute(self, command, params=None):
		if command == "newSession":
			# Mock the response
			return {'success': 0, 'value': None, 'sessionId': session_id}
		else:
			return original_execute(self, command, params)
	# Patch the function before creating the driver object
	WebDriver.execute = new_command_execute
	driver = webdriver.Remote(command_executor=url, desired_capabilities={})
	driver.session_id = session_id
	# Replace the patched function with original function
	WebDriver.execute = original_execute
	return driver
