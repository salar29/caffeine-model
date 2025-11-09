import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from model_params import *
from caffeine_model import model, initial_conditions, t

# Parameter ranges for sensitivity analysis
param_ranges = {
    # 'ka': (0.6, 1.5),  # Absorption rate (explore slower and faster absorption)
    # 'k12': (0.6, 1.5), # Distribution rate from central to peripheral (explore faster distribution)
    # 'k21': (0.1, 0.3), # Distribution rate from peripheral to central (explore slower distribution)
    # 'ke': (0.2, 1.2),  # Elimination rate (explore slower and faster elimination)
    # 'r_cp': (0.5, 0.9) # Ratio of stomach-to-central vs stomach-to-peripheral transfer rate
}

num_points = 9  # Number of points for each parameter

# Get active parameter names and ranges
active_params = [key for key, value in param_ranges.items() if not key.startswith('#')]
active_ranges = [param_ranges[key] for key in active_params]

# Choose a colormap 
cmap = cm._colormaps['cool']

# Generate evenly spaced values for each parameter
param_val_lists = []
for param_range in active_ranges:
    param_vals = np.linspace(param_range[0], param_range[1], num_points)
    param_val_lists.append(param_vals)

# Create diagonal combinations
param_val_lists_rounded = [[round(val, 2) for val in sublist] for sublist in param_val_lists]
param_combos = list(zip(*param_val_lists_rounded))

# Print results (for clarity)
print(f"Active parameters: {active_params}")
print(f"Parameter value lists: {param_val_lists}")
print(f"Parameter combinations (diagonals): {param_combos}")

# Sensitivity analysis Loop
for i, param_combo in enumerate(param_combos):
    # Modify parameters
    params = model_params.copy()
    for param_name, value in zip(param_ranges.keys(), param_combo):
        params[param_name] = value 

    # Solve the model
    solution = odeint(model, initial_conditions, t, tuple(params.values()))
    C_c = solution[:, 1] / V_c

    # Plot on the same figure
    label = f'Set {i+1}: {param_combo}' if len(active_params) > 1 else f'{active_params[0]} = {param_combo[0]}'
    plt.plot(t, C_c, label=label)

# Apply colormap
lines = plt.gca().get_lines()  # Get plotted lines
color_values = np.linspace(0, 1, num_points) 
for line, color_val in zip(lines, color_values):
    line.set_color(cmap(color_val))

# Generate plot
plt.xlabel('Time (hours)')
plt.ylabel('Caffeine concentration (mg/L)')
plt.title(f'Sensitivity Analysis {active_params}') 
plt.legend()
plt.grid(True)
plt.show()

# WIP: Extract quantitative measures of sensitivity