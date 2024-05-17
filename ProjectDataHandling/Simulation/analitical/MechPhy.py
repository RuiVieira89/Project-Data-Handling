
import numpy as np


def hose_insertion_force(hose_inner_diameter, hose_thickness, 
                         spigot_outer_diameter, spigot_length, 
                         young_modulus, friction_coef):
    # tested on rubber hoses on plastic spigots
    # friction_coef can be obtained by experiment (fitting)
    # same for material young_modulus

    striking_pressure = young_modulus*hose_thickness*2*(
        spigot_outer_diameter - hose_inner_diameter)/(hose_inner_diameter*spigot_outer_diameter) #MPa
    
    striking_force = striking_pressure*spigot_length*np.pi*spigot_outer_diameter*10**6 # N
    
    pull_out_force = friction_coef*striking_force # N

    return pull_out_force


## helical gears 
def to_radians(angle):
    
    return angle*(np.pi/180)

def to_rad_sec(rpm):

    return (rpm * 2 * np.pi) / 60


def helical_gears(normal_pressure_angle, helix_angle, diameter_in, diameter_out,
                  power, rotation):
    # angles in RAD!!
    # SI units

    torque_in = power/rotation
    tangent_force = torque_in/diameter_in

    radial_force = tangent_force * np.tan(normal_pressure_angle)/np.cos(helix_angle)
    axial_force = tangent_force * np.tan(helix_angle)
    resultant_force = np.sqrt(tangent_force**2 + radial_force**2 + axial_force**2)

    torque_out = tangent_force * diameter_out

    return [resultant_force, torque_in, torque_out]


def stress_shaft(torque, diameter, moment_inertia=None):

    if moment_inertia is None:
        moment_inertia = (np.pi / 32) * diameter**4 # [m**4]

    return (torque * (diameter / 2)) / moment_inertia 


