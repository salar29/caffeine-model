# Input parameters
D       = 100   # mg, dose of caffeine ingested
T_ing   = 2     # hr, time window for caffeine ingestion (linear)

# Pharmacokinetic parameters
ka      = 1.50  # hr^-1, [0,inf) absorption rate constant
k12     = 1.20  # hr^-1, [0,inf) distribution rate constant from central to peripheral
k21     = 0.20  # hr^-1, [0,inf) distribution rate constant from peripheral to central
ke      = 0.40  # hr^-1, [0,inf) elimination rate constant
r_cp    = 0.60  # dimensionless, [0,1] ratio of stomach-to-central versus stomach-to-periphery transfer rate

# Compartment volumes (in liters)
V_s     = 1     # Volume of stomach (assumed)
V_c     = 5     # Volume of central compartment (e.g., blood)
V_p     = 50    # Volume of peripheral compartment (e.g., tissues)

model_params = {
    'ka'    : ka,
    'k12'   : k12,
    'k21'   : k21,
    'ke'    : ke,
    'r_cp'  : r_cp
}