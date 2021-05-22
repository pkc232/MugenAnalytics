from wand.image import Image
import time
import os
 

base = "/home/pratyush/Documents/Mugen_Analytics/ByPassCaptcha/TelaganaElectoralRolls/"

MIN_CONSTITUENCY_NO = 49
MAX_CONSTITUENCY_NO = 50

def convert_pdf_to_png(pdf_path, pdf_no, png_path):
	png_path_new = png_path
	png_path += str(pdf_no)
	png_path += "/"
	if not os.path.exists(png_path):
		os.makedirs(png_path)
	
	with Image(filename=pdf_path+str(pdf_no)+".pdf", resolution=300) as img:
		time.sleep(2)
		print('pages = ', len(img.sequence))
		img.compression_quality = 99
		with img.convert('png') as converted:
			time.sleep(2)
			converted.save(filename=png_path+str(pdf_no)+".png".format(img.sequence))


# def convert_pdf_to_png(pdf_path, pdf_no, png_path):
# 	png_path_new = png_path
	
# 	with Image(filename=pdf_path+str(pdf_no), resolution=300) as img:
#     	print('pages = ', len(img.sequence))
#     	img.compression_quality = 99
#     	with img.convert('png') as converted:
# 			converted.save(filename=png_path+"".format(img.sequence))

for cnum in range(MIN_CONSTITUENCY_NO, MAX_CONSTITUENCY_NO):
	path = base
	path += str(cnum)
	path += "/"
	pdf_path = path
	pdf_path += "pdfs/"
	png_path = path
	png_path += "pngs/"
	for pdf_no in range(12,41): 
		start = time.time()
		convert_pdf_to_png(pdf_path, pdf_no, png_path)
		end = time.time()
		print(end - start)
		print "Converted PDF NO", pdf_no
