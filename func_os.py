import psutil

def is_chrome_running():
	for proc in psutil.process_iter(['pid', 'name']):
		# This will check if there exists any process running with executable name
		if proc.info['name'] == 'chrome.exe':
			return True
	return None