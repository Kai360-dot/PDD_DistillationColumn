import numpy as np
from scipy.optimize import fsolve
from physical_properties import PhysicalProperties
import nist_data
from component_settings import Components


components = Components(nist_data.components_data, nist_data.Antoine_parameters, nist_data.Heat_vap_parameters)
phys_props = PhysicalProperties(nist_data.Antoine_parameters, nist_data.Heat_vap_parameters)

class FindTemperature:
    """Class to find the temperature in a given section of the column, default pressure 1 bar."""
    def __init__(self, component_aliases, p_tot=1):
        """
        Parameters:
        - component_aliases:  list of components present in the section.
        - p_tot: Total pressure in bar (default is 1 bar).
        """
        self.component_aliases = component_aliases
        self.molarFlows = self.getMolarFlows()
        self.totalMolarFlow = self.getTotalMolarFlow()
        self.p_tot = p_tot

    def getMolarFlows(self):
        """Fetches molar flows for the specified components from component_settings."""
        flows = {}
        for component in self.component_aliases:
            flows[component] = components.get_single_flowrate(component)
        return flows

    def getTotalMolarFlow(self):
        """Calculates the total molar flow in the column section."""
        return components.total_section_flowrate(self.component_aliases)

    def getMolFraction(self, component):
        """Calculates the molar fraction of a given component."""
        return self.molarFlows[component] / self.totalMolarFlow

    def objectiveEquation(self, T):
        """Objective function to be solved for temperature."""
        sum_terms = 0
        for component in self.molarFlows:
            sum_terms += phys_props.get_vapor_pressure(component, T) * self.getMolFraction(component)
        return sum_terms - self.p_tot
    def _checkTemperatureBounds(self, Temperature):
        for component in self.component_aliases:
            T = Temperature
            chemical_name = components.components[component].name
            T_up = nist_data.Antoine_parameters[chemical_name]['T_up']
            T_lo = nist_data.Antoine_parameters[chemical_name]['T_lo']
            if T > T_up or T < T_lo:
                raise ValueError(f"Temperature {T} K is out of range for {component}. Valid range is {T_lo} to {T_up} K.")
    def getTemperature(self):
        """Finds the temperature using a numerical solver."""
        initial_guess = 300.0  # Initial guess for temperature in Kelvin
        solution = fsolve(self.objectiveEquation, initial_guess)
        self._checkTemperatureBounds(solution)
        return solution[0]

