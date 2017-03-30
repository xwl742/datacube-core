'''NetCDF storage driver class
'''
from __future__ import absolute_import

from datacube.drivers.driver import Driver

class NetCDFDriver(Driver):
    '''NetCDF storage driver. A placeholder for now.
    '''

    @property
    def name(self):
        return 'NetCDF CF'
