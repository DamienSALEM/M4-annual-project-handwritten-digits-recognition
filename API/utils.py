import numpy as np
from PIL import Image
import base64
import io


def transform_image_png_to_pixels(image_png):
    print(image_png)
    image = base64.b64decode(image_png)
    image = Image.open(io.BytesIO(image))
    image = image.resize((28, 28))
    image = image.convert('L')
    image = np.array(image)
    image = image.reshape(1, 28, 28, 1)
    image = image.astype('float32')
    image /= 255
    print(image)
    return image
