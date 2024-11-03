from l1b.src.l1b import l1b, readToa
import matplotlib.pyplot as plt

auxdir = r'C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP\\auxiliary'
indir = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-L1B\\input"
outdir_eq = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-L1B\\output_eq"
outdir_noeq = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-L1B\\output_noeq"
outdir_reference = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-L1B\\output"

# Initialise the ISM
myL1b_eq = l1b(auxdir, indir, outdir_eq)
myL1b_noeq = l1b(auxdir, indir, outdir_noeq)

# Obtain the restored signal (toa) with equalization
myL1b_eq.l1bConfig.do_equalization = True
toa_list_eq = myL1b_eq.processModule()

# Obtain the restored signal (toa) without equalization
myL1b_noeq.l1bConfig.do_equalization = False
toa_list_noeq = myL1b_noeq.processModule()
'''
Question 1:
Check for all bands that the differences with respect to the output TOA (l1b_toa_) are <0.01% for at 
least 3-sigma of the points.
'''
# Retrieve the TOA values from the reference output folder
reference_toa_list = []
for index in range(4):
    reference_toa_list.append(readToa(outdir_reference, f'l1b_toa_VNIR-{index}' + '.nc'))

# Compare them with the TOA values obtained in our code
for index, (toa_eq, reference_toa) in enumerate(zip(toa_list_eq, reference_toa_list)):
    element_number = list(range(1, toa_eq.size + 1))

    toa_error = []
    for toa_eq_i, reference_toa_i in zip(toa_eq.flatten(), reference_toa.flatten()):
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

'''
Question 2:
For the central ALT position, plot the restored signal (l1b_toa), and the TOA after the ISRF 
(ism_toa_isrf). Explain the differences.
'''
# Retrieve the TOA values after the ISRF from the input folder
toa_after_isrf_list = []
for index in range(4):
    toa_after_isrf_list.append(readToa(indir, f'ism_toa_isrf_VNIR-{index}' + '.nc'))

for index, (toa_eq, toa_after_isrf) in enumerate(zip(toa_list_eq, toa_after_isrf_list)):

    ACT_pixel_number = list(range(150))
    toa_eq_plot = toa_eq[49, :]
    toa_after_isrf_plot = toa_after_isrf[49, :]

    # Create a plot
    fig = plt.figure(index)
    plt.plot(ACT_pixel_number, toa_eq_plot, label='TOA restored signal')
    plt.plot(ACT_pixel_number, toa_after_isrf_plot, label='TOA after the ISRF')
    plt.title(f'Effect of equalization for VNIR-{index}')
    plt.xlabel('ACT pixel number [-]')
    plt.ylabel('TOA [mW/m2/sr]')
    plt.legend()
    plt.show()
'''
Question 3:
Do another run of the L1B with the equalization enabled to false. Plot the restored signal for this case 
and for the case with the equalization set to True. Compare.
'''

for index, (toa_eq, toa_no_eq) in enumerate(zip(toa_list_eq, toa_list_noeq)):

    # Obtain the central ALT row
    toa_eq = toa_eq[49, :]
    toa_no_eq = toa_no_eq[49, :]

    # Define the pixel number in the ACT direction
    ACT_pixel_number = list(range(150))

    # Generate the plots
    fig = plt.figure(index)
    plt.plot(ACT_pixel_number, toa_eq, label='TOA with eq')
    plt.plot(ACT_pixel_number, toa_no_eq, label='TOA with no eq')
    plt.title(f'Effect of equalization for VNIR-{index}')
    plt.xlabel('ACT pixel number [-]')
    plt.ylabel('TOA [mW/m2/sr]')
    plt.legend()
    plt.show()

'''
Question 4:
Can you explain why the restoration for VNIR-1 to VNIR-3 is “blocked” for radiances above 
approximately 200 mW/sr/m2?
'''