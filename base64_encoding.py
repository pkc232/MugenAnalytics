import base64
from PIL import Image

with open("captch3.aspx", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
with open("imageToSave.png", "rb") as fh:
    fh.write(base64.decodebytes(encoded_string))