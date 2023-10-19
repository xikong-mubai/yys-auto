from PIL import Image

import os

os.chdir('./img-1')

for i in os.listdir('./'):
    if os.path.isdir(i):
        for j in os.listdir('./'+i):
            img = Image.open('./'+i+'/'+j)
            x,y = img.size
            x = 9 ; y -= 45
            print(i,j)
            print(img.getpixel((8,y)))
            exit()

            tmp = Image.new('RGB',img.size,0)