# TODO:
# specific_heat(T)

import numpy as np


'''FLOW CONDITIONs'''


#######################
##### Bernulii eq #####
#######################

# p + rho*g*h + rho*u/2 = constant

def free_air_flow(q_N, 
                  T_FAD=293.15, T_N=273.15, 
                  p_N=1.013*10**5, p_FAD=1*10**5):
# input
# qN = Normal volume rate of fow (Nl/s)
# TFAD = standard inlet temperature (20°C)
# TN = Normal reference temperature (0°C)
# pFAD = standard inlet pressure (1.00 bar(a))
# pN = Normal reference pressure
#  (1.013 bar(a))
    
# output
# qFAD = Free Air Delivery (l/s)
    return q_N * (T_FAD / T_N) * (p_N / p_FAD)


def nozzle_massFlow(alfa, flow_coef, p_before_nozzle, area, R, T):
# input:
# α = nozzle coeffcient
# ψ = fow coeffcient
# area = minimum area (m²)
# R = individual gas constant (J/kg x K)
# T1 = absolute temperature before nozzle (K)
# p1 = absolute pressure before nozzle (Pa)

# ouput
# Q = mass fow (kg/s)

    return alfa * flow_coef * p_before_nozzle * area * (2/(R * T))**0.5

def reynoldsNumber(D, u, density, viscosity):
# D = characteristic dimension
#  (e.g. the pipe diameter) (m)
# u = mean fow velocity (m/s)
# ρ = density of the fowing medium (kg/m³)
# η = medium dynamic viscosity (Pa . s)
    
    return (D * u * density) / viscosity

def log_mean_temperature_difference(T1, T2):
# logarithmic mean temperature difference (K)

    return (T1 - T2)/np.log(T1/T2)

#######################
###### Moist Air ######
#######################

# (p-rel_vapor_pressure*ps)*V = Ra * ma * T
# rel_vapor_pressure*ps*V = Rv * mv * T

# p = total absolute pressure (Pa)
# ps = saturation pressure at actual temp. (Pa)
# φ = relative vapor pressure (p/ps)
# V = total volume of the moist air (m3
# )
# Ra = gas constant for dry air = 287 J/kg x K
# Rv = gas constant for water vapor = 462 J/kg x K
# ma = mass of the dry air (kg)
# mv= mass of the water vapor (kg)
# T = absolute temperature of the moist air (K)

'''THERMODYNAMICS'''

# p1 V1 = p2 V2
# V1/T1 = V2/T2
# (p V)/T = R (= individual gas constant J/ (kg x K))
# pV = n R_univ T

# p = absolute pressure (Pa)
# V = volume (m³)
# n = number of moles
# R_univ = universal gas constant
# = 8.314 (J/mol x K)
# T = absolute temperature (K)

## isentropic process 
# k = cp/cv
# p2/p1  =  (V2/V1)**k or 
# p2/p1  =  (T2/T1)**(k/(k-1))

## Polytropic process
# p V**n
# n = 0 for isobaric process
# n = 1 for isothermal process
# n = κ for isentropic process
# n = ∞ for isochoric process

#######################
#### Heat transfer ####
#######################

class HeatTransfer():
      
    def __init__(self):
        pass

    def heat_transfer_conduction(self, k, A, dT, dx):
    # inputs
    # k material's conductivity, W/(m·K)
    # A area m2
    # dT temperature difference (K)
    # dx distance (m)

    # outputs:
    # heat transfer [W]
        
        return k * A * (dT/dx)

    def heat_transfer_convection(self, h, A, dT):
    # h = heat transfer coeffcient (W/m² x K)
    # A = contact area (m²)
    # dT = temperature difference (cold - hot) (K)
        
    # outputs:
    # heat transfer [W]

        return h * A * dT


    ## for isobaric (cp) and isochoric (cv) processes
    def therm_power(self, mass_flow, specific_heat, T1, T2):
    # #input
    # mass_flow= mass fow (kg/s)
    # c = specifc heat (J/kg x K)
    # T = temperature (K)

    # # output
    # P = heat power (W)

        return mass_flow * specific_heat * (T1 - T2)


    ## isothermal process (time ==> OO)
    def isoTherm_tempPressure(self, mass, R, T, p2, p1):
    # inputs
    # m = mass (kg)
    # R = individual gas constant (J/kg x K)
    # T = absolute temperature (K)
    # p = absolute pressure (Pa)

    # ouput
    # quantity of heat (J)

        return mass * R * T *np.log(p2/p1)
    
    ## isothermal process (time ==> OO)
    def isoTherm_volPressure(self, mass, V2, V1):
    # inputs
    # m = mass (kg)
    # V = volume (m³)

    # ouput
    # quantity of heat (J)
        
        return mass * V1 *np.log(V2/V1)


def compressor_work(p1, p2, V1, V2=None, k=None):
# input
# p1 = initial pressure (Pa)
# V1 = initial volume (m3)
# p2 = fnal pressure (Pa)
# К = isentropic exponent: К => 1,3 – 1,4

# output
# W = compression work (J)

    if k==None: # isothermal
        return p1 * V1 * np.log(p2/p1)
    else: # isentropic
        return (k / (k - 1)) * (p2 * V2 - p1 * V1)
    
