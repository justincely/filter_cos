import glob
import pyfits
import numpy as np

targs = set( [ pyfits.getval(item,'TARGNAME') for item in glob.glob('*corrtag_a.fits') ] )

for targname in targs:
    tot_exptime_before = 0
    tot_exptime_after = 0
    for item in glob.glob('*corrtag_a.fits'):
        if pyfits.getval( item, 'TARGNAME' ) != targname: continue
        if pyfits.getval( item, 'OPT_ELEM' ) != 'G130M': continue        
        tot_exptime_before += pyfits.getval( item, 'EXPTIMEA', ext=1 )
        tot_exptime_after += pyfits.getval( 'out_filtered/' + item, 'EXPTIMEA', ext=1 )

    print targname, tot_exptime_before, tot_exptime_after, 100*(tot_exptime_after)/tot_exptime_before
