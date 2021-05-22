import cv2
import numpy as np

def binarize():
	img = cv2.imread('cropped.png',0)
	ret,thresh_img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
	cv2.imwrite("modified.png", thresh_img)