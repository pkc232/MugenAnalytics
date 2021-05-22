import pytesseract
import sys
import argparse
try:
    import Image
except ImportError:
    from PIL import Image
from subprocess import check_output


def resolve(path):
	print("Resampling the Image")
	check_output(['convert', path, '-resample', '600', path])
	return pytesseract.image_to_string(Image.open(path),config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 6")

def solve_captcha(path):
	print('Resolving Captcha')
	captcha_text = resolve(path)
	return captcha_text