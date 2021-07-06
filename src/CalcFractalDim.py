# !/user/bin/env python
# coding: utf-8
""" 
The following scripts have been modified in this script.
https://gist.github.com/e5eafc276a4e54f516ed5559df4242c0.git
"""

from __future__ import annotations

import sys
import numpy as np
import scipy
import cv2


class fractal_dimension:

    def __init__(self, file_in, file_out):
        # Initialize with out of range value
        self.fractal_dim = -1.0
        self._f_in = file_in
        self.f_out = file_out

    def run(self) -> None:
        self.input()
        self.calc()
        self.fractal_dim = self._calc_slope()

    def get_dim(self) -> float:
        assert self.fractal_dim >= 0, 'Not calculated yet'
        return self.fractal_dim

    # From https://github.com/rougier/numpy-100 (#87)
    def _boxcount(self, Z: 'img array', k: 'box size') -> int:
        S = np.add.reduceat(
            np.add.reduceat(Z, np.arange(0, Z.shape[0], k), axis=0),
            np.arange(0, Z.shape[1], k), axis=1)

        # We count non-empty (0) and non-full boxes (k*k)
        return len(np.where((S > 0) & (S < k * k))[0])

    def calc(self) -> None:
        # Set the threshold
        threshold = np.mean(self._Z)

        # Transform Z into a binary array
        self._Z = (self._Z > threshold)

        # Minimal dimension of image
        p = min(self._Z.shape)

        # Greatest power of 2 less than or equal to p
        n = 2**np.floor(np.log(p) / np.log(2))

        # Extract the exponent
        n = int(np.log(n) / np.log(2))

        # Build successive box sizes (from 2**n down to 2**1)
        self._sizes = 2**np.arange(n, 1, -1)

        # Actual box counting with decreasing size
        self._counts = []
        for size in self._sizes:
            self._counts.append(self._boxcount(self._Z, size))

    def _calc_slope(self) -> float:
        # Fit the successive log(sizes) with log (counts)
        coeffs = np.polyfit(np.log(self._sizes), np.log(self._counts), 1)
        return -coeffs[0]

    def input(self) -> None:
        # read imagefile
        try:
            self._Z = cv2.imread(self._f_in, 0)
        except AttributeError:
            print("")
            # Only for 2d image
            assert(len(self._Z.shape) == 2)

    def output(self) -> None:
        # output filename&fractalDim to .csv
        try:
            # Check calculated whether or not
            self._Z
        except AttributeError:
            print("AttributeError: Imagefile doesn't loaded yet")
            sys.exit(1)
        else:
            assert self.fractal_dim >= 0, 'Not calculated yet'

            im = self._Z.astype(np.int) * 255
            with open(self.f_out, "a") as f:
                print(self._f_in.rsplit("/", 1)[-1].rsplit(".", 1)[0]
                      + "," + str(self.fractal_dim), file=f)
            # output binarrized image
            # imageio.imwrite("./result/f_out.jpg", im)
