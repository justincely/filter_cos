import pyfits
import glob
import pylab

pylab.ioff()

for item in glob.glob('*corrtag_a.fits'):
    print item
    fits = pyfits.open(item)
    if fits[0].header['OPT_ELEM'] != 'G130M': continue
    pylab.figure( figsize=(14,6) )
    pylab.suptitle( item )
    pylab.subplot(1,2,1)
    pylab.title('OI vs time')
    pylab.xlabel('Time (s)')
    pylab.ylabel('Airglow cnts/sc')
    pylab.plot(fits['TIMELINE'].data['TIME'],fits['TIMELINE'].data['OI_1304'])

    pylab.subplot(1,2,2)
    pylab.title('OI vs sun_alt')
    pylab.xlabel('sun_alt')
    pylab.ylabel('Airglow cnts/sc')
    pylab.plot(fits['TIMELINE'].data['SUN_ALT'], fits['TIMELINE'].data['OI_1304'], label='OI_1304')
    #pylab.plot(fits['TIMELINE'].data['SUN_ALT'], fits['TIMELINE'].data['LY_ALPHA'], label='LY_ALHPA')
    #pylab.legend()

    pylab.savefig(item[:-5]+'_airglow.png')
    pylab.close()
