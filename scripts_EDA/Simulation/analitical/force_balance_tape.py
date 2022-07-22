
import pandas as pd
import numpy as np

# for the tape force to hold the protector



def retention_force(EU_peel_force):
    protector_volume = ((np.pi*(18.5/2)**2)-(np.pi*(14/2)**2))*126 # [mm3]
    AL_density =  2.7/1000 # [g/mm³]

    protector_mass = 8.6/1000 # [kg]  # protector_volume*AL_density/1000

    acceleration_on_tape = 24*9.8 # [m/s*s]

    hose_diameter = 18/1000 # [mm]
    protector_diameter = 18/1000 # [mm]
    # protector_mass = 20/1000 # [kg]

    ave_diameter = (hose_diameter + protector_diameter)/2

    EU_peel_strength = EU_peel_force/(13/1000) # [N/m]

    EU_tape_assy_force = EU_peel_strength*(ave_diameter*np.pi) # [N]
    protector_force = protector_mass*acceleration_on_tape

    delta_tape_protector = EU_tape_assy_force - protector_force

    print(f'\nEU_tape_assy_force {EU_tape_assy_force:.2f} ' + \
        f'- protector_force {protector_force:.2f} = {delta_tape_protector:.2f}\n' + \
        f'SF = {EU_tape_assy_force/protector_force:.2f}\n')
    print(f'Protector mass={protector_mass} kg\n')

    d = {'col1': [0, 1, 2, 3], 'col2': pd.Series([2, 3], index=[2, 3])}
    pd.DataFrame(data=d, index=[0, 1, 2, 3])

    ['Din [mm]', 'Dout [mm]', 'L [mm]', 'Protector mass [g]']


def main():

    EU_peel_force = 3.53 # [N] for 13 mm
    retention_force(EU_peel_force)

    EU_peel_force = 3.68 # [N] for 13 mm
    retention_force(EU_peel_force)

    EU_peel_force = 4.68 # [N] for 13 mm
    retention_force(EU_peel_force)


if __name__ == "__main__":
    main()
