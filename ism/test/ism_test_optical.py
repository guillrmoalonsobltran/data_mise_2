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
Question 1:
Check for all bands that the differences with respect to the output TOA (ism_toa_isrf) are <0.01% for 
at least 3-sigma of the points.
"""
# Retrieve the TOA values from the reference output folder
reference_toa_list = []
for index in range(4):
    reference_toa_list.append(readToa(outdir_reference, f'ism_toa_isrf_VNIR-{index}' + '.nc'))

# Compare them with the TOA values obtained in our code
for index, (toa, reference_toa) in enumerate(zip(toa_list_isrf, reference_toa_list)):
    element_number = list(range(1, toa.size + 1))

    toa_error = []
    for toa_i, reference_toa_i in zip(toa.flatten(), reference_toa.flatten()):
        toa_error.append(abs(toa_i - reference_toa_i)*100/reference_toa_i)

    # Create a plot
    fig = plt.figure(index)
    plt.plot(element_number, toa_error, label="TOA Error")
    plt.axhline(y=0.01, color='red', linestyle='--', label='% Error = 0.01')
    plt.title(f'Error in TOA with respect to the reference output (ism_toa_isrf) for VNIR-{index}')
    plt.xlabel('Element number in TOA matrix')
    plt.ylabel('% Error in TOA wrt reference output')
    plt.legend()
    plt.show()

"""
Question 2:
Check for all bands that the differences with respect to the output TOA (ism_toa_optical) are <0.01% 
for at least 3-sigma of the points.
"""
# Retrieve the TOA values from the reference output folder
reference_toa_list = []
for index in range(4):
    reference_toa_list.append(readToa(outdir_reference, f'ism_toa_optical_VNIR-{index}' + '.nc'))

# Compare them with the TOA values obtained in our code
for index, (toa, reference_toa) in enumerate(zip(toa_list_optical, reference_toa_list)):
    element_number = list(range(1, toa.size + 1))

    toa_error = []
    for toa_i, reference_toa_i in zip(toa.flatten(), reference_toa.flatten()):
        toa_error.append(abs(toa_i - reference_toa_i)*100/reference_toa_i)

    # Create a plot
    fig = plt.figure(index)
    plt.plot(element_number, toa_error, label="TOA Error")
    plt.axhline(y=0.01, color='red', linestyle='--', label='% Error = 0.01')
    plt.title(f'Error in TOA with respect to the reference output (ism_toa_optical) for VNIR-{index}')
    plt.xlabel('Element number in TOA matrix')
    plt.ylabel('% Error in TOA wrt reference output')
    plt.legend()
    plt.show()

"""
Question 3: 
What is the radiance to irradiance conversion factor for each band. What are the units of the TOA at 
this stage.
"""
CF = conv_factor_list
data = [
    [f"{CF[0]:.5f}", f"{CF[1]:.5f}", f"{CF[2]:.5f}", f"{CF[3]:.5f}"]
]
column_labels = ["VNIR-0", "VNIR-1", "VNIR-2", "VNIR-3"]

fig, ax = plt.subplots(figsize=(5, 2))
plt.title("Radiance to irradiance conversion factor for each band", fontsize=16, pad=1)
ax.axis('off')
table = ax.table(cellText=data, colLabels=column_labels, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(16)
plt.show()
"""
Question 4:
Plot for all bands the System MTF across and along track (for the central pixels). Report the MTF at 
the Nyquist frequency. Explain whether this is a decent or mediocre value and why. 
"""
nyquist_MTF = []
for index, (system_MTF, fnAct) in enumerate(zip(system_MTF_list, fnAct_list)):

    rows, columns = system_MTF.shape
    across_track = system_MTF[int(rows/2), :]
    nyquist_MTF.append(across_track[columns - 1])

    # Across track plot
    plt.plot(fnAct[int(columns/2):], across_track[int(columns/2):], label=f"VNIR-{index}")

plt.title(f'System MTF across track (central row)')
plt.axvline(x=0.5, color='red', linestyle='--', linewidth=1, label='f Nyquist')
plt.xlabel('Spatial frequencies f/(1/w)')
plt.ylabel('MTF across track')
plt.legend()
plt.show()

for index, (system_MTF, fnAlt) in enumerate(zip(system_MTF_list, fnAlt_list)):

    rows, columns = system_MTF.shape
    along_track = system_MTF[:, int(columns/2)]
    nyquist_MTF.append(along_track[rows - 1])

    # Along track plot
    plt.plot(fnAlt[int(rows/2):], along_track[int(rows/2):], label=f"VNIR-{index}")

plt.title(f'System MTF along track (central column)')
plt.axvline(x=0.5, color='red', linestyle='--', linewidth=1, label='f Nyquist')
plt.xlabel('Spatial frequencies f/(1/w)')
plt.ylabel('MTF along track')
plt.legend()
plt.show()

NM = nyquist_MTF
data = [
    [f"Across track", f"{NM[0]:.4f}", f"{NM[1]:.4f}", f"{NM[2]:.4f}", f"{NM[3]:.4f}"],
    [f"Along track", f"{NM[4]:.4f}", f"{NM[5]:.4f}", f"{NM[6]:.4f}", f"{NM[7]:.4f}"]
]
column_labels = ["", "VNIR-0", "VNIR-1", "VNIR-2", "VNIR-3"]

fig, ax = plt.subplots(figsize=(5, 2))
plt.title("MTF at the Nyquist frequency", fontsize=16, pad=1)
ax.axis('off')
table = ax.table(cellText=data, colLabels=column_labels, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(16)
plt.show()
"""
Question 5:
Explain the cause of the border effect introduced by the spatial filter (MTF) and what would be an 
appropriate solution (if any). How many pixel lines does it affect (roughly).
"""
for index, toa in enumerate(toa_list_optical):
    rows, columns = toa.shape
    across_track = toa[int(rows / 2), :]
    pixel_number = list(range(1, columns + 1))

    # Across track plot
    plt.plot(pixel_number, across_track, label=f"VNIR-{index}")

plt.title(f'TOA after the optical stage for the central row')
plt.xlabel('Pixel number')
plt.ylabel('TOA signal')
plt.legend()
plt.show()
"""
Question 6:
Plot the TOA for all bands after the optical stage (with Panoply).
"""