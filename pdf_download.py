"""
Module to download all electoral pdfs for a given constituency

@author : Pratyush Kamal Chaudhary
"""

import sys
import requests
import urllib2
import os

base_link 	= "http://ceoaperms1.ap.gov.in/Electoral_Rolls/PDFGeneration.aspx?urlPath=F:\RUNNING_APPLICATIONS_23012018\FINALROLLS_SSR_2018"
base_path = "/home/pratyush/Documents/Mugen_Analytics/PDF_DOC/AP/"
MAX_RANGE = 300

def create_constituency_url(electoral_constituency_number):
	"""
	This method creates the part of URL containing the constituency number
	"""
	constituency_url = "\AC_"
	constituency_url += str('%03d' % electoral_constituency_number)
	constituency_url += "\English\S01A"
	constituency_url += str('%03d' % electoral_constituency_number)
	return constituency_url


def electoral_doc_no(document_number):
	"""
	This method creates the part of URL containing the document number 
	"""
	document_url = "P"
	document_url += str('%03d' % document_number)
	document_url += ".PDF"
	return document_url


def create_url(electoral_constituency_number, document_number):
	"""
	This method creates the complete URL given the electoral constituency number and 
	the document number
	"""
	url = base_link
	url += create_constituency_url(electoral_constituency_number)
	url += electoral_doc_no(document_number)
	return url

def create_storage_path(electoral_constituency_number):
	"""
	This method generates the path string for creating a directory 
	for the given constituency number 
	"""
	path = base_path
	path += str('%03d' % electoral_constituency_number)
	return path

def download_file(download_url, path, document_number):
	"""
	This method downloads and stores the pdf specified as URL into the directory
	"""
	try:
	    response = urllib2.urlopen(download_url)
	    file_name = path
	    file_name += "/"
	    file_name += str('%03d' % document_number)
	    file_name += ".pdf"
	    file = open(file_name, 'w')
	    file.write(response.read())
	    file.close()
	    print("Completed document number ", document_number)    	
	    return 1
	except urllib2.HTTPError, e:
	    print(e.code)
	    return 0

def downlodad_electoral_pdfs(electoral_constituency_number):
	"""
	This method downloads all the electoral pdfs for the constituency specified
	It goes to a MAX_RANGE and if the URL breaks in between it returns
	"""
	path = create_storage_path(electoral_constituency_number)
	print 'for constituency ', electoral_constituency_number
	if not os.path.exists(path):
			os.makedirs(path)
	for number in range(1,MAX_RANGE):
		download_url = create_url(electoral_constituency_number, number)
		print download_url
		return_val = download_file(download_url, path, number)
		if return_val == 0:
			break

"""
Sample :
download_electoral_pdfs(98)
"""
