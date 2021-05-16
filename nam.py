from PIL import Image
import numpy as np
def get_Size(fileobject):
    fileobject.seek(0,2) # move the cursor to the end of the file
    size = fileobject.tell()
    return size
def read_img(filename):
    im = Image.open(filename,'r')
    width,height = im.size
    print("width = "+str(width))
    print("height = "+str(height))
    pixels = list(im.getdata())


    print(len(pixels))

# read_img("ScreenShot.png")
a = 225
print(str(a).__sizeof__())