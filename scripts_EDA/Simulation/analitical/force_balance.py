
import pandas as pd
import numpy as np

# for the tape force to hold the protector
def deltaCalc(protector_mass):

    acceleration_on_tape = 24*9.8 # [m/s*s]

    hose_diameter = 8/1000 # [mm]
    protector_diameter = 8/1000 # [mm]
    # protector_mass = 20/1000 # [kg]

    ave_diameter = (hose_diameter + protector_diameter)/2

    EU_peel_force = 3.53 # [N] for 13 mm
    EU_peel_strength = EU_peel_force/(13/1000) # [N/m]

    EU_tape_assy_force = EU_peel_strength*(ave_diameter*np.pi) # [N]
    protector_force = protector_mass*acceleration_on_tape

    delta_tape_protector = EU_tape_assy_force - protector_force

    print(f'\nEU_tape_assy_force {EU_tape_assy_force:.2f} ' + \
        f'- protector_force {protector_force:.2f} = {delta_tape_protector:.2f}\n')

deltaCalc(30/1000)
