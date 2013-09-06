import pyfits
import glob
import os
import shutil
import calcos
from costools import timefilter

from astroraf.cos.misc import read_asn, remake_asn

os.environ['lref']='/grp/hst/cdbs/lref/'

out_dir='out_filtered/'
asn_list = glob.glob('*asn.fits')

def filter_corrtag(filename,output,timerange=None, waverange=(1301,1307) ):
    import numpy as np
    fits = pyfits.open(filename,mode='update')

    time_index = np.where( (fits['timeline'].data['SUN_ALT'] > 20) )[0]
    all_times = fits['timeline'].data['time'][time_index]
    min_time = all_times.min()
    max_time = all_times.max()

    index_keep = np.where( (fits[1].data['wavelength'] < waverange[0]) & 
                      (fits[1].data['wavelength'] > waverange[1]) & 
                      (fits[1].data['time'] < min_time) &
                      (fits[1].data['time'] > max_time) )[0]
    
    fits['EVENTS'].data = fits['EVENTS'].data[index_keep]
    fits.writeto(output)
    fits.close()


if __name__ == '__main__':
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    for item in asn_list:
        print item
        shutil.copy(item,out_dir)
        members,producuts = read_asn(item)
        for member in members:
            print member
            for segment in ['a','b']:
                file_name=member+'_corrtag_%s.fits'%(segment)
                if os.path.exists(os.path.join(out_dir,file_name) ): continue
                if (segment == 'a') and (pyfits.getval(file_name,'OPT_ELEM',ext=0) == 'G130M'): 
                    timefilter.TimelineFilter(input = file_name, output = os.path.join(out_dir,file_name), 
                                              filter = 'SUN_ALT > 20')
                else: 
                    shutil.copy(file_name,os.path.join(out_dir,file_name))
   


    os.chdir(out_dir)

    if not os.path.exists('out/'):
        os.mkdir('out/')

    for item in glob.glob('*asn.fits'):
        shutil.copy( item, 'out/' )

    cal_list = glob.glob('*corrtag_a*')

    for corrtag in cal_list:
        try:
            calcos.calcos(corrtag, 'out/') 
        except:
            print 'Exception occured'
            pass

    os.chdir( 'out/' )
    for item in glob.glob( '*x1d.fits' ):
        fits = pyfits.open( item )
        for i in range(len( fits[1].data ) ):
            if not fits[1].data[i]['FLUX'].any():
                fits[1].data[i]['DQ_WGT'] = 0
                fits.writeto( item, clobber=True )

    for item in glob.glob( '*asn.fits' ):
        remake_asn( item )
