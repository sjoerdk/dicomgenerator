from copy import deepcopy

import matplotlib.pyplot as plt

from dicomgenerator.generators import quick_dataset
from dicomgenerator.pixeldata import Block, add_blocks, draw_noise, add_pixel_data_2d


# A 2D block region, upper left corner pixel location + extent


def write_pixel_dataset():
    ds = quick_dataset(PatientID="TestPatient", Modality="CT")
    pixel_values = draw_noise(201, 301, "uint8")

    ds = add_pixel_data_2d(dataset=ds, pixel_array=pixel_values, dtype="uint8")
    ds2 = deepcopy(ds)
    ds2 = add_blocks(ds2, [Block(10, 10, 50, 200)])

    ds.save_as("/tmp/test.dcm")
    ds2.save_as("/tmp/test2.dcm")
    plt.imshow(ds.pixel_array)
    plt.imshow(ds2.pixel_array)
    plt.show()


write_pixel_dataset()
