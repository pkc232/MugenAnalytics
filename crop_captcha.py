from PIL import Image

def crop_captcha():
	"""
	This method crops the screenshot for the captcha part. 
	"""
	img = Image.open("screenshot.png")
	area = (160, 10, 350, 60)
	cropped_img = img.crop(area)
	cropped_img.save("cropped.png")
