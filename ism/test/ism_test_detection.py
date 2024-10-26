from ism.src.ism import ism
from l1b.src.l1b import readToa
import matplotlib.pyplot as plt

auxdir = r'C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP\\auxiliary'
indir = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-ISM\\input\\gradient_alt100_act150"
outdir = r"C:\\Users\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-ISM\\output_2"
outdir_reference = r"C:\\Users\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-ISM\\output"

# Initialise the ISM
myIsm = ism(auxdir, indir, outdir)
toa_list_optical, toa_list_isrf, toa_list_final, conv_factor_list, \
    system_MTF_list, fnAlt_list, fnAct_list, conv_i2p_list, conv_p2e_list, \
    conv_e2v_list, conv_v2d_list, perc_sat_list = myIsm.processModule()

"""
Question 1: DONE
Check for all bands that the differences with respect to the output TOA (ism_toa_) are <0.01% for at 
least 3-sigma of the points.
"""
# Retrieve the TOA values from the reference output folder
reference_toa_list = []
for index in range(4):
    reference_toa_list.append(readToa(outdir_reference, f'ism_toa_VNIR-{index}' + '.nc'))

# Compare them with the TOA values obtained in our code
for index, (toa, reference_toa) in enumerate(zip(toa_list_final, reference_toa_list)):
    element_number = list(range(1, toa.size + 1))

    toa_error = []
    for toa_i, reference_toa_i in zip(toa.flatten(), reference_toa.flatten()):
        toa_error.append(abs(toa_i - reference_toa_i)*100/reference_toa_i)

    # Create a plot
    fig = plt.figure(index)
    plt.plot(element_number, toa_error, label="TOA Error")
    plt.axhline(y=0.01, color='red', linestyle='--', label='% Error = 0.01')
    plt.title(f'Error in TOA with respect to the reference output (ism_toa_) for VNIR-{index}')
    plt.xlabel('Element number in TOA matrix')
    plt.ylabel('% Error in TOA wrt reference output')
    plt.legend()
    plt.show()

"""
Question 2: DONE
What is the irradiance to photons, photons to electrons, electrons to Volts, and volts to Digital 
numbers conversion factor for all bands. What are the units of the TOA at each stage.

1. Irradiance to photons:
Input: TOA in irradiances [mW/m2]
Output: TOA in photons [ph]

2. Photons to electrons:
Input: TOA in photons [ph]
Output: TOA in electrons [e-]

3. Electrons to Volts:
Input: TOA in electrons [e-]
Output: TOA in volts [V]

4. Volts to digital numbers.
Input: TOA in volts [V]
Output: TOA in digital counts
"""
I2P = conv_i2p_list
P2E = conv_p2e_list
E2V = conv_e2v_list
V2D = conv_v2d_list

data = [
    [f"Irr to phot", f"{I2P[0]:.2e}", f"{I2P[1]:.2e}", f"{I2P[2]:.2e}", f"{I2P[3]:.2e}"],
    [f"Phot to elec", f"{P2E[0]:.1f}", f"{P2E[1]:.1f}", f"{P2E[2]:.1f}", f"{P2E[3]:.1f}"],
    [f"Elec to volts", f"{E2V[0]:.2e}", f"{E2V[1]:.2e}", f"{E2V[2]:.2e}", f"{E2V[3]:.2e}"],
    [f"Volts to num", f"{V2D[0]:.2e}", f"{V2D[1]:.2e}", f"{V2D[2]:.2e}", f"{V2D[3]:.2e}"],
]
column_labels = ["", "VNIR-0", "VNIR-1", "VNIR-2", "VNIR-3"]

fig, ax = plt.subplots(figsize=(5, 2))
plt.title("Conversion factor for all bands", fontsize=16, pad=1)
ax.axis('off')
table = ax.table(cellText=data, colLabels=column_labels, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(16)
plt.show()
"""
Question 3:
Explain why there are ‘stripes’ in the image, and why they are in the ALT direction.

PUT WHATEVER PLOT OF THE FOLDER TO ANSWER THIS. OR, BETTER, ANSWER QUESTION 5 BEFORE QUESTION 3.
"""

"""
Question 4:
For all bands, check whether there are any saturated pixels. Quantify the percentage of saturated 
pixels per band.
"""
SP = perc_sat_list
data = [
    [f"{SP[0]:.1f}%", f"{SP[1]:.1f}%", f"{SP[2]:.1f}%", f"{SP[3]:.1f}%"]
]
column_labels = ["VNIR-0", "VNIR-1", "VNIR-2", "VNIR-3"]

fig, ax = plt.subplots(figsize=(5, 2))
plt.title("Percentage of saturated pixels per band", fontsize=16, pad=1)
ax.axis('off')
table = ax.table(cellText=data, colLabels=column_labels, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(16)
plt.show()
"""
Question 5: DONE
Plot the TOA for all bands after the detection and the VCU stages (Panoply).
THE PLOTS ARE ALREADY IN THE FOLDER
"""