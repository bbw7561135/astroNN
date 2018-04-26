# ---------------------------------------------------------#
#   astroNN.gaia.downloader: download gaia files
# ---------------------------------------------------------#

import os
import urllib.request
from functools import reduce

import numpy as np
from astropy.io import fits

import astroNN
from astroNN.gaia.gaia_shared import gaia_env, gaia_default_dr
from astroNN.shared.downloader_tools import TqdmUpTo, md5_checksum

currentdir = os.getcwd()


def tgas(flag=None):
    """
    Get path to the Gaia TGAS DR1 files, download if files not found

    :return: List of file path
    :rtype: list
    :History: 2017-Oct-13 - Written - Henry Leung (University of Toronto)
    """
    # Check if dr arguement is provided, if none then use default
    fulllist = []

    # Check if directory exists
    folderpath = os.path.join(gaia_env(), 'Gaia/tgas_source/fits/')
    urlbase = 'http://cdn.gea.esac.esa.int/Gaia/gdr1/tgas_source/fits/'

    if not os.path.exists(folderpath):
        os.makedirs(folderpath)

    hash_filename = 'MD5SUM.txt'
    full_hash_filename = os.path.join(folderpath, hash_filename)
    if not os.path.isfile(full_hash_filename):
        urllib.request.urlretrieve(urlbase + hash_filename, full_hash_filename)

    hash_list = np.loadtxt(full_hash_filename, dtype='str').T

    for i in range(0, 16, 1):
        filename = f'TgasSource_000-000-0{i:0{2}d}.fits'
        fullfilename = os.path.join(folderpath, filename)
        urlstr = urlbase + filename
        file_hash = (hash_list[0])[np.argwhere(hash_list[1] == filename)]

        # Check if files exists
        if os.path.isfile(fullfilename) and flag is None:
            checksum = md5_checksum(fullfilename)
            # In some rare case, the hash cant be found, so during checking, check len(file_has)!=0 too
            if checksum != file_hash and len(file_hash) != 0:
                print(checksum)
                print(file_hash)
                print('File corruption detected, astroNN attempting to download again')
                tgas(flag=1)
            else:
                print(fullfilename + ' was found!')

        elif not os.path.isfile(fullfilename) or flag == 1:
            # progress bar
            with TqdmUpTo(unit='B', unit_scale=True, miniters=1, desc=urlstr.split('/')[-1]) as t:
                # Download
                urllib.request.urlretrieve(urlstr, fullfilename, reporthook=t.update_to)
                checksum = md5_checksum(fullfilename)
                if checksum != file_hash and len(file_hash) != 0:
                    print('File corruption detected, astroNN attempting to download again')
                    tgas(flag=1)
            print(f'Downloaded Gaia DR1 TGAS ({i:d} of 15) file catalog successfully to {fullfilename}')
        fulllist.extend([fullfilename])

    return fulllist


def tgas_load(cuts=True):
    """
    To load useful parameters from multiple TGAS DR1 files

    :param cuts: Whether to cut bad data (negative parallax and percentage error more than 20%)
    :type cuts: boolean
    :return: Dictionary of parameters
    :rtype: dict
    :History: 2017-Dec-17 - Written - Henry Leung (University of Toronto)
    """
    tgas_list = tgas()

    ra = np.array([])
    dec = np.array([])
    pmra_gaia = np.array([])
    pmdec_gaia = np.array([])
    parallax_gaia = np.array([])
    parallax_error_gaia = np.array([])
    g_band_gaia = np.array([])

    for i in tgas_list:
        gaia = fits.open(i)
        ra = np.concatenate((ra, gaia[1].data['RA']))
        dec = np.concatenate((dec, gaia[1].data['DEC']))
        pmra_gaia = np.concatenate((pmra_gaia, gaia[1].data['PMRA']))
        pmdec_gaia = np.concatenate((pmdec_gaia, gaia[1].data['PMDEC']))
        parallax_gaia = np.concatenate((parallax_gaia, gaia[1].data['parallax']))
        parallax_error_gaia = np.concatenate((parallax_error_gaia, gaia[1].data['parallax_error']))
        g_band_gaia = np.concatenate((g_band_gaia, gaia[1].data['phot_g_mean_mag']))
        gaia.close()

    if cuts is True:
        filtered_index = [(parallax_error_gaia / parallax_gaia < 0.2) & (parallax_gaia > 0.)]

        ra = ra[filtered_index]
        dec = dec[filtered_index]
        pmra_gaia = pmra_gaia[filtered_index]
        pmdec_gaia = pmdec_gaia[filtered_index]
        parallax_gaia = parallax_gaia[filtered_index]
        parallax_error_gaia = parallax_error_gaia[filtered_index]
        g_band_gaia = g_band_gaia[filtered_index]

    return {'ra': ra, 'dec': dec, 'pmra': pmra_gaia, 'pmdec': pmdec_gaia, 'parallax': parallax_gaia,
            'parallax_err': parallax_error_gaia, 'gmag': g_band_gaia}


def gaia_source(dr=None, flag=None):
    """
    NAME:
        gaia_source
    PURPOSE:
        download the gaia_source files
    INPUT:
        dr (int): Gaia DR, example dr=1
        flag (int): 0: normal, 1: force to re-download
    OUTPUT:
        list of file path
    HISTORY:
        2017-Oct-13 - Written - Henry Leung (University of Toronto)
        2017-Nov-26 - Update - Henry Leung (University of Toronto)
    """
    dr = gaia_default_dr(dr=dr)
    fulllist = []

    if dr == 1:

        # Check if directory exists
        folderpath = os.path.join(gaia_env(), 'Gaia/tgas_source/fits/')
        urlbase = 'http://cdn.gea.esac.esa.int/Gaia/gdr1//gaia_source/fits/'

        if not os.path.exists(folderpath):
            os.makedirs(folderpath)

        hash_filename = 'MD5SUM.txt'
        full_hash_filename = os.path.join(folderpath, hash_filename)
        if not os.path.isfile(full_hash_filename):
            urllib.request.urlretrieve(urlbase + hash_filename, full_hash_filename)

        hash_list = np.loadtxt(full_hash_filename, dtype='str').T

        for j in range(0, 20, 1):
            for i in range(0, 256, 1):
                filename = f'GaiaSource_000-0{j:0{2}d}-{i:0{3}d}.fits'
                urlstr = urlbase + filename

                fullfilename = os.path.join(folderpath, filename)
                file_hash = (hash_list[0])[np.argwhere(hash_list[1] == filename)]

                # Check if files exists
                if os.path.isfile(fullfilename) and flag is None:
                    checksum = md5_checksum(fullfilename)
                    # In some rare case, the hash cant be found, so during checking, check len(file_has)!=0 too
                    if checksum != file_hash and len(file_hash) != 0:
                        print(checksum)
                        print(file_hash)
                        print('File corruption detected, astroNN attempting to download again')
                        gaia_source(dr=dr, flag=1)
                    else:
                        print(fullfilename + ' was found!')
                elif not os.path.isfile(fullfilename) or flag == 1:
                    # progress bar
                    with TqdmUpTo(unit='B', unit_scale=True, miniters=1, desc=urlstr.split('/')[-1]) as t:
                        urllib.request.urlretrieve(urlstr, fullfilename, reporthook=t.update_to)
                        checksum = md5_checksum(fullfilename)
                        if checksum != file_hash and len(file_hash) != 0:
                            print('File corruption detected, astroNN attempting to download again')
                            gaia_source(dr=dr, flag=1)
                    print(f'Downloaded Gaia DR{dr} Gaia Source ({(j * 256 + i):d} of {(256 * 20 + 112):d}) '
                          f'file catalog successfully to {fullfilename}')
                fulllist.extend([fullfilename])

        for i in range(0, 111, 1):
            filename = f'GaiaSource_000-020-{i:0{3}d}.fits'
            urlstr = urlbase + filename

            fullfilename = os.path.join(folderpath, filename)
            file_hash = (hash_list[0])[np.argwhere(hash_list[1] == filename)]
            # Check if files exists
            if os.path.isfile(fullfilename) and flag is None:
                checksum = md5_checksum(fullfilename)
                # In some rare case, the hash cant be found, so during checking, check len(file_has)!=0 too
                if checksum != file_hash and len(file_hash) != 0:
                    print(checksum)
                    print(file_hash)
                    print('File corruption detected, astroNN attempting to download again')
                    gaia_source(dr=dr, flag=1)
                else:
                    print(fullfilename + ' was found!')
            elif not os.path.isfile(fullfilename) or flag == 1:
                # progress bar
                with TqdmUpTo(unit='B', unit_scale=True, miniters=1, desc=urlstr.split('/')[-1]) as t:
                    urllib.request.urlretrieve(urlstr, fullfilename, reporthook=t.update_to)
                    checksum = md5_checksum(fullfilename)
                    if checksum != file_hash and len(file_hash) != 0:
                        print('File corruption detected, astroNN attempting to download again')
                        gaia_source(dr=dr, flag=1)
                    print(f'Downloaded Gaia DR{dr} Gaia Source ({(20 * 256 + i):d} of {(256 * 20 + 112):d}) file '
                          f'catalog successfully to {fullfilename}')
            fulllist.extend([fullfilename])

    else:
        raise ValueError('gaia_source() only supports Gaia DR1 Gaia Source')

    return fulllist


def anderson_2017_parallax(cuts=True):
    """
    NAME:
        anderson_2017_parallax
    PURPOSE:
        load pre-compiled Anderson et al 2017 improved parallax from data-driven stars model
    INPUT:
        cuts (boolean): whether to cut those parallax err larger than 20% or not
    OUTPUT:
        ra (ndarray)
        dec (ndarray)
        parallax (ndarray): parallax in mas
        parallax_err (ndarray): 1-standard derivation parallax error in mas
    HISTORY:
        2017-Dec-22 - Written - Henry Leung (University of Toronto)
    """
    fullfilename = os.path.join(os.path.dirname(astroNN.__path__[0]), 'astroNN', 'data', 'anderson_2017_dr14_parallax.npz')
    print('Original dataset at: http://voms.simonsfoundation.org:50013/8kM7XXPCJleK2M02B9E7YIYmvu5l2rh/ServedFiles/')
    print('Please be advised starting from 26 April 2018, anderson2017 in astroNN was reduced to parallax cross '
          'matched with APOGEE DR14 only')
    print('If you see this message, anderson2017 in this astroNN version is reduced. Moreover, anderson2017 will be '
          'removed in the future')

    hdu = np.load(fullfilename)
    ra = hdu['ra']
    dec = hdu['dec']
    parallax = hdu['parallax']
    parallax_err = hdu['parallax_err']

    if cuts is True:
        good_index = np.where(parallax_err / parallax < 0.2)[0]
        ra = ra[good_index]
        dec = dec[good_index]
        parallax = parallax[good_index]
        parallax_err = parallax_err[good_index]
    return ra, dec, parallax, parallax_err


def gaiadr2_parallax(cuts=True, keepdims=False):
    """
    Load Gaia DR2 - APOGEE DR14 matches, indices corresponds to APOGEE allstar DR14 file

    :param cuts: Whether to cut bad data (negative parallax and percentage error more than 20%)
    :type cuts: boolean
    :param keepdims: Whether to preserve indices the same as APOGEE allstar DR14, no effect when cuts=False, set to -9999 for bad indices when cuts=True keepdims=True
    :type keepdims: boolean
    :return: numpy array of ra, dec, parallax, parallax_error
    :rtype: ndarrays
    :History: 2018-Apr-26 - Written - Henry Leung (University of Toronto)
    """
    fullfilename = os.path.join(os.path.dirname(astroNN.__path__[0]), 'astroNN', 'data', 'gaiadr2_apogeedr14_parallax.npz')
    print('This is Gaia DR2 - APOGEE DR14 matches, indices corresponds to APOGEE allstar DR14 file')

    hdu = np.load(fullfilename)
    ra = np.array(hdu['RA'])
    dec = np.array(hdu['DEC'])
    parallax = np.array(hdu['parallax'])
    parallax_err = np.array(hdu['parallax_error'])

    if cuts is True and keepdims is False:
        good_index = [(parallax_err / parallax < 0.2) & (parallax > 0.)]
        ra = ra[good_index]
        dec = dec[good_index]
        parallax = parallax[good_index]
        parallax_err = parallax_err[good_index]
    elif cuts is True and keepdims is True:
        # Not magic_number because this should be apogee style
        bad_idx = [(parallax_err / parallax > 0.2) & (parallax < 0.)]
        parallax[bad_idx] = -9999.
        parallax_err[bad_idx] = -9999.
    return ra, dec, parallax, parallax_err
