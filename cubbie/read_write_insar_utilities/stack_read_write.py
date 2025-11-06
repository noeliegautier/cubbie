from . import isce_read_write
import numpy as np


def read_stack_isce(inputfile):
    """
    Read an input file containing list of files.
    Read each indicated interferogram
    Combine them into a dataset known as a "stack", consisting of x coordinates, y-coordinates,
    3d data cube, and a string associated with each image.
    """
    stack_list, file_names = [], []
    with open(inputfile, 'r') as ifile:
        for line in ifile:
            single_file = line.split()[0]
            x, y, z = isce_read_write.read_scalar_data(single_file)
            stack_list.append(z)
            file_names.append(single_file)
    return x, y, np.array(stack_list), file_names
