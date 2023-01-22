from PIL import Image
import os

path = r"D:\PyGame\Hocus Pocus\Hocus Pocus\graphics"

size_multiplier = 3

for root, dirs, files in os.walk(path):
    for name in files:
        print(name)
        if name.endswith(".png"):
            im = Image.open(os.path.join(root, name))
            width, height = im.size
            newsize = (width * size_multiplier, height * size_multiplier)
            im1 = im.resize(newsize, Image.NEAREST)
            im1.save(os.path.join(root, name))

    # for file in files:
    #     if file.endswith('.png'):
    #         im = Image.open(os.path.join(path,))

# # Opens a image in RGB mode
# im = Image.open(r"C:\Users\System-Pc\Desktop\ybear.jpg")
 
# # Size of the image in pixels (size of original image)
# # (This is not mandatory)
# width, height = im.size
 
# # Setting the points for cropped image
# left = 4
# top = height / 5
# right = 154
# bottom = 3 * height / 5
 
# # Cropped image of above dimension
# # (It will not change original image)
# im1 = im.crop((left, top, right, bottom))
# newsize = (300, 300)
# im1 = im1.resize(newsize)
# # Shows the image in image viewer
# im1.show()