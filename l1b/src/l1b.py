
# LEVEL-1B MODULE

from l1b.src.initL1b import initL1b
from common.io.writeToa import writeToa, readToa
from common.src.auxFunc import getIndexBand
from common.io.readFactor import readFactor, EQ_MULT, EQ_ADD, NC_EXT
import os

class l1b(initL1b):

    def __init__(self, auxdir, indir, outdir):
        super().__init__(auxdir, indir, outdir)

    def processModule(self):

        self.logger.info("Start of the L1B Processing Module")

        toa_list = []

        for band in self.globalConfig.bands:

            self.logger.info("Start of BAND " + band)

            # Read TOA - output of the ISM in Digital Numbers
            # -------------------------------------------------------------------------------
            toa = readToa(self.indir, self.globalConfig.ism_toa + band + '.nc')

            # Equalization (radiometric correction)
            # -------------------------------------------------------------------------------
            if self.l1bConfig.do_equalization:
                self.logger.info("EODP-ALG-L1B-1010: Radiometric Correction (equalization)")

                # Read the multiplicative and additive factors from auxiliary/equalization/
                eq_mult = readFactor(os.path.join(self.auxdir,self.l1bConfig.eq_mult+band+NC_EXT),EQ_MULT)
                eq_add = readFactor(os.path.join(self.auxdir,self.l1bConfig.eq_add+band+NC_EXT),EQ_ADD)

                # Do the equalization and save to file
                toa = self.equalization(toa, eq_add, eq_mult)
                writeToa(self.outdir, self.globalConfig.l1b_toa_eq + band, toa)

            # Restitution (absolute radiometric gain)
            # -------------------------------------------------------------------------------
            self.logger.info("EODP-ALG-L1B-1020: Absolute radiometric gain application (restoration)")
            toa = self.restoration(toa, self.l1bConfig.gain[getIndexBand(band)])
            toa_list.append(toa)

            # Write output TOA
            # -------------------------------------------------------------------------------
            writeToa(self.outdir, self.globalConfig.l1b_toa + band, toa)
            self.logger.info("End of BAND " + band)


        self.logger.info("End of the L1B Module!")

        return toa_list


    def equalization(self, toa_measured, eq_add, eq_mult):
        """
        Equlization. Apply an offset and a gain.
        :param toa_measured: TOA in DN
        :param eq_add: Offset in DN
        :param eq_mult: Gain factor, adimensional
        :return: TOA in DN, equalized
        """
        toa_real = (toa_measured - eq_add)/eq_mult
        return toa_real

    def restoration(self,toa_real,gain):
        """
        Absolute Radiometric Gain - restore back to radiances
        :param toa_real: TOA in DN
        :param gain: gain in [rad/DN]
        :return: TOA in radiances [mW/sr/m2]
        """
        toa_L1B = toa_real*gain

        self.logger.debug('Sanity check. TOA in radiances after gain application ' + str(toa_L1B[1,-1]) + ' [mW/m2/sr]')

        return toa_L1B





