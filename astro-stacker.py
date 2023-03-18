from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from astropy.nddata import Cutout2D
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
import numpy as np

# Load the first FITS image to get the image dimensions and WCS
filename = 'image1.fits'
with fits.open(filename) as hdul:
    data = hdul[0].data
    header = hdul[0].header
    wcs = WCS(header)

# Calculate the median of the data values for each pixel
median_data = np.median([fits.getdata('image{}.fits'.format(i)) for i in range(1, 10001)], axis=0)

# Calculate the standard deviation and mean of the data values for each pixel
mean, median, std = sigma_clipped_stats(median_data, sigma=3.0)

# Create a Cutout2D object centered on the astronomical object
ra = header['CRVAL1']
dec = header['CRVAL2']
coord = SkyCoord(ra, dec, unit='deg')
cutout_size = 100  # The size of the cutout in pixels
cutout = Cutout2D(median_data, coord, cutout_size, wcs=wcs)

# Save the stacked image to a FITS file
header['COMMENT'] = 'Stacked from 10000 images'
header['MEAN'] = (mean, 'Mean of pixel values')
header['MEDIAN'] = (median, 'Median of pixel values')
header['STD'] = (std, 'Standard deviation of pixel values')
header['CUTOUT'] = ('({}, {}) with size {} px'.format(ra, dec, cutout_size),
                    'RA and Dec of the cutout and cutout size in pixels')
hdu = fits.PrimaryHDU(data=cutout.data, header=header)
hdu.writeto('stacked_image.fits', overwrite=True)
