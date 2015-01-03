#!/usr/bin/env python
""" 
Script to make CMD, LF, or Hess diagram from a binary fits table
Written by: Phil Rosenfield
"""
import argparse
from astropy.io import fits
import matplotlib.pylab as plt
import numpy as np
import sys

def plot_cmd(color, mag, color_err=None, mag_err=None, ax=None):
    '''
    Plot a Color Magnitude diagram with uncertainties
    
    Parameters
    ----------
    color, mag : color and magnitude arrays
    color_err, mag_err: uncertainties in color and mag
    
    ax : axes instance
    
    Returns
    -------
    ax : axes instance
    '''

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))

    ax.plot(color, mag, '.', ms=3)

    if color_err is not None and mag_err is not None:
        ax.errorbar(color, mag, fmt='none', lw=1, xerr=color_err,
                    yerr=mag_err, capsize=0, ecolor='gray')

    # reverse yaxis
    ax.set_ylim(ax.get_ylim()[::-1])
    return ax


def plot_lf(mag, binsize, mbin=None, yscale='log'):
    """
    Make a Luminosty function (binned magnitude) plot
    
    Parameters
    ----------
    mag : array
        magnitude array to be binned
    binsize : float
        width of magnitude bins
    mbin : array
        right edges of magnitude bins
    yscale : str
        plt.set_yscale option

    Returns
    -------
    ax : axes instance
    """
    if mbin is None:
        mbin = np.arange(mag.min(), mag.max(), binsize)
    
    lf, bins = np.histogram(mag, bins=mbin)
    fig, ax = plt.subplots()
    
    ax.plot(bins[1:], lf, linestyle='steps-pre')
    ax.set_yscale(yscale)
    return ax
    
def make_hess(color, mag, binsize, cbinsize=None, mbin=None, cbin=None):
    """
    Compute a hess diagram (surface-density CMD) on photometry data.

    Parameters
    ---------
    color : array
        color values

    mag : array
        magnitude values

    binsize, cbinsize: float, float
        width of mag, color bins in magnitudes

    cbin : array
        the right edges of the color bins

    mbin : array
        the right edges of the magnitude bins

    Returns
    -------
    cbin : array
        the centers of the color bins

    mbin : array
        the centers of the magnitude bins

    hess : 2d array
        The Hess diagram values
    """

    if mbin is None:
        mbin = np.arange(mag.min(), mag.max(), binsize)

    if cbin is None:
        if cbinsize is None:
            cbinsize = binsize
        cbin = np.arange(color.min(), color.max(), cbinsize)

    hess, cbin, mbin = np.histogram2d(color, mag, bins=[cbin, mbin])
    return hess, cbin, mbin


def plot_hess(color, mag, binsize, ax=None, colorbar=False,
              vmin=None, vmax=None, cbinsize=None, im_kwargs={}):
    """
    Plot a hess diagram with imshow.
    
    Parameters
    ----------
    color : array
        color array to be binned
    mag : array
        magnitude array to be binned

    binsize, cbinsize : float, float
        width of magnitude, color bins
    
    colorbar : bool
        option to also plot the colorbar
    
    vmin, vmax : float, float or None, None
        lower and upper limits sent to matplotlib.colors.LogNorm
    
    im_kwargs : dict
        dictionary passed to imshow by default:
        defaults = {'norm': LogNorm(vmin=vmin, vmax=vmax),
                    'cmap': plt.cm.gray,
                    'interpolation': 'nearest',
                    'extent' [limits of mag and color]
                    'aspect': 'auto'}
    Returns
    -------
    ax : axes instance
    """
    from matplotlib.colors import LogNorm
    if ax is None:
        fig, ax = plt.subplots()

    hess, cbin, mbin = make_hess(color, mag, binsize, cbinsize=cbinsize)
    extent = [np.min(cbin), np.max(cbin), np.max(mbin), np.min(mbin)]
    vmax = vmax or hess.max()

    defaults = {'norm': LogNorm(vmin=vmin, vmax=vmax),
                'cmap': plt.cm.gray,
                'interpolation': 'nearest',
                'extent': extent,
                'aspect': 'auto'}

    kwargs = dict(defaults.items() + im_kwargs.items())

    im = ax.imshow(hess.T, **kwargs)

    if colorbar is True:
        plt.colorbar(im)

    return ax


def load_data(fitsfile, yfilt='I'):
    """
    Load color, magnitude and uncertainties from binary fits table
    
    Parameters
    ----------
    fitsfile : string or file object
        path to binary fits table or object to be read by astropy.io.fits
    
    yfilt : string
        filter to use as mag (V or I)

    Returns
    -------
    color, mag : arrays of color and magnitude
    color_error, mag_err : arrays of summed quadriture uncertainies and magnitude uncertainties
    """

    hdu = fits.open(fitsfile)
    data = hdu[1].data
    photsys = hdu[0].header['CAMERA']

    # the magnitude fields in the fits file are named MAG{1,2}_[photsys]
    mag1 = data['MAG1_%s' % photsys]
    mag2 = data['MAG2_%s' % photsys]
    color = mag1 - mag2

    color_err = np.sqrt(data['MAG1_ERR'] ** 2 + data['MAG2_ERR'] ** 2)

    # choose what gets the yaxis V or I
    if yfilt.upper() == 'I':
        mag = mag2
        ymag = 'MAG2'
    else:
        mag = mag1
        ymag = 'MAG1'

    # the error fields in the fits file are named [MAG]_ERR
    mag_err = data['%s_ERR' % ymag]

    return color, mag, color_err, mag_err

    
def main(argv):
    parser = argparse.ArgumentParser(description="Generate a plot of a fits file")

    parser.add_argument('-p', '--plottype', type=str, default='cmd',
                        help='which plot to make: CMD, hess, or LF')

    parser.add_argument('-f', '--filters', type=str, default=None,
                        help='comma separated V and I filter names for plot labels')

    parser.add_argument('-y', '--yfilter', type=str, default='I',
                        help='plot V or I for LF or on y axis for cmd, Hess')

    parser.add_argument('-m', '--binsize', type=float, default=0.05,
                        help='hess diagram or LF mag binsize')

    parser.add_argument('-c', '--cbinsize', type=float, default=0.1,
                        help='hess diagram color binsize')

    parser.add_argument('-xlim', '--xlim', type=list, default=None,
                        help='comma separated x axis min, max')

    parser.add_argument('-ylim', '--ylim', type=list, default=None,
                        help='comma separated y axis min, max')

    parser.add_argument('-yscale', '--yscale', type=str, default='log',
                        help='y axis scale for LF')

    parser.add_argument('-x', '--colorbar', action='store_true',
                        help='add the hess diagram colorbar')

    parser.add_argument('-outfile', '--outfile', type=str, default='data_plot.png',
                        help='the name of the output file')

    parser.add_argument('-style', '--style', type=str, default='ggplot',
                        choices=plt.style.available,
                        help='the name of the matplotlib style')

    parser.add_argument('file', type=argparse.FileType('r'),
                        help='the name of the fits file')

    args = parser.parse_args(argv)

    # set the plot style
    plt.style.use(args.style)

    if args.filters is not None:
        filter1, filter2 = args.filters.split(',')
    else:
        print('warning: using V, I as default filter names')
        filter1 = 'V'
        filter2 = 'I'
    
    yfilt = args.yfilter
    
    color, mag, color_err, mag_err = load_data(args.file, yfilt=yfilt)
    # the fits file contains stars that are recovered in only one filter
    # stars not recovered are given values >= 90. No need to plot em.
    good, = np.nonzero((np.abs(color) < 30) & (np.abs(mag) < 30))    
    
    if args.plottype.lower() == 'cmd':    
        ax = plot_cmd(color[good], mag[good], color_err=color_err[good], mag_err=mag_err[good])

    if args.plottype.lower() == 'hess':
        ax = plot_hess(color[good], mag[good], colorbar=args.colorbar,
                       binsize=args.binsize, cbinsize=args.cbinsize)

    if args.plottype.lower() == 'lf':
        ax = plot_lf(mag[good], args.binsize, yscale=args.yscale)

        # make axis labels
        ax.set_xlabel(r'$%s$' % yfilt)
        ax.set_ylabel(r'$\#$')
    else:
        # make axis labels for cmd, hess
        if args.filters is not None:
            if yfilt == 'I':
                yfilt = filter2
            else:
                yfilt = filter1

        ax.set_ylabel(r'$%s$' % yfilt)
        ax.set_xlabel(r'$%s-%s$' % (filter1, filter2))

    if args.ylim is not None:
        ylim = np.array(''.join(args.ylim).split(','), dtype=float)
        ax.set_ylim(ylim)
    
    if args.xlim is not None:
        xlim = np.array(''.join(args.xlim).split(','), dtype=float)
        ax.set_xlim(xlim)

    plt.savefig(args.outfile)
    print('wrote %s' % args.outfile)

if __name__ == "__main__":
    main(sys.argv[1:])