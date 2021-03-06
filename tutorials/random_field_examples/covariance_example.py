#!/usr/bin/env python
# Copyright 2018 Virginia Polytechnic Institute and State University.
""" Example of generating covariance matrices. """

# third party imports
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# local imports
import random_field as rf


# inputs - coordinates
nxpoints = 100
nypoints = 100
ncells = nxpoints*nypoints

# inputs - length scales
constant_length_scales = True
length_scales = (2.0, 1.0)

# inputs - plot locations
point_list = [5050, 0, 4999]

# inputs - standard deviation (sigma) field
stddev_field = np.ones(ncells)*1

# inputs - covariance
perform_checks = True
corr_flag = True
verbose = 2

# calculations
# coordinates
xpos, ypos = np.meshgrid(np.arange(nxpoints), np.arange(nypoints))
xpos = np.atleast_2d(xpos.ravel()).T
ypos = np.atleast_2d(ypos.ravel()).T
coords = np.hstack([xpos, ypos])

# square exponential kernel and inputs
kernel_func = rf.covariance.kernel_sqrexp
kernel_args = {'coords': coords, 'length_scales': length_scales,
               'constant_length_scales': constant_length_scales}

# generate covariance
cov = rf.covariance.generate_cov(
    kernel_func, perform_checks=perform_checks, corr_flag=corr_flag,
    stddev=stddev_field, verbose=verbose, **kernel_args)

# plot covariance matrix
cov_plot = rf.covariance.sparse_to_nan(cov)
fig, ax = plt.subplots()
im = ax.matshow(cov_plot)
ax.set_title('Square Exponential Covariance')
ax.xaxis.tick_bottom()
ax.set_xlabel('Cell ID')
ax.set_ylabel('Cell ID')
ax.set_xlim([0, ncells])
ax.set_ylim([0, ncells])
ax.set_aspect('equal')
ax.invert_yaxis()
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)

# plot covariance field for a specific point
for ipoint in point_list:
    cov_plot = cov[ipoint, :].todense().reshape(nypoints, nxpoints)
    cov_plot = rf.covariance.sparse_to_nan(cov_plot)
    fig, ax = plt.subplots()
    im = ax.matshow(cov_plot)
    ax.set_title('Covariance for Point ({:d}, {:d})'.format(
        coords[ipoint, 0], coords[ipoint, 1]))
    ax.set_xlim([-0.5, nxpoints-0.5])
    ax.set_ylim([-0.5, nypoints-0.5])
    # plt.axis('equal')
    ax.set_aspect('equal')
    ax.xaxis.tick_bottom()
    ax.invert_yaxis()
    ax.set_xlabel('x-coordinate')
    ax.set_ylabel('y-coordinate')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax)

plt.show()
