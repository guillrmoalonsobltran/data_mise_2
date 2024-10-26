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
Question 2: DONE
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
Question 3: DONE
What is the radiance to irradiance conversion factor for each band. What are the units of the TOA at 
this stage.
Answer to the second question: 
In the function rad2Irrad: Input: TOA image in radiances [mW/sr/m2]. Output: TOA image in irradiances [mW/m2]
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
Question 4: DONE
Plot for all bands the System MTF across and along track (for the central pixels). Report the MTF at 
the Nyquist frequency. Explain whether this is a decent or mediocre value and why. 

Answer: 
The higher the y-axis (the MTF), the better you can see objects with the spatial resolution specified in the x-axis
The bigger the area under the MTF graph, the lower the PSF, the more resolution your instrument has 
(i.e., the better you can see/resolve objects). Lower psf means a narrower graph (como una distribución normal 
estrechada) and higher psf means a wider graph (como una distribución normal pero muy gorda), el eje x de esas 
gráficas es espacio, y el eje y ni idea.
We are not able to resolve objects with a spatial frequency above the Nyquist frequency (i.e., we can´t resolve any 
object with a spatial frequency to the right of the Nyquist frequency. The spatial resolution in the x-axis is 1/size 
of the object. That is why smaller objects are larger x-axis values
The Nyquist frequency is = 1/(2*size of the pixel). So when its normalized by (1/w) =(1/size of the pixel) we get 0.5.
If the MTF value of your instrument at the Nyquist frequency is = 0. You don´t have aliasing. But you have a bad 
response close to the Nyqusit frequency because the MTF is 0 at Nyquist. It's a trade-off. In general we target 
instruments with a response (MTF) of 0.3-0.4 at the Nyquist frequency.
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
Question 5: DONE
Explain the cause of the border effect introduced by the spatial filter (MTF) and what would be an 
appropriate solution (if any). How many pixel lines does it affect (roughly).

Theory: A convolution is a mathematical operation by which you sweep across an image and multiply each zone 
with a kernel (the zone is the number of pixels equivalent to the kernel size). A kernel, also called a filter or mask,
is a typically small matrix by which you multiply each zone of the input image. Conceptually, you add (or subtract), 
the contribution of neighbouring pixels to a given pixel (i,j). Kernels and convolutions are widely used instruments 
in image processing. For the first pixel, the convolution will multiply the kernel with non-existent pixels.
Usually these imaginary pixels are zero-padded.

Answer: We are calculating the response of the pixels using convolution. A process in which the pixel's response is 
affected by the pixels in its surroundings. Therefore, when we apply the kernel in the borders (and specially 
in the corners), we don´t have sufficient information to perform the convolution and the response becomes non-smooth.
There are different strategies to make up the missing information so the pixel response at the edges is smoother.

When we convolute, we asign energy from neighbouring pixels. That's why, if zero-padding is used, at the borders 
the energy goes down because we are performing convolution with zeros. The amount of signal assigned at the border 
pixels is lower, and a contrast is introduced.

ZOOM IN THE PLOTS IN THE REPORT TO SHOW THE BORDER EFFECT. 
For the central row of all bands, the first pixel is very different from the rest. Pixels 2 to 4 show also some 
relevant jumps. And then from pixels 4 to 8 the smoothing out finishes so that from there on we cannot notice it. 
And the same happens to the pixels at the further end.
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
Question 6: DONE in the folder
Plot the TOA for all bands after the optical stage (with Panoply).
"""