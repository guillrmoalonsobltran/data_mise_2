
# MAIN FUNCTION TO CALL THE ISM MODULE

from ism.src.ism import ism

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = r'C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP\\auxiliary'
#Lo que estaba antes:
indir = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-ISM\\input\\gradient_alt100_act150"
# Para el test 7:
# indir = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-E2E\\sgm_out"

#Lo que estaba antes:
outdir = r"C:\\Users\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-ISM\\output_2"
# Para el test 7:
# outdir = r"C:\\Users\\guill\\Documents\\Universidad\\Earth Observation Data Processing\\EODP_TER_2021\\EODP-TS-E2E\\output_test7"

# Initialise the ISM
myIsm = ism(auxdir, indir, outdir)
myIsm.processModule()
