

from __future__ import division

import pydensecrf.densecrf as dcrf
from pydensecrf.utils import unary_from_labels, create_pairwise_bilateral, create_pairwise_gaussian, unary_from_softmax

import numpy as np
import matplotlib.pyplot as plt
import sys
import scipy.io as sio
from skimage import color
from skimage.io import imread, imsave

from os import listdir, makedirs
from os.path import isfile, join, isdir
import argparse

import sys
import os
import subprocess
import shutil

from apply_crf import *

IMAGE_DATA = '/data/arunirc/Research/dense-crf-data/training_subset/'
SEG_DATA = '/data2/arunirc/Research/dense-crf/data/our/FBMS/Trainingset/'
OUT_DIR = '/data/arunirc/Research/dense-crf-data/cross-val-crf/'


# range_W=[5]
# range_XY_STD=[40]
# range_RGB_STD=[3]

# gaussian (positional)
POS_W = 3
POS_X_STD = 3

MAX_ITER=5


# bilateral (colorspace)
range_W=[3, 5, 10]
range_XY_STD=[40, 50, 60, 70, 80, 90, 100]
range_RGB_STD=[3, 5, 7, 9, 10]


def grid_runner():

    if not os.path.isdir(OUT_DIR):
            os.makedirs(OUT_DIR)

    for w in range_W:
        Bi_W=w
        for x in range_XY_STD:
            Bi_XY_STD=x
            for r in range_RGB_STD:
                Bi_R_STD = r

                out_dir_name = join( OUT_DIR, 'w-'+str(w) + '_x-'+str(x) + '_r-'+str(r) )

                cmd = 'python  apply_crf.py ' \
                        + '-i ' + IMAGE_DATA + ' ' \
                        + '-s ' + SEG_DATA + ' ' \
                        + '-o ' + out_dir_name + ' ' \
                        + '-d ' + 'fbms ' \
                        + '-cgw ' + str(POS_W) + ' ' \
                        + '-cgx ' + str(POS_X_STD) + ' ' \
                        + '-cbw ' + str(w) + ' ' \
                        + '-cbx ' + str(x) + ' ' \
                        + '-cbc ' + str(r) + ' ' \
                        + '-mi ' + str(MAX_ITER) + ' &'
                print cmd
                subprocess.call(cmd, shell=True)



def grid_evaluater():

    GT_DATA = IMAGE_DATA
    RAW_SEG_DATA = SEG_DATA

    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)

    for w in range_W:
        Bi_W=w
        for x in range_XY_STD:
            Bi_XY_STD=x
            for r in range_RGB_STD:
                Bi_R_STD = r

                out_dir_name = join( OUT_DIR, 'w-'+str(w) + '_x-'+str(x) + '_r-'+str(r) )
                CRF_SEG_DATA = out_dir_name

                cmd = 'python  -m pdb eval_segmentation.py ' \
                        + '-g ' + GT_DATA + ' ' \
                        + '-c ' + CRF_SEG_DATA + ' ' \
                        + '-r ' + RAW_SEG_DATA + ' ' \
                        + '-o ' + out_dir_name
                print cmd
                subprocess.call(cmd, shell=True)



if __name__ == '__main__':
    grid_runner()
    # grid_evaluater()

                


