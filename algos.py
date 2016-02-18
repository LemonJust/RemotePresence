"""
Algorithms for manipulating OpenCV videos for use with the Oculus DK2
"""


import numpy as np
import cv2

def crop(image, _xl, _xr, _yl, _yr):
    """Crop the image based on inputs

    For a color image, `image` is a 3D array, where the third dimenion
    is the RGB color separation. This method ignores the third
    dimensions, thus cropping all three equally.

    Args:
        image (np.array): The image matrix returned as the second
            item of cv2.VideoCapture.read().
        _xl, _xr, _yl, _yr (int): The boundaries to crop `image` to
    """

    width, height = Parameters.width, Parameters.height
    return image[
        _xl:width - _xr,
        _yl:height - _yr
    ]

def create_distortion_matrix(_fx, _cx, _fy, _cy):
    """Construct distortion matrix from arguments"""
    return np.array([
        [_fx, 0, _cx],
        [0, _fy, _cy],
        [0, 0, 1]
    ])

def transform(image, matrix, k1=0.22, k2=0.24):
    """Apply barrel distortion using OpenCV's Undistort operation

    This counteracts the pincushion distortion that the Oculus lens
    applies. The distortion coefficients k1 and k2 are the main
    action here.

    [1]: http://docs.opencv.org/trunk/doc/py_tutorials/py_calib3d/\
             py_calibration/py_calibration.html
    """
    return cv2.undistort(
        image,
        matrix,
        np.array([k1, k2, 0, 0, 0])
    )

def join_images(image_left, image_right):
    """Join two images left-to-right, using Numpy"""
    return np.append(image_left, image_right, axis=1)

def translate(image, x, y):
    """Strict linear translation, using OpenCv's warpAffine

    TODO: Make rows and columns dynamic (OpenCV doesn't seem to  like
    it if you try to change this value during runtime).

    Also see the bottom of this page:
    http://www.3dtv.at/knowhow/EncodingDivx_en.aspx
    """
    columns, rows = Parameters.width, Parameters.height
    return cv2.warpAffine(
        image,
        np.float32([[1, 0, x], [0, 1, y]]),
        (columns, rows)
    )

def print_params():
    """Print out all parameters for reference"""
    strings = []
    for item in [par for par in dir(Parameters) if par.isalnum()]:
        strings.append("{name} = {value}".format(
            name=item,
            value=getattr(Parameters, item),
        ))
    string = ', '.join(strings)
    print(string)

class Parameters():
    """Parameters for the video frame and the like

    Includes width, height, offsets, warp, and window size, as well
    as frames-per-second.

    Also includes a set of key mapping tuples, which are used to
    increment and decrement (the first and second items in the tuple)
    each parameter. This could be possibly more elegant, but it's
    simple and it works ok.
    """

    cropXL = 0
    cropXR = 0
    cropYL = 0
    cropYR = 0
    cxL = 0
    cxR = 0
    cyL = 0
    cyR = 0
    fps = 30
    fxL = 270
    fxR = 270
    fyL = 360
    fyR = 360
    height = 340
    width = 420
    xL = 0
    xR = 0
    yL = 0
    yR = 0
    xo = 0
    xo2 = 0
    yL = 0
    yR = 0
    yo = 0
    yo2 = 0
    '''
    cropXL = 0
    cropXR = 160
    cropYL = 0
    cropYR = 0
    cxL = 330
    cxR = 330
    cyL = 250
    cyR = 250
    fps = 15
    fxL = 270
    fxR = 270
    fyL = 360
    fyR = 360
    height = 480
    width = 720
    xL = 200
    xR = 200
    yL = -200
    yR = -200
    xo = 70
    xo2 = -70
    yL = 0
    yR = 0
    yo = 0
    yo2 = 0
    '''
    key_mappings = dict(
        fxL=('f', 's'),
        fxR=('f', 's'),
        fyL=('e', 'd'),
        fyR=('e', 'd'),
        cxL=('l', 'j'),
        cxR=('l', 'j'),
        cyL=('k', 'i'),
        cyR=('k', 'i'),
        yo2=('o', 'u'),
        xo2=('m', 'n'),
        xo=('.', ','),
        yo=('h', ';'),
        cropXL=('z', 'x'),
        cropYL=('w', 'r'),
        cropXR=('c', 'v'),
        cropYR=('a', 'g'),
    )
