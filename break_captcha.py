import captcha_download
import crop_captcha
import binarize
import captcha_solver
import time
import re
import os

url = "http://ceotserms2.telangana.gov.in/ts_erolls/Popuppage.aspx?partNumber=123&roll=EnglishMotherRoll&districtName=DIST_01&acname=AC_001&acnameeng=A001&acno=1&acnameurdu=001" 
base_url = "http://ceotserms2.telangana.gov.in/ts_erolls/Popuppage.aspx?partNumber=PNUM&roll=EnglishMotherRoll&districtName=DIST_01&"
constituency_number = "acname=AC_NUM&acnameeng=ANUM&acno=NUM&acnameurdu=NUM"
fname = ""

"""
Change the download directory to the path required by you.
"""

download_dir = "/home/pratyush/Documents/Mugen_Analytics/ByPassCaptcha/TelaganaElectoralRolls/"


MIN_CONSTITUENCY_NUMBER = 1
MAX_CONSTITUENCY_NUMBER = 100

MIN_BOOTH_NUMBER = 1
MAX_BOOTH_NUMBER = 300

def simplify(key):
	regex = re.compile('[^A-Z0-9]')
	key = regex.sub('', key)
	return key.upper()

def getCurrentDirectory(cnum):
	ndir = download_dir
	ndir += str(cnum)
	ndir += "/"
	return ndir

def open_pdf(link, cnum):
	"""
	This module opens the link in selenium
	Takes a screenshot and saves it
	Crops the captcha part
	Binarizes the captcha
	SOlves the captcha to get the text
	Fills in the text and clicks submit

	If captcha is correct the PDF opens for preview. 
	If captcha is wrong it tries again until the pdf opens. 
	"""
	ndir = getCurrentDirectory(cnum)
	if not os.path.exists(ndir):
		os.makedirs(ndir)

	driver = captcha_download.download_captcha(link, ndir)
	crop_captcha.crop_captcha()
	binarize.binarize()
	key = captcha_solver.resolve("modified.png") 
	key = simplify(key)
	rval = captcha_download.fill_captcha(driver,key)

	try:
		p = driver.find_element_by_id("lblCaptchaMessage")
		if p.text == 'Please enter correct captcha !':
			print "Wrong captcha"
			driver.close()
			return 0
		else:
			# time.sleep(40)
			while not os.path.isfile(fname):
				pass
			driver.close()
			return 1
	except:
		while not os.path.isfile(fname):
				pass
		driver.close()
		return 1

"""
We loop through all the constituencies and for each constituency we loop through 
all the polling booths.
"""
LB_NAGAR = 49
for cnum in range(LB_NAGAR, LB_NAGAR+1):
	constnum = str('%03d' %cnum)
	nd = constituency_number.replace('NUM',constnum)
	booth = 400
	current = getCurrentDirectory(cnum)
	while booth <= 509:
		part_number = str('%03d' %booth)
		nb = base_url.replace('PNUM',part_number)
		link = nb
		link += nd
		print link
		fname = current + "Popuppage.pdf"
		val = open_pdf(link, cnum)
		if val == 1:
			os.rename(fname,current + str(booth)+".pdf")
			booth = booth + 1

