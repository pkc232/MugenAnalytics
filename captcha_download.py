import urllib
import time
from selenium import webdriver

 
def download_captcha(url, download_dir):
	options = webdriver.ChromeOptions()
	prefs = {"plugins.always_open_pdf_externally": True, "download.default_directory": download_dir}
	options.add_experimental_option("prefs",prefs)

	driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", chrome_options=options)

	driver.get(url)
	try:
		driver.maximize_window()
	except:
		pass
	driver.save_screenshot("screenshot.png")
	return driver

def fill_captcha(driver, key):
	captcha_text = driver.find_element_by_id("txtVerificationCode")
	captcha_text.send_keys(key)
	driver.find_element_by_name("btnSubmit").click()
	return driver


