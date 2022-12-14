#!/usr/bin/env python

"""Exposes functions to create, and interact with, a histogram
computed from the values of feasible paths generated by GameTime.
"""

"""See the LICENSE file, located in the root directory of
the source distribution and
at http://verifun.eecs.berkeley.edu/gametime/about/LICENSE,
for details on the GameTime license and authors.
"""


import numpy as np

from defaults import logger
from gametimeError import GameTimeError


def computeHistogram(paths, bins=10, range=None, measured=False):
    """Computes a histogram from the values of a list of
    feasible paths generated by GameTime. This function is
    a wrapper around the function :func:`~numpy.histogram` from
    the module :mod:`numpy`. Refer to the documentation of this
    function for more information about the computed histogram.

    Arguments:
        paths:
            List of feasible paths generated by GameTime, each
            represented by a :class:`~gametime.path.Path` object.
        bins:
            Same purpose as the same-named argument of the function
            :func:`numpy.histogram`.
        range:
            Same purpose as the same-named argument of the function
            :func:`numpy.histogram`.
        measured:
            `True` if, and only if, the values that will be used for
            the histogram are the measured values of the feasible paths.

    Returns:
        Tuple, whose first element is an array of the values of
        the histogram, and whose second element is an array of
        the left edges of the bins.
    """
    pathValues = [path.measuredValue if measured else path.predictedValue
                  for path in paths]
    return np.histogram(pathValues, bins=bins, range=range)

def writeHistogramToFile(location, paths, bins=10, range=None, measured=False):
    """Computes a histogram from the values of a list of
    feasible paths generated by GameTime, and writes the histogram
    to a file. Each line of the file has the left edge of each bin
    and the number of samples in each bin, with both of the values
    separated by whitespace.

    Arguments:
        location:
            Location of the file.
        paths:
            List of feasible paths generated by GameTime, each
            represented by a :class:`~gametime.path.Path` object.
        bins:
            Same purpose as the same-named argument of the function
            :func:`numpy.histogram`.
        range:
            Same purpose as the same-named argument of the function
            :func:`numpy.histogram`.
        measured:
            `True` if, and only if, the values that will be used for
            the histogram are the measured values of the feasible paths.
    """
    logger.info("Creating histogram...")

    hist, binEdges = computeHistogram(paths, bins, range, measured)
    try:
        histogramFileHandler = open(location, "w")
    except EnvironmentError as e:
        errMsg = ("Error writing the histogram to the file located "
                  "at %s: %s" % (location, e))
        raise GameTimeError(errMsg)
    else:
        with histogramFileHandler:
            for binEdge, sample in zip(binEdges, hist):
                histogramFileHandler.write("%s\t%s\n" % (binEdge, sample))

    logger.info("Histogram created.")
