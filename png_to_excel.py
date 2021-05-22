"""
Module to convert pngs to text and
store them in an excel file
"""
# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
import pandas as pd
import pprint
import time

preprocess = "thresh" 
KEYS = ["Number", "Voter_ID", "Voter_Name", "Mother's_Name", "Father's_Name", "Husband's_Name", 
		"House_Number", "Age", "Sex"]
info = {}
info["Number"] = []
info["Voter_ID"] = []
info["Voter_Name"] = []
info["Mother's_Name"] = []
info["Father's_Name"] = []
info["Husband's_Name"] = []
info["House_Number"] = []
info["Age"] = []
info["Sex"] = []

base = "/home/pratyush/Documents/Mugen_Analytics/ByPassCaptcha/TelaganaElectoralRolls/"
excel_path = base
excel_path = base
excel_path += str(49)
excel_path += "/excels/"

cropped_path = base
cropped_path += str(49)
cropped_path += "/cropped/"



def write_to_excel(info, boothnum):
	"""
	This method is to write the dictionary containing the 
	electoral data into a csv file.
	"""
	excel_loc = excel_path+str(boothnum)
	# pprint.pprint(info)
	try:
		df = pd.DataFrame(info)
		# print df
		df = df.sort_values(["Number"])
		df = df[['Number','Voter_ID','Voter_Name',"Father's_Name",
			"Mother's_Name","Husband's_Name","House_Number","Age","Sex"]]
		df.to_csv(excel_loc+'.csv',index = False)
	except Exception as e:
		print str(e) 


GUARDIANS = ["Father's_Name", "Mother's_Name", "Husband's_Name"]


base_path = "/home/pratyush/Documents/Mugen_Analytics/ByPassCaptcha/TelaganaElectoralRolls/cropped-49/"

def pad_dictionary(obj):
	"""
	This method is to append NULL values into 
	the keys of the dictionary
	"""
	l = len(obj["Number"])
	for key in KEYS:
		l = max(len(obj[key]),l)
	for key in KEYS:
		if len(obj[key]) < l:
			obj[key].append("None")

def preprocess(text):
	text = text.replace(";",":")
	text = text.replace("Sex:", " ")
	text = text.replace("A1263","Age:")
	if "Male" in text:
		info["Sex"].append("Male".encode('utf-8').strip())
		text = text.replace("Male", " ")
	elif "Female" in text:
		info["Sex"].append("Female".encode('utf-8').strip())
		text = text.replace("Female", " ")
	text = text.replace("Agez", "Age:")

	try:
		lst = text.split("Age:")
		age = lst[1].split()[0]
		age = age.strip()
		info["Age"].append(age.encode('utf-8').strip())
		text = lst[0]
	except:
		info["Age"].append("None".encode('utf-8').strip())
		# print " NO age"

	lst = text.split("No:")
	try:
		house_number = '_'.join(lst[1].split())
		info["House_Number"].append(house_number.encode('utf-8').strip())
	except:
		info["House_Number"].append("None".encode('utf-8').strip())
	text = lst[0]
	text = text.replace("House","")
	
	# for guardian in GUARDIANS:
	# 	act_guardian = ' '.join(guardian.split('_'))
	# 	if act_guardian in text:
	# 		lst = text.split(act_guardian+":")
	# 		gname = '_'.join(lst[1].split())
	# 		info[guardian].append(gname)
	# 		text = lst[0]
	# 		break

	# print "Nodifiedddd"
	# print " "
	# print (text)

	return text

def store_in_excel(text):
	"""
	This method takes in the text converted from png
	and stores in the dictionary. 
	"""
	i=0
	text = preprocess(text)
	# text = text.replace("Agez","Age:")
	try:
		line_text = text.split()
		number = "99999"
		try:
			number = str(int(line_text[0]))
		except:
			number = "99999"
			line_text = ["None"] + line_text
		# print line_text, len(line_text)
		voter_id = line_text[1]
		if line_text[2][0:7] != "Elector":
			voter_id += line_text[2]
			line_text = [line_text[0],line_text[1:3]] + line_text[3:] 

		
		info["Number"].append(int(number))#.encode('utf-8').strip())
		info["Voter_ID"].append(voter_id.encode('utf-8').strip())

		remaining_line = ' '.join(line_text[2:])
		# print remaining_line
		values = remaining_line.split(":")

		phrase_1 = values[1].split()
		name =  []
		guardian = "None"
		for w in phrase_1:
			if w == "Husband's":
				guardian = "Husband's_Name"
				break
			elif w == "Father's":
				guardian = "Father's_Name"
				break
			elif w == "Mother's":
				guardian = "Mother's_Name"
				break
			else:
				name.append(w)
		voter_name = '_'.join(name)
		for guardian in GUARDIANS:
			voter_name = voter_name.replace(guardian, "")
		voter_name = voter_name.replace("Name","")
		voter_name = voter_name.replace("Father's","")
		voter_name = voter_name.replace("Mother's","")
		voter_name = voter_name.replace("Husband's","")
		voter_name = voter_name.replace("Mothel's","")
		
		info["Voter_Name"] .append(voter_name.encode('utf-8').strip())
		if guardian == "None":
			print "written"
			pad_dictionary(info)
			return


		phrase_2 = values[2].split()
		guardian_name = []
		for w in phrase_2:
			guardian_name.append(w)
		info[guardian].append('_'.join(guardian_name).encode('utf-8').strip())
		for w in GUARDIANS:
			if w != guardian:
				info[w].append("None".encode('utf-8').strip())
		# write_to_excel(info)
		print "written"
		pad_dictionary(info)
	except Exception as e:
		print(str(e))
		print "Not written"
		pad_dictionary(info)


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
		# print(text)
		# return
		# line_formator(text)
		store_in_excel(text)
	except:
		pass

for boothnum in range(40,41):
	for key in info:
		info[key] = []

	crop_location = cropped_path+str(boothnum)+"/"
	i=0
	for filename in os.listdir(crop_location):
		path = crop_location
		path+=filename
		convertImageToText(path)
		print boothnum, filename, "done"
		i = i+1

		
	# break
	write_to_excel(info,boothnum)
	time.sleep(5)
	
