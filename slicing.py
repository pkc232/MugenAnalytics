# https://www.pyimagesearch.com/2014/01/20/basic-image-manipulations-in-python-and-opencv-resizing-scaling-rotating-and-cropping/

# import the necessary packages
import cv2
import os

# load the image and show it
slice_width = 740
slice_height = 293
x = 65
y = 252

base = "/home/pratyush/Documents/Mugen_Analytics/ByPassCaptcha/TelaganaElectoralRolls/"
png_path = base
png_path += str(49)
png_path += "/pngs/"

cropped_path = base
cropped_path += str(49)
cropped_path += "/cropped/"

def slice(png_path, boothnum, cropped_path):
    png_pics = png_path
    png_pics += str(boothnum)
    png_pics += "/"

    cropped_pics = cropped_path
    cropped_pics += str(boothnum)
    cropped_pics += "/"

    if not os.path.exists(cropped_pics):
        os.makedirs(cropped_pics)
    i = 1
    for filename in os.listdir(png_pics):
        page_no = filename[:-4]
        page_no = int(page_no.split("-")[1])
        if page_no < 2:
            continue
        image = cv2.imread(png_pics+filename)
        # print "opened", png_pics+filename
        counter = 1
        start_position_y = y
        for row in range(1, 11):
            # print "row: ", row
            start_position_x = x
            for column in range(1, 4):
                # print "column: ", column
                try:
                    cropped = image[start_position_y:(start_position_y + slice_height),
                              start_position_x:(start_position_x + slice_width)]
                    start_position_x = start_position_x + slice_width + 10
                    cv2.imwrite(cropped_pics+"{}-{}-{}-{}.png".format(page_no, row, column, counter), cropped)
                    # print "writing", "{}-{}-{}-{}.png".format(page_no, row, column, counter)
                    counter = counter + 1
                except Exception as e:
                    print str(e)
            start_position_y = start_position_y + slice_height + 7

for bnum in range(11,41):
    slice(png_path, bnum, cropped_path)