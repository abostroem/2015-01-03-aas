#!/usr/bin/env python

from astropy.io import fits
import matplotlib.pylab as plt
import numpy as np
import argparse
import sys

plt.style.use('presentation')


def cmd(color, mag, color_err=None, mag_err=None):
    '''Color Magnitude diagram with uncertainties'''

    # the fits file contains stars that are recovered in only one filter
    # stars not recovered are given values >= 90. No need to plot em.
    good, = np.nonzero((np.abs(color) < 30) & (np.abs(mag) < 30))

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))

    ax.plot(color[good], mag[good], '.', color='black', ms=3)

    if color_err is not None and mag_err is not None:
        ax.errorbar(color[good], mag[good], fmt='none', xerr=color_err[good],
                    yerr=mag_err[good], capsize=0, ecolor='gray')

    return ax


def plot_lf(mag, binsize, mbin=None, yscale='log'):
    if mbin is None:
        mbin = np.arange(mag.min(), mag.max(), binsize)
    
    lf, bins = np.histogram(mag, bins=mbin)
    fig, ax = plt.subplots()
    
    ax.plot(bins[1:], lf, linestyle='steps-pre', lw=3, color='k')
    ax.set_yscale(yscale)
    return ax
    
def make_hess(color, mag, binsize, **kw):
    """
    Compute a hess diagram (surface-density CMD) on photometry data.

    Paramters
    ---------
    color: array
        color values

    mag: array
        magnitude values

    binsize, cbinsize: float, float
        width of mag, color bins in magnitudes

    cbin: sequence, optional
        set the centers of the color bins

    mbin: sequence, optional
        set the centers of the magnitude bins

    Returns
    -------
    cbin: sequence
        the centers of the color bins

    mbin: sequence
        the centers of the magnitude bins

    hess:
        The Hess diagram array
    """

    mbin = kw.get('mbin')
    cbin = kw.get('cbin')

    if mbin is None:
        mbin = np.arange(mag.min(), mag.max(), binsize)

    if cbin is None:
        cbinsize = kw.get('cbinsize')
        if cbinsize is None:
            cbinsize = binsize
        cbin = np.arange(color.min(), color.max(), cbinsize)

    hess, cbin, mbin = np.histogram2d(color, mag, bins=[cbin, mbin])
    return hess, cbin, mbin


def plot_hess(color, mag, binsize, ax=None, colorbar=False,
              vmin=None, vmax=None, cbinsize=None, im_kwargs={}):
    '''Plot a hess diagram with imshow.'''
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
                'aspect': 1.}

    kwargs = dict(defaults.items() + im_kwargs.items())

    ax.autoscale(False)
    im = ax.imshow(hess.T, **kwargs)

    if colorbar is True:
        plt.colorbar(im)

    return ax


def load_data(fitsfile, yfilt='I'):
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
                        help='plot V or I on y axis or on LF')

    parser.add_argument('-m', '--binsize', type=float, default=0.05,
                        help='hess diagram or LF mag binsize')

    parser.add_argument('-c', '--cbinsize', type=float, default=0.1,
                        help='hess diagram color binsize')

    parser.add_argument('-xlim', '--xlim', type=str, default=None,
                        help='x axis limit')

    parser.add_argument('-ylim', '--ylim', type=str, default=None,
                        help='y axis limit')

    parser.add_argument('-yscale', '--yscale', type=str, default='log',
                        help='y axis scale for LF')

    parser.add_argument('-x', '--colorbar', type=bool, default=False,
                        help='cmd y axis limit')

    parser.add_argument('file', type=argparse.FileType('r'),
                        help='the name of the fits file')

    parser.add_argument('-outfile', '--outfile', type=str, default=None,
                        help='the name of the output file')

    args = parser.parse_args(argv)
    
    filter1, filter2 = args.filters.split(',')
    
    yfilt = args.yfilter
    
    color, mag, color_err, mag_err = load_data(args.file, yfilt=yfilt)

    if args.plottype.lower() == 'cmd':    
        ax = cmd(color, mag, color_err=color_err, mag_err=mag_err)

    if args.plottype.lower() == 'hess':
        ax = plot_hess(color, mag, colorbar=args.colorbar,
                       binsize=args.binsize, cbinsize=args.cbinsize)

    if args.plottype.lower() == 'lf':
        ax = plot_lf(mag, args.binsize, yscale=args.yscale)
        ax.set_xlabel(r'$%s$' % yfilt)
        ax.set_ylabel(r'$\#$')
    else:
        if filter2 is not None and filter1 is not None:
            if yfilt == 'I':
                yfilt = filter2
            else:
                yfilt = filter1

            ax.set_ylabel(r'$%s$' % yfilt)
            ax.set_xlabel(r'$%s-%s$' % (filter1, filter2))

        if args.ylim is None:
            # reverse yaxis
            args.ylim = ax.get_ylim()[::-1]
        ax.set_ylim(args.ylim)
    
    if args.xlim is not None:
        ax.set_xlim(args.xlim)

    if args.outfile is None:
        args.outfile = 'data_plot.png'

    plt.savefig(args.outfile)
    print('wrote %s' % args.outfile)

# Click on CMD

if __name__ == "__main__":
    main(sys.argv[1:])
    # http://archive.stsci.edu/prepds/angst/datalist.html
    # http://archive.stsci.edu/pub/hlsp/angst/acs/hlsp_angst_hst_acs-wfc_10605-ugc-5336_f555w-f814w_v1_gst.fits
