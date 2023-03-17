import io
from typing import Tuple, Optional

import numpy as np
from PIL import Image


def convert_file_to_pil_image(file: bytes):
    return Image.open(io.BytesIO(file))


def resize_pil_image(pil_image: Image.Image, shape: Tuple[int, int]):
    """Resize image to expected input shape"""
    return pil_image.resize((shape[1], shape[2]))


def convert_pil_image_rgba_to_rgb(pil_image: Image.Image):
    """ Convert from RGBA to RGB *to avoid alpha channels*"""
    if pil_image.mode == 'RGBA':
        pil_image = pil_image.convert('RGB')
    return pil_image


def convert_pil_image_to_grayscale(pil_image: Image.Image):
    """Convert image into grayscale *if expected*"""
    return pil_image.convert('L')


def convert_pil_image_to_numpy_array(pil_image: Image.Image):
    """Convert image into numpy format"""
    return np.array(pil_image)


def convert_image_file_to_numpy_image_array(file: bytes, *, shape: Optional[Tuple[int, int]] = None,
                                            gray: bool = False):
    """Convert file bytes into numpy format"""

    image = convert_file_to_pil_image(file)
    if shape:
        image = resize_pil_image(image, shape)

    image = convert_pil_image_rgba_to_rgb(image)
    if gray:
        image = convert_pil_image_to_grayscale(image)

    return np.array(image)
