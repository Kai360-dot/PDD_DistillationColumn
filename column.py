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
        self.components_feed = list(set(self.components_top + self.components_bottom))

        self.Temperature_top = self._find_temperature(self.components_top)
        self.Temperature_bottom = self._find_temperature(self.components_bottom)
        

        self.split_fraction_top = self._get_split_fraction(self.components_top) # top to feed molar flow
        self.split_fraction_bottom = self._get_split_fraction(self.components_bottom) # bottom to feed molar flow
        
        self.feed_flowrate = components.total_section_flowrate(self.components_feed)
        self.distillate_flowrate = components.total_section_flowrate(self.components_top)
        self.bottoms_flowrate = components.total_section_flowrate(self.components_bottom)

        self.heats_of_vaporization_top = self._calculate_heats_of_vaporization(self.components_top, self.Temperature_top)
        self.heats_of_vaporization_bottom = self._calculate_heats_of_vaporization(self.components_bottom, self.Temperature_bottom)
        self.avg_heat_of_vap_top = self._get_avg_heat_of_vap_top()
        self.avg_heat_of_vap_bottom = self._get_avg_heat_of_vap_bottom()

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
        self.R_act = self.R_min*1.2
       
        self.duty_condenser = self._get_condenser_duty()
        self.duty_reboiler = self._get_reboiler_duty()

        self.relative_duty_condenser = self.duty_condenser / self.feed_flowrate
        self.relative_duty_reboiler = self.duty_reboiler / self.feed_flowrate

    def _find_temperature(self, components_of_section):
        """Finds and returns the temperature in the tops or bottoms"""
        return FindTemperature([component for component in components_of_section]).getTemperature()

    def _calculate_heats_of_vaporization(self, components, temperature):
        return {component: phys_props.get_heat_of_vaporization(component, temperature) for component in components}
    
    def _get_split_fraction(self, components_section):
        """computes the split fraction of components_section / components feed"""
        flow_components_section = components.total_section_flowrate(components_section)
        flow_column_feed = components.total_section_flowrate(self.components_feed)
        split_fraction = flow_components_section / flow_column_feed
        return split_fraction
    
    def _get_reboiler_duty(self):
        RR = self.R_act
        D = self.distillate_flowrate
        H_vap_avg = self.avg_heat_of_vap_bottom
        Q_R = D * (1+ RR)* H_vap_avg
        return Q_R
    
    def _get_condenser_duty(self):
        RR = self.R_act
        D = self.distillate_flowrate
        H_vap_avg = self.avg_heat_of_vap_top
        Q_C = D * (1+ RR)* H_vap_avg
        return Q_C
    
    def _get_avg_heat_of_vap_top(self):
        avg_H_vap = 0
        for component in self.components_top:
            flow_comp = components.get_single_flowrate(component)
            flow_top = self.distillate_flowrate
            component_molfraction = flow_comp / flow_top
            avg_H_vap += component_molfraction * self.heats_of_vaporization_top[component]
        return avg_H_vap

    def _get_avg_heat_of_vap_bottom(self):
        avg_H_vap = 0
        for component in self.components_bottom:
            flow_comp = components.get_single_flowrate(component)
            flow_bottom = self.bottoms_flowrate
            component_molfraction = flow_comp / flow_bottom
            avg_H_vap += component_molfraction * self.heats_of_vaporization_bottom[component]
        return avg_H_vap


    def print_temperature(self):
        print(f'The Temperature of the Distillate (top of the column) is:\n{self.Temperature_top:.3f} K')
        print(f'The Temperature of the Bottoms (bottom of the column) is:\n{self.Temperature_bottom:.3f} K')

    def print_heat_of_vaporization(self):
        print(f'The heats of vaporization [kJ/mol] in the top: {self.heats_of_vaporization_top}')
        print(f'The heats of vaporization [kJ/mol] in the bottom: {self.heats_of_vaporization_bottom}')
        print(f'Average heat of vaporization [kJ/mol] in the top: {self.avg_heat_of_vap_top}')
        print(f'Average heat of vaporization [kJ/mol] in the bottom: {self.avg_heat_of_vap_bottom}')

    def print_average_relative_volatility(self):
        print(f'The average relative volatility w.r.t. Heavy Key: {self.avg_relative_volatility}')

    def print_Rmin(self):
        print(f'R_min = {self.R_min}')

    def print_R_act(self):
        print(f'R_act = {self.R_min*1.2}')

    def print_present_components(self):
        print(f'Components Top / Bottom:{self.components_top} / {self.components_bottom}')

    def print_split_fractions(self):
        print(f'SplitFracTop : {self.split_fraction_top:.3f}\nSplitFracBottom : {self.split_fraction_bottom:.3f}')

    def print_condenser_duty(self):
        print(f'Condenser Duty: Q_C [MJ / hr] = {self.duty_condenser:.3f}')

    def print_reboiler_duty(self):
        print(f'Reboiler Duty: Q_R [MJ / hr] = {self.duty_reboiler:.3f}')
    
    def print_relative_duties(self):
        print(f'The relative duties [MJ / kmol] are:\nCondenser: {self.relative_duty_condenser:.3f}\n'\
              f'Reboiler: {self.relative_duty_reboiler:.3f}')

    def print_column_data(self):
        print('----------------------------------')
        self.print_present_components()
        # self.print_temperature()
        # self.print_heat_of_vaporization()
        # self.print_average_relative_volatility()
        # self.print_R_act()
        self.print_split_fractions()
        # self.print_condenser_duty()
        # self.print_reboiler_duty()
        self.print_relative_duties()
        print('----------------------------------')

    

# Modify example code below to simulate colunm.
# column_A_BCD = Column(['A', 'B'], [ 'C'])
# column_A_BCD.print_column_data()




# # Example usage
# component_names = ['Pentane', 'Hexane', 'Heptane']
# temperature_finder = FindTemperature(component_names)
# temperature_finder.getTemperature()