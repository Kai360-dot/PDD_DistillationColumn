import numpy as np
from find_temperature import FindTemperature
from physical_properties import PhysicalProperties
from underwood import Underwood
from component_settings import Components
import nist_data # This imports the NIST parameters


phys_props = PhysicalProperties(nist_data.Antoine_parameters, nist_data.Heat_vap_parameters)
components = Components(nist_data.components_data, nist_data.Antoine_parameters, nist_data.Heat_vap_parameters)

class Column:
    """Represents a single distillation column."""
    def __init__(self, components_top_aliases, components_bottom_aliases):
        self.components_top = components_top_aliases
        self.components_bottom = components_bottom_aliases

        self.Temperature_top = self._find_temperature(self.components_top)
        self.Temperature_bottom = self._find_temperature(self.components_bottom)
        
        self.heats_of_vaporization_top = self._calculate_heats_of_vaporization(self.components_top, self.Temperature_top)
        self.heats_of_vaporization_bottom = self._calculate_heats_of_vaporization(self.components_bottom, self.Temperature_bottom)
        
        self.light_key, self.heavy_key, self.avg_relative_volatility = phys_props.get_LK_HK_avg_relative_volatility_wrt_HK(
            self.Temperature_top, self.Temperature_bottom,
            [component for component in self.components_top],
            [component for component in self.components_bottom]
        )
        self.relative_volatility_distillate_conditions = phys_props.get_relative_volatility_wrt_HK(self.Temperature_top, 
                                                                                                   self.Temperature_bottom,
                                                                                                   self.components_top, 
                                                                                                   self.components_bottom)
        
        self.avg_relative_volatility_LK = self.avg_relative_volatility[self.light_key]
        self.avg_relative_volatility_HK = self.avg_relative_volatility[self.heavy_key]

        self.R_min = Underwood(
            self.components_top,
            self.components_bottom,
            self.avg_relative_volatility, 
            self.avg_relative_volatility_LK, 
            self.avg_relative_volatility_HK
        ).get_Rmin(self.relative_volatility_distillate_conditions)

    def _find_temperature(self, components_of_section):
        """Finds and returns the temperature in the tops or bottoms"""
        return FindTemperature([component for component in components_of_section]).getTemperature()

    def _calculate_heats_of_vaporization(self, components, temperature):
        return {component: phys_props.get_heat_of_vaporization(component, temperature) for component in components}

    def print_temperature(self):
        print(f'The Temperature of the Distillate (top of the column) is:\n{self.Temperature_top:.3f} K')
        print(f'The Temperature of the Bottoms (bottom of the column) is:\n{self.Temperature_bottom:.3f} K')

    def print_heat_of_vaporization(self):
        print(f'The heats of vaporization [kJ/mol] in the top: {self.heats_of_vaporization_top}')
        print(f'The heats of vaporization [kJ/mol] in the bottom: {self.heats_of_vaporization_bottom}')

    def print_average_relative_volatility(self):
        print(f'The average relative volatility w.r.t. Heavy Key: {self.avg_relative_volatility}')

    def print_Rmin(self):
        print(f'R_min = {self.R_min}')
    def print_R_act(self):
        print(f'R_act = {self.R_min*1.2}')

# Modify example code below to simulate colunm.
column_A_BCD = Column(['A', 'B'], [ 'C'])
column_A_BCD.print_temperature()
column_A_BCD.print_heat_of_vaporization()
column_A_BCD.print_average_relative_volatility()
column_A_BCD.print_Rmin()
column_A_BCD.print_R_act()

# # Example usage
# component_names = ['Pentane', 'Hexane', 'Heptane']
# temperature_finder = FindTemperature(component_names)
# temperature_finder.getTemperature()