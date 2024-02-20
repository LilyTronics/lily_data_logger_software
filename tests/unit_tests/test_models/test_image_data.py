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
                         f"There is no definition for image: '{image_name}'")
            embedded_image = getattr(ImageData, image_name)
            self.fail_if(not isinstance(embedded_image, wx.lib.embeddedimage.PyEmbeddedImage),
                         f"The object for attribute '{image_name}' is not a embedded image object")
            bitmap = embedded_image.Bitmap
            self.fail_if(not isinstance(bitmap, wx.Bitmap),
                         f"The bitmap for attribute '{image_name}' is not a wx.Bitmap")
        app.Destroy()


if __name__ == "__main__":

    import pylint

    TestImageData().run(True)
    pylint.run_pylint([__file__])
