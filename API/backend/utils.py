import numpy as np
from PIL import Image
import base64
import io


def transform_image_png_to_pixels(image_png):
    format, imgstr = image_png.split(';base64,')
    image = base64.b64decode(imgstr)
    image = Image.open(io.BytesIO(image))
    image = image.resize((28, 28))
    image = image.convert('L')
    pixels = list(image.getdata())
    return pixels
