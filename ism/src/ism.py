
# INSTRUMENT MODULE

from ism.src.initIsm import initIsm
from ism.src.opticalPhase import opticalPhase
from ism.src.detectionPhase import detectionPhase
from ism.src.videoChainPhase import videoChainPhase
from common.io.readCube import readCube
from common.io.writeToa import writeToa

class ism(initIsm):

    def __init__(self, auxdir, indir, outdir):
        super().__init__(auxdir, indir, outdir)

    def processModule(self):

        self.logger.info("Start of the Instrument Module")

        # Read input TOA cube
        # -------------------------------------------------------------------------------
        sgm_toa, sgm_wv = readCube(self.indir, self.globalConfig.scene)

        toa_list_optical = []
        toa_list_isrf = []
        toa_list_final = []
        conv_factor_list = []
        system_MTF_list = []
        fnAlt_list = []
        fnAct_list = []
        conv_i2p_list = []
        conv_p2e_list = []
        conv_e2v_list = []
        conv_v2d_list = []
        perc_sat_list = []

        for band in self.globalConfig.bands:

            self.logger.info("Start of BAND " + band)

            # Optical Phase
            # -------------------------------------------------------------------------------
            myOpt = opticalPhase(self.auxdir, self.indir, self.outdir)
            toa, toa_isrf, conv_factor, Hsys, fnAlt, fnAct = myOpt.compute(sgm_toa, sgm_wv, band)

            toa_list_optical.append(toa)
            toa_list_isrf.append(toa_isrf)
            conv_factor_list.append(conv_factor)
            system_MTF_list.append(Hsys)
            fnAlt_list.append(fnAlt)
            fnAct_list.append(fnAct)

            # Detection Stage
            # -------------------------------------------------------------------------------

            myDet = detectionPhase(self.auxdir, self.indir, self.outdir)
            toa, conv_i2p, conv_p2e = myDet.compute(toa, band)

            conv_i2p_list.append(conv_i2p)
            conv_p2e_list.append(conv_p2e)
            # Video Chain Phase
            # -------------------------------------------------------------------------------
            myVcu = videoChainPhase(self.auxdir, self.indir, self.outdir)
            toa, conv_e2v, conv_v2d, perc_sat = myVcu.compute(toa, band)

            toa_list_final.append(toa)
            conv_e2v_list.append(conv_e2v)
            conv_v2d_list.append(conv_v2d)
            perc_sat_list.append(perc_sat)

            # Write output TOA
            # -------------------------------------------------------------------------------
            writeToa(self.outdir, self.globalConfig.ism_toa + band, toa)
            self.logger.info("End of BAND " + band)

        self.logger.info("End of the Instrument Module!")

        return toa_list_optical, toa_list_isrf, toa_list_final, conv_factor_list, system_MTF_list, \
            fnAlt_list, fnAct_list, conv_i2p_list, conv_p2e_list, conv_e2v_list, conv_v2d_list, perc_sat_list



