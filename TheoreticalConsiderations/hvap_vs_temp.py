# Does the enthalpy of vaporization always increase with temperature?
import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from physical_properties import PhysicalProperties
from component_settings import Components
from column import Column
import nist_data # This imports the NIST parameters
import numpy as np
import matplotlib.pyplot as plt

components = Components(nist_data.components_data, nist_data.Antoine_parameters, nist_data.Heat_vap_parameters)
phys_props = PhysicalProperties(nist_data.Antoine_parameters, nist_data.Heat_vap_parameters)

Temp = np.linspace(200, 400, 1000) # although not strictly applicable for all components

hvap_octane = phys_props.get_heat_of_vaporization('D', temperature=Temp)
hvap_heptane = phys_props.get_heat_of_vaporization('C', temperature=Temp)
hvap_hexane  = phys_props.get_heat_of_vaporization('B', temperature=Temp)
hvap_pentane = phys_props.get_heat_of_vaporization('A', temperature=Temp)

plt.plot(Temp, hvap_pentane, label='Pentane')
plt.plot(Temp, hvap_hexane, label='Hexane')
plt.plot(Temp, hvap_heptane, label='Heptane')
plt.plot(Temp, hvap_octane, label='Octane')

# Add axis labels and title
plt.xlabel('Temperature / $K$')
plt.ylabel('Enthalpy of Vaporization / $ kJ \,mol^{-1}$)')
plt.title('Enthalpy of Vaporization vs Temperature')
plt.grid(True)

plt.legend()
plt.savefig('/Users/kairuth/Desktop/MasterStudium/PDD/Marked_1/figures/hvap_vs_temp', dpi = 300)
# plt.show()