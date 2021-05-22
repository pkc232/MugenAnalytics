from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
import pandas as pd
import pprint

def convertImageToText(image_path):
	try:
		image = cv2.imread(image_path)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# check to see if we should apply thresholding to preprocess the
		# image
		if preprocess == "thresh":
			gray = cv2.threshold(gray, 0, 255,
				cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
		 
		# make a check to see if median blurring should be done to remove
		# noise
		elif preprocess == "blur":
			gray = cv2.medianBlur(gray, 3)
		filename = "{}.png".format(os.getpid())
		cv2.imwrite(filename, gray)
		# load the image as a PIL/Pillow image, apply OCR, and then delete
		# the temporary file
		text = pytesseract.image_to_string(Image.open(filename))
		os.remove(filename)
		print(text)
		# line_formator(text)
		# store_in_excel(text)
	except Exception as e:
		print str(e)
		pass

convertImageToText("Captcha2.jpeg")
