from scipy.optimize import fsolve
import numpy as np
from physical_properties import PhysicalProperties
import nist_data
from component_settings import Components

phys_props = PhysicalProperties(nist_data.Antoine_parameters, nist_data.Heat_vap_parameters)
components = Components(nist_data.components_data, nist_data.Antoine_parameters, nist_data.Heat_vap_parameters)

class Underwood:
    def __init__(self, 
                 ComponentsTop, 
                 ComponentsBottom, 
                 AverageRelativeVolatilities, 
                 AverageRelativeVolatilityLK, 
                 AverageRelativeVolatilityHK) -> None:
        
        """The average rel.vol. are expected as dictionary."""
        self.all_components = list(set(ComponentsTop + ComponentsBottom))
        self.average_relative_volatilities = AverageRelativeVolatilities
        self.z_dict = self._component_to_z_Feed()
        self.components_top = ComponentsTop
        self.average_relative_volatility_LK = AverageRelativeVolatilityLK
        self.average_relative_volatility_HK = AverageRelativeVolatilityHK
        self.phi = self._get_phi(self.average_relative_volatilities, 
                                 self.z_dict, self.average_relative_volatility_HK, 
                                 self.average_relative_volatility_LK)

    def _component_to_z_Feed(self):
        z_dict = {}
        sum_streams_column = components.total_section_flowrate(self.all_components)
        # print('The Sum of streams in this column is: {}'.format(sum_streams_column))
        for component in self.all_components:
            z_dict[component] = components.get_single_flowrate(component) / sum_streams_column
        return z_dict
    def _objective_function(self, phi):
        sum_underwood = 0
        for component in self.all_components:
            alpha_comp = self.average_relative_volatilities[component]
            z_comp = self.z_dict[component]
            # print("z ({}) is {}".format(component, z_comp))
            sum_underwood += alpha_comp*z_comp / (alpha_comp - phi)
        return sum_underwood
    
    def _get_phi(self, AverageRelativeVolatilities, ZDict, lower_bound, upper_bound):
            initial_guess = (lower_bound + upper_bound) / 2
            solution = fsolve(self._objective_function, initial_guess)
            if lower_bound <= solution[0] <= upper_bound:
                # print('Phi is: {}\nBounds: [{}; {}]'.format(solution[0], lower_bound, upper_bound))
                return solution[0]
            else:
                raise ValueError("Solution found by fsolve is outside the bounds")
    def get_Rmin(self, relative_volatility_distillate_conditions):
        sum = 0
        for component in self.all_components:
            alpha = self.average_relative_volatilities[component] #use averaged values
            # print('alpha of {} is {}'.format(component, alpha))
            stream_component = components.get_single_flowrate(component)
            sum_of_distillate_streams = components.total_section_flowrate(self.components_top)
            x = stream_component / sum_of_distillate_streams
            # print('x of {} is {}'.format(component, x))
            if component in self.components_top:
                sum += alpha*x / (alpha - self.phi)
        return sum - 1