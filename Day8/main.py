import math
import numpy as np
from PIL import Image

BLACK = 0
WHITE = 1
TRANSPARENT = 2

def load_image(file, width, height):
    with open(file, "r") as f:
        data = f.read()
        layer_length = width * height
        layers = [data[i : i + layer_length] for i in range(0, len(data), layer_length)]
        result = []
        for layer in layers:
            result.append(list(map(int, list(layer))))
        return result

def get_pixel_from_layer(layer, width, height, x, y):
    return layer[x + y * width]

def decode_image(image, width, height):
    result = np.zeros(width * height)
    for j in range(height):
        for i in range(width):
            for layer in image:
                pixel = get_pixel_from_layer(layer, width, height, i, j)
                if pixel != TRANSPARENT:
                    result[i + j * width] = pixel
                    break
    return result

image = load_image("image.txt", 25, 6)

zero_pixels = 0
max_one_pixels = 0
max_two_pixels = 0

min_zeros = math.inf
max_layer = None

for layer in image:
    zero_pixels = 0
    one_pixels = 0
    two_pixels = 0
    for pixel in layer:
        if pixel == 0:
            zero_pixels += 1
        elif pixel == 1:
            one_pixels += 1
        elif pixel == 2:
            two_pixels += 1
    if zero_pixels < min_zeros:
        max_layer = layer
        min_zeros = zero_pixels
        max_one_pixels = one_pixels
        max_two_pixels = two_pixels

print(max_one_pixels * max_two_pixels)

image = decode_image(image, 25, 6) * 255
print(image)

im = Image.fromarray(image.reshape(6, 25).astype(np.uint8))
im.show()