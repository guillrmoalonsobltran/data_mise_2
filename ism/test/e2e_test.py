from ism.src.ism import ism
from l1b.src.l1b import l1b, readToa
import numpy as np
import matplotlib.pyplot as plt

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = r'C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP\\auxiliary'

# Run ISM:

indir = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-E2E\\sgm_out"
outdir = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-E2E\\output_e2e_ism"

myIsm = ism(auxdir, indir, outdir)

# Overwrite configuration values without affecting the config file.
myIsm.ismConfig.pix_size = 42e-6
myIsm.ismConfig.t_int = 0.0428
myIsm.ismConfig.D = 0.07565
myIsm.ismConfig.f = 0.2345
myIsm.ismConfig.apply_prnu = False
myIsm.ismConfig.apply_dark_signal = False
myIsm.ismConfig.apply_bad_dead = False

toa_list_optical, toa_list_isrf, toa_list_final, conv_factor_list, \
    system_MTF_list, fnAlt_list, fnAct_list, conv_i2p_list, conv_p2e_list, \
    conv_e2v_list, conv_v2d_list, perc_sat_list = myIsm.processModule()

# Run L1B:

indir = outdir
outdir = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-E2E\\output_e2e_l1b"

myL1b = l1b(auxdir, indir, outdir)
myL1b.l1bConfig.do_equalization = False
myL1b.l1bConfig.gain = np.array([0.005764054, 0.0042465106, 0.0032643573, 0.002987937]) # [mW/m2/sr/DN]

toa_l1b_list = myL1b.processModule()
"""
Question 1: 
Check that all the modules run with the expected outputs.
"""

"""
Question 2:
Plot the GM latitudes (in Panoply, georeferenced plot). Notice how it is over Toulouse.
"""

"""
Question 3:
Plot altitudes of DEM.
"""

"""
Question 4:
Plot for all bands the outputs of the ISM, the TOA radiances after the optical, the detection and the VCU stages.
"""

"""
Question 5: 
Plot for all bands the outputs of the L1B, the TOA radiances. 
For all bands, compare the L1B TOA radiances with the TOAs after the ISRF.
"""
indir = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-E2E\\output_e2e_ism"
# Retrieve the TOA values after the ISRF from the input folder
toa_after_isrf_list = []
for index in range(4):
    toa_after_isrf_list.append(readToa(indir, f'ism_toa_isrf_VNIR-{index}' + '.nc'))

for index, (toa_eq, toa_after_isrf) in enumerate(zip(toa_l1b_list, toa_after_isrf_list)):

    ACT_pixel_number = list(range(525))
    toa_eq_plot = toa_eq[475, :]
    toa_after_isrf_plot = toa_after_isrf[475, :]

    # Create a plot
    fig = plt.figure(index)
    plt.plot(ACT_pixel_number, toa_eq_plot, label='TOA restored signal')
    plt.plot(ACT_pixel_number, toa_after_isrf_plot, label='TOA after the ISRF')
    plt.title(f'Effect of equalization for VNIR-{index}')
    plt.xlabel('ACT pixel number [-]')
    plt.ylabel('TOA [mW/m2/sr]')
    plt.legend()
    plt.show()
