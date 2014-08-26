# Perceptual image hash calculation tool based on algorithm descibed in
# Block Mean Value Based Image Perceptual Hashing by Bian Yang, Fan Gu and Xiamu Niu
#
# Copyright 2014 Commons Machinery http://commonsmachinery.se/
# Distributed under an MIT license, please see LICENSE in the top dir.

import unittest
import blockhash
import PIL.Image as Image
import os, glob

datadir = os.path.join(os.path.dirname(__file__), 'data')

class BlockhashTestCase(unittest.TestCase):
    def __init__(self, img_filename=None, hash_filename=None, method=None, bits=None):
        unittest.TestCase.__init__(self)
        self.img_filename = img_filename
        self.hash_filename = hash_filename
        self.method = method
        self.bits = bits

    def runTest(self):
        im = Image.open(self.img_filename)

        # convert indexed/grayscale images to RGB
        if im.mode == '1' or im.mode == 'L' or im.mode == 'P':
            im = im.convert('RGB')
        elif im.mode == 'LA':
            im = im.convert('RGBA')

        hash = open(self.hash_filename).readline().split()[1]

        if self.method == 1:
            method = blockhash.method1
        elif self.method == 2:
            method = blockhash.method2
        elif self.method == 3:
            method = blockhash.method3
        elif self.method == 4:
            method = blockhash.method4

        method(im, self.bits)

def load_tests(loader, tests, pattern):
    test_cases = unittest.TestSuite()
    for img_fn in glob.glob(os.path.join(datadir, '*.jpg')):
        for m in range(4):
            bits = 16
            method = m + 1
            basename, ext = os.path.splitext(img_fn)
            hash_fn = basename + '_{}_{}.txt'.format(bits, method)
            test_cases.addTest(BlockhashTestCase(img_fn, hash_fn, method, bits))
        pass
    return test_cases
