import PIL
import numpy as np
import pytesseract
import re
import matplotlib.pyplot as plt

CP_REGION = np.array([[0.038, 0.347,], [0.118, 0.625]])
HP_REGION = np.array([[0.484, 0.375,], [0.516, 0.6]])
DUST_REGION = np.array([[0.73, 0.52,], [0.77, 0.66]])
NAME_REGION = np.array([[0.4, 0.23,], [0.47, 0.8]])

DEFAULT_THRESHOLD = 220

CP_THRESHOLD = 240      # Text is white. Noise level depends on pokemon type
HP_THRESHOLD = DEFAULT_THRESHOLD
DUST_THRESHOLD = DEFAULT_THRESHOLD
NAME_THRESHOLD = 210    # Hides the "pen" edit symbol


class Visual(object):
    """
    Abstract superclass which defines a drawable array with
    monochromatic and thresholded display options.

    Note that implementing classes must set `self.visible` to
    the drawable array.
    """
    def draw(self, mono=False, threshold=None):
        disp_arr = self.visible

        if mono or threshold is not None:
            plt.gray()
            monochrome = np.array(np.average(disp_arr, axis=2), dtype=np.uint8)

            if threshold is None:
                disp_arr = monochrome
            else:
                disp_arr = np.array(monochrome > threshold, dtype=np.uint8)

        plt.imshow(disp_arr)
        plt.show()


class Region(Visual):
    """
    Represents a region of an image with a method to extract text from it.
    """
    def __init__(self, img_arr, key, rel_borders, pattern, threshold):
        """
        `img_arr`: the image array (assumed to be colour == 3-dimensional)
        `key`: identifying property for the region, e.g. 'Name'
        `rel_borders`: relative borders of the region in `img_arr`,
            on the form [[x1, y1], [x2, y2]].
            NOTE: This is matplotlib (x, y) pairs; (0, 0) is the top-left corner
        `pattern`: regex pattern for text to be extracted
        `threshold`: monochrome cut-off for improved text identification
        """
        self.key = key
        [(x1, y1), (x2, y2)] = img_arr.shape[:2] * rel_borders
        self.visible = img_arr[x1:x2, y1:y2]
        self.pattern = pattern
        self.threshold = threshold

    def get_value(self):
        """Returns text found in the image which satisfies `self.pattern`."""
        monochrome = np.array(np.average(self.visible, axis=2), dtype=np.uint8)
        thresholded = np.array(monochrome > self.threshold, dtype=np.uint8)

        ret = pytesseract.image_to_string(PIL.Image.fromarray(tresholded))

        return ret


class IntegerRegion(Region):
    """A region where the value found should be an integer."""
    def get_value(self):
        value = super(NumberRegion, self).get_value()
        return int(value)


class CPRegion(IntegerRegion):
    """The region describing a pokemon's CP."""
    def __init__(self, img_arr):
        super(CPRegion, self).__init__(img_arr, "CP", CP_REGION,
                                       r"(\d\d+)", CP_THRESHOLD)


class HPRegion(IntegerRegion):
    """The region describing a pokemon's HP."""
    def __init__(self, img_arr):
        super(HPRegion, self).__init__(img_arr, "HP", HP_REGION,
                                       r"/(\d+)", HP_THRESHOLD)


class DustRegion(IntegerRegion):
    """The region describing a pokemon's upgrade cost in dust."""
    def __init__(self, img_arr):
        super(DustRegion, self).__init__(img_arr, "Dust", DUST_REGION,
                                         r"(\d+)", DUST_THRESHOLD)


class NameRegion(Region):
    """The region describing a pokemon's name."""
    def __init__(self, img_arr):
        super(NameRegion, self).__init__(img_arr, "Name", NAME_REGION,
                                         r"(.+)", NAME_THRESHOLD)

    def get_value(self):
        value = super(NameRegion, self).get_value().rstrip("/")
        return value


class Screenshot(Visual):
    def __init__(self, path, crop=((0,0), (1184, 720)):
        self.visible = np.array(PIL.Image.open(path), dtype=np.uint8)
        if crop:
            (x1, y1), (x2, y2) = crop
            self.visible = self.visible[x1:x2, y1:y2]
        self.name = NameRegion(self.visible)
        self.cp = CPRegion(self.visible)
        self.hp = HPRegion(self.visible)
        self.dust = DustRegion(self.visible)
        self.regions = [self.name, self.cp, self.hp, self.dust]

    def get_stats(self):
        ret = {}
        for region in self.regions:
            ret[region.key] = region.get_value()


def android_crop(img_array, height=96):
    y_shape = img_array.shape[1]
    return img_array[:, :y_shape - height]



if __name__ == "__main__":
    import os
    import random
    base = "/Users/jorgen/pokedex/"
    x = np.random.choice(os.listdir(base))
    x = "Jigglypuff86_1217_174_2500_crop.png"
    x = "iphone5.jpeg"
    pic = Screenshot(base + x, crop=None)
    pic.visible.shape
    pic.draw()
    pic.visible.shape


    p2 = Screenshot(base + x)
    p2.visible.shape

    p3 = Screenshot(base + x, crop=((0, 0), (1184, 720)))
    p3.draw()

    files = os.listdir(base)
    xs = np.array(files)[np.where(["crop" in f for f in files])]
    xs

    pic = Screenshot(base + "iphone5.jpeg")
    for r in pic.regions:
        r.draw()

    for f in xs:
        pic = Screenshot(base + f)
        for r in pic.regions:
            r.draw()
    pic.draw()

    for i in range(140, 241, 10):

        pic.hp.draw(threshold=i)
