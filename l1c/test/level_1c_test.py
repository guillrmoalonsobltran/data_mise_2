from l1c.src.l1c import l1c, readToa
import matplotlib.pyplot as plt
import numpy as np

# Directories
auxdir = r'C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP\\auxiliary'
indir = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-L1C\\input\\gm_alt100_act_150,C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-L1C\\input\\l1b_output"
outdir = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-L1C\\output_2"
outdir_reference = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-L1C\\output"

# Initialise the ISM
myL1c = l1c(auxdir, indir, outdir)
toa_l1c_list = myL1c.processModule()
"""
Question 1:
Check for all bands that the differences with respect to the output TOA are <0.01% for 3-sigma of 
the points.
"""
# Retrieve the TOA values from the reference output folder
reference_toa_list = []
for index in range(4):
    toa = np.sort(readToa(outdir_reference, f'l1c_toa_VNIR-{index}' + '.nc'))
    toa[toa < 0] = 0
    reference_toa_list.append(toa)

# Compare them with the TOA values obtained in our code
for index, (toa_l1c, reference_toa) in enumerate(zip(toa_l1c_list, reference_toa_list)):
    element_number = list(range(1, toa_l1c.size + 1))

    toa_error = []
    for toa_eq_i, reference_toa_i in zip(toa_l1c.flatten(), reference_toa.flatten()):
        toa_error.append(abs(toa_eq_i - reference_toa_i)*100/reference_toa_i)

    # Create a plot
    fig = plt.figure(index)
    plt.plot(element_number, toa_error, label="TOA Error")
    plt.axhline(y=0.01, color='red', linestyle='--', label='% Error = 0.01')
    plt.title(f'Error in TOA with respect to the reference output for VNIR-{index}')
    plt.xlabel('Element number in TOA matrix')
    plt.ylabel('% Error in TOA wrt reference output')
    plt.legend()
    plt.show()
"""
Question 2:
Plot for all bands the L1C grid points and plot the georeferenced TOA (with Panoply). Verify that the 
grid points are equispaced, see Figure 6-3.
"""



