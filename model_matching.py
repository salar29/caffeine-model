import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize
from model_params import *
from caffeine_model import model, initial_conditions, t

# Desired maximum concentration (mg/L)
C_cmax_desired = 8

# Initial guess for the parameters
initial_guess = [ka, k12, k21, ke, r_cp]  # Default values, overwrite if needed

# Define parameter bounds, adjust as needed
bounds = ((0.10, 1.50),  # ka   (absorption rate)
          (0.10, 5.00),  # k12  (transfer central to peripheral)
          (0.01, 0.50),  # k21  (transfer peripheral to central)
          (0.05, 0.50),  # ke   (elimination rate)
          (0.60, 0.90))  # r_cp (central vs peripheral absorption ratio) 

def objective_function(params):
    ka, k12, k21, ke, r_cp = params

    # Solve the model with the provided parameters
    solution = odeint(model, initial_conditions, t, args=(ka, k12, k21, ke, r_cp))

    # Extract concentration in the central compartment (C_c = Q_c / V_c)
    C_c = solution[:, 1] / V_c

    # Find the maximum concentration in the central compartment
    C_cmax = max(C_c)

    # Minimize the absolute difference between simulated and desired Cmax
    return abs(C_cmax - C_cmax_desired)

# Perform optimization
results = minimize(objective_function, initial_guess, method='Nelder-Mead')
optimized_params = results.x

# Print results
print(f'Optimized parameters: ka = {optimized_params[0]:.2f}, k12 = {optimized_params[1]:.2f}, k21 = {optimized_params[2]:.2f}, ke = {optimized_params[3]:.2f}, r_cp = {optimized_params[4]:.2f}')
print(f'Optimized Cmax: {C_cmax_desired + results.fun:.2f} mg/L')
print(f'At time: {t[np.argmax(odeint(model, initial_conditions, t, args=tuple(optimized_params))[:, 1] / V_c)]:.2f} hours')

# WIP: Develop a more robust optimization strategy