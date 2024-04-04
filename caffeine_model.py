import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from model_params import *

# Boolean flags
plot_concentration = True
distributed_ingestion = True  # True for linear ingestion, False for instantaneous ingestion

# Initial conditions (amount of caffeine, not concentration)
Q_s0 = 0 if distributed_ingestion else D    # Initial amount in stomach
Q_c0 = 0                                    # Initial amount in central compartment
Q_p0 = 0                                    # Initial amount in peripheral compartment
initial_conditions = [Q_s0, Q_c0, Q_p0]

# Time points for simulation (in hours)
t = np.linspace(0, 24, 1000)

# Define the differential equations (amount rate of change)
def model(Q, t, ka, k12, k21, ke, r_cp):
    Q_s, Q_c, Q_p = Q
    
    if distributed_ingestion:
        if t <= T_ing:
            dQ_s_dt = D / T_ing - ka * Q_s / V_s  # Linear increase in stomach during ingestion window
        else:
            dQ_s_dt = -ka * Q_s / V_s  # No further intake after ingestion window
    else:
        dQ_s_dt = -ka * Q_s / V_s  # Instantaneous ingestion
    
    dQ_c_dt = ka * r_cp * Q_s / V_s - (k12 + ke) * Q_c / V_c + k21 * Q_p / V_p  # Consider compartment volumes
    dQ_p_dt = ka * (1 - r_cp) * Q_s / V_s + k12 * Q_c / V_c - k21 * Q_p / V_p  # Consider compartment volumes
    return [dQ_s_dt, dQ_c_dt, dQ_p_dt]

if plot_concentration:
    # Solve the differential equations
    solution = odeint(model, initial_conditions, t, (ka, k12, k21, ke, r_cp))

    # Extract results (C = Q / V)
    C_s = solution[:, 0] / V_s
    C_c = solution[:, 1] / V_c
    C_p = solution[:, 2] / V_p

    C_cmax = max(C_c)
    t_max = t[np.argmax(C_c)]
    C_cend = C_c[-1]
    n_hl = int(np.floor(np.log(C_cmax / C_cend) / np.log(2))) # Number of complete half-lives in simulation

    print(f'Number of half-lives simulated: {n_hl:.2f}')

    t_hl = [t_max] # Store half-lives

    for i in range(n_hl):
        t_hl.append(t[np.where(C_c > C_cmax / 2**(i+1))[0][-1]]) # Find the time when concentration drops to half

    half_life = np.mean(np.diff(t_hl))

    # Print results
    print(f'Maximum concentration in central compartment: {C_cmax:.2f} mg/L')
    print(f'At time: {t_max:.2f} hours')
    print(f'Average half-life: {half_life:.2f} hours')

    # Plot results
    plt.plot(t, C_c, label='Central compartment (blood)')
    plt.plot(t, C_p, label='Peripheral compartment')
    plt.plot(t, C_s, label='Stomach')
    plt.xlabel('Time (hours)')
    plt.ylabel('Caffeine concentration (mg/L)')
    plt.title('Caffeine Concentration vs. Time')
    plt.ylim(0, max(C_c) * 1.1)
    plt.legend()
    plt.grid(True)
    plt.show()

# WIP: Reduce assumptions by adding more compartments and parameters