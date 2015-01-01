from astropy.io import fits
import matplotlib.pylab as plt
import numpy as np

from matplotlib import rc
rc('text', usetex=True)

def add_data(color, mag, color_err=None, mag_err=None, inds=None, ax=None):
    '''plot a cmd with errors'''
    # a subset of indices to plot
    if inds is None:
        inds = np.arange(len(mag))

    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 12))

    ax.plot(color[inds], mag[inds], '.', color='black', ms=3)

    if color_err is not None and mag_err is not None:
        ax.errorbar(color[inds], mag[inds], fmt='none', xerr=color_err[inds],
                    yerr=mag_err[inds], capsize=0, ecolor='gray')
    return ax


def cmd(fitsfile, filter1, filter2, yfilt='I', xlim=None, ylim=None):
    '''
    plot cmd of data, two insets are hard coded.
    '''
    hdu = fits.open(fitsfile)
    data = hdu[1].data
    photsys = hdu[0].header['CAMERA']

    # the magnitude fields in the fits file are named MAG{1,2}_[photsys]
    mag1 = data['MAG1_%s' % photsys]
    mag2 = data['MAG2_%s' % photsys]
    color = mag1 - mag2

    # choose what gets the yaxis V or I
    if yfilt.upper() == 'I':
        yfilt = filter2
        mag = mag2
        ymag = 'MAG2'
    else:
        yfilt = filter1
        mag = mag1
        ymag = 'MAG1'
    # the error fields in the fits file are named [MAG]_ERR
    mag_err = data['%s_ERR' % ymag]
    color_err = np.sqrt(data['MAG1_ERR'] ** 2 + data['MAG2_ERR'] ** 2)

    # the fits file contains stars that are recovered in only one filter
    # stars not recovered are given values >= 90. No need to plot em.

    good, = np.nonzero((np.abs(color) < 30) & (np.abs(mag) < 30))

    fig, ax = plt.subplots(figsize=(8, 8))

    ax = add_data(color, mag, color_err=color_err, mag_err=mag_err, inds=good,
                  ax=ax)

    plt.tick_params(labelsize=18)

    ax.set_ylabel(r'$%s$' % yfilt, fontsize=24)
    ax.set_xlabel(r'$%s-%s$' % (filter1, filter2), fontsize=24)

    if ylim is None:
        # reverse yaxis
        ylim = ax.get_ylim()[::-1]
    ax.set_ylim(ylim)

    if xlim is not None:
        ax.set_xlim(xlim)

    return fig, ax

# LF

# Hess

# Click on CMD


if __name__ == "__main__":
    # http://archive.stsci.edu/prepds/angst/datalist.html
    # http://archive.stsci.edu/pub/hlsp/angst/acs/hlsp_angst_hst_acs-wfc_10605-ugc-5336_f555w-f814w_v1_gst.fits
    fitsfile = 'hlsp_angst_hst_acs-wfc_10605-ugc-5336_f555w-f814w_v1_gst.fits'
    filter1, filter2 = fitsfile.upper().split('_')[5].split('-')
    cmd(fitsfile, filter1, filter2)
    plt.show()