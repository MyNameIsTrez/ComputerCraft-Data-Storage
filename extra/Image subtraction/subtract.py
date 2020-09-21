from PIL import Image
import numpy as np

# image1Path = "./Error diffusion/redmean numpy broken.png"
# image2Path = "./Error diffusion/redmean working.png"

image1Path = "./No error diffusion/redmean numpy broken.png"
image2Path = "./No error diffusion/redmean working.png"

image1 = Image.open(image1Path)
image2 = Image.open(image2Path)

buffer1 = np.asarray(image1)
buffer2 = np.asarray(image2)

buffer3 = np.subtract(buffer1, buffer2)

print("Images are identical: {}".format(np.all(buffer3 == 0)))

differenceImage = Image.fromarray(buffer3)

image1.show()
image2.show()
differenceImage.show()

# differenceImage.save("difference.png")