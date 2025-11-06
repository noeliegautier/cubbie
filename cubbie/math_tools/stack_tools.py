"""
Tools to work with large stacks of coregistered data.
Stacks will be using a certain data format.
X, Y, (image, image, image....) large tuple of images
Some metadata also?
"""

import numpy as np
import os
from cubbie.read_write_insar_utilities import view_raster_utils


def check_dimensions(stack):
    """
    Check the dimensionality of a bunch of interferograms.

    :param stack: a data structure consisting of [X, Y, [intf, intf, intf, intf....]]
    :returns: 1 if the stack has exactly matching dimensions, 0 otherwise
    """
    retval = 1
    numcols, numrows = len(stack[1]), len(stack[0])
    for item in stack[2]:
        yi, xi = np.shape(item)
        if yi != numcols:
            retval = 0
        if xi != numcols:
            retval = 0
    return retval


def convert_nans_to_value(stack, value=-9999):
    """ Convert nans into a particular value, equivalent to applying a mask. """
    stack[2][np.isnan(stack[2])] = value
    return stack


def convert_value_to_nans(stack, value=-9999):
    """ Convert a certain value into nan, equivalent to applying a mask. """
    stack[2][np.where(stack[2]==value)] = np.nan
    return stack


def apply_reference_pixel(stack, reflon, reflat):
    referenced_stack = []
    idx_x = np.abs(stack[0]-reflon).argmin()  # find nearest xval and yval in arrays
    idx_y = np.abs(stack[1]-reflat).argmin()
    for item in stack[2]:
        referenced = item - item[idx_y][idx_x]
        referenced_stack.append(referenced)
    return stack[0], stack[1], np.array(referenced_stack)


def average_stack(stack):
    """
    Perform the element-wise averaging of a stack of interferograms that have been referenced to the same pixel.

    :param stack: a data structure consisting of [X, Y, [intf, intf, intf, intf....]]
    :returns: 1d array for X, 1d array for Y, and 2d array for the average of all the intfs.
    """
    zmean = np.nanmean(stack[2], axis=0)
    return stack[0], stack[1], zmean


def visualize_stack_data(stack, annotation_strs, outdir='images'):
    """ Create a series of images that show the individual interferograms within a stack."""
    os.makedirs(outdir, exist_ok=True)
    for i in range(len(stack[2])):
        view_raster_utils.plot_raster_simple(stack[0], stack[1], stack[2][i],
                                             os.path.join(outdir, 'img_'+str(i)+'.png'),
                                             vmin=-7, vmax=7, title=annotation_strs[i])
    return
