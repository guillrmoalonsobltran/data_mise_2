from l1c.src.l1c import l1c

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = r'C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP\\auxiliary'
indir = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-L1C\\input\\gm_alt100_act_150,C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-L1C\\input\\l1b_output"
outdir = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-L1C\\output_2"


# Initialise the ISM
myL1c = l1c(auxdir, indir, outdir)
myL1c.processModule()

"""
Question 1:
Check for all bands that the differences with respect to the output TOA are <0.01% for 3-sigma of 
the points.
"""

"""
NOTE: The output reference L1C TOA has some points with negative radiances which are the result of an 
extrapolation. If you want, you can set these negative radiances to zero.
NOTE: The ordering of the TOAs is not the same in all executions, therefore, to check this requirement 
you need to sort the TOAs in your results and in the reference data.
"""

"""
Question 2:
Plot for all bands the L1C grid points and plot the georeferenced TOA (with Panoply). Verify that the 
grid points are equispaced, see Figure 6-3.
"""