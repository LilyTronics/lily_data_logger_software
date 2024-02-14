"""
Test for the image data model.
"""

import glob
import os

import wx.lib.embeddedimage

from src import images
from src.models.image_data import ImageData
from tests.unit_tests.lib.test_suite import TestSuite


class TestImageData(TestSuite):

    def test_image_data(self):
        app = wx.App(redirect=False)
        images_path = os.path.dirname(images.__file__)
        for item in glob.glob(os.path.join(images_path, "*.png")):
            image_name = os.path.splitext(os.path.split(item)[-1])[0]
            self.fail_if(not hasattr(ImageData, image_name),
                         "There is no definition for image: '{}'".format(image_name))
            embedded_image = getattr(ImageData, image_name)
            self.fail_if(not isinstance(embedded_image, wx.lib.embeddedimage.PyEmbeddedImage),
                         "The object for attribute '{}' is not a embedded image object".format(image_name))
            bitmap = embedded_image.Bitmap
            self.fail_if(not isinstance(bitmap, wx.Bitmap),
                         "The bitmap for attribute '{}' is not a wx.Bitmap".format(image_name))
        app.Destroy()


if __name__ == "__main__":

    TestImageData().run(True)
