import argparse
import numpy as np
from pathlib import Path
from PIL import Image
from scipy.ndimage import gaussian_filter
import sys 

from util import load_img, save_img

class XDoG:
    def __init__(self, input, gamma, phi, eps, k, sigma, thresh=False):
        self.input_arr = load_img(input)
        self.set_params(gamma, phi, eps, k, sigma)
        self.thresh = thresh
        self.output_arr = None

    def set_params(self, gamma, phi, eps, k, sigma):
        self.gamma = gamma
        self.phi = phi 
        self.eps = eps 
        self.k = k 
        self.sigma = sigma

    def apply(self):
        g_filtered_1 = gaussian_filter(self.input_arr, self.sigma)
        g_filtered_2 = gaussian_filter(self.input_arr, self.sigma * self.k)

        z = g_filtered_1 - self.gamma * g_filtered_2

        z[z < self.eps] = 1.

        mask = z >= self.eps
        z[mask] =  1. + np.tanh(self.phi * z[mask])

        if self.thresh:
            mean = z.mean()
            z[z < mean] = 0.
            z[z >= mean] = 1.

        self.output_arr = z

    def save(self, out_path):
        save_img(out_path, self.output_arr)

PARAM_DEFAULT = [0.98, 200, -0.1, 1.6, 0.8]

parser = argparse.ArgumentParser(description='Provide input and output image file paths and parameters for the XDoG image filter.')
parser.add_argument('-i', '--input', type=Path)
parser.add_argument('-o', '--output', type=Path)
parser.add_argument('-p', '--params', type=float, nargs=5,
                        default=PARAM_DEFAULT)
parser.add_argument('-t', '--thresh', action='store_true')


parsed = parser.parse_args(sys.argv[1:])

in_path, out_path, params = parsed.input, parsed.output, parsed.params

if in_path is not None:
    if in_path.is_file():
        if out_path is None:
            out_path = in_path.parent / f'{in_path.name}-out.png'

        xdog = XDoG(in_path, *params, thresh=parsed.thresh)
        xdog.apply()
        xdog.save(out_path)
    else:
        print(f'File {in_path} could not be found.')

