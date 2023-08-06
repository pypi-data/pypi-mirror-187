import unittest

import pobaidu
from pobaidu.api.imageprocess import selfie_anime, colourize


class TestBaidu(unittest.TestCase):
    def test_selfie_anime(self):
        selfie_anime(img_path=r'file/img_cartoon.jpg')

    def test_colourize(self):
        colourize(img_path=r'file/girl.jpg')
