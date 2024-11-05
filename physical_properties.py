import numpy as np
import nist_data
from component_settings import Components

components = Components(nist_data.components_data, nist_data.Antoine_parameters, nist_data.Heat_vap_parameters)

class PhysicalProperties:
    def __init__(self, antoine_params, heat_vap_params):
        self.antoine_params = antoine_params
        self.heat_vap_params = heat_vap_params

    def get_vapor_pressure(self, chemical, temperature):
        """Calculate vapor pressure using Antoine equation."""
        chemical_name = components.get_chemical_name(chemical)
        params = self.antoine_params[chemical_name]
        A, B, C, D, E, F, G, T_lo, T_up = params.values()
        return np.exp(A + (B / (temperature + C)) + D * temperature + E * np.log(temperature) + F * (temperature ** G))

    def get_heat_of_vaporization(self, chemical, temperature):
        """Calculate heat of vaporization."""
        chemical_name = components.get_chemical_name(chemical)
        params = self.heat_vap_params[chemical_name]
        A, B, C, Tc, T_lo, T_up = params.values()
        return A * (1 - temperature / Tc) ** B * np.exp(-C * temperature / Tc)

    def identify_light_key(self, components, temperature_top):
        """Identify the light key based on vapor pressure at the top temperature."""
        p_sat_arr = [self.get_vapor_pressure(component, temperature_top) for component in components]
        light_key_index = np.argmin(p_sat_arr)
        return components[light_key_index]

    def identify_heavy_key(self, components, temperature_bottom):
        """Identify the heavy key based on vapor pressure at the bottom temperature."""
        p_sat_arr = [self.get_vapor_pressure(component, temperature_bottom) for component in components]
        heavy_key_index = np.argmax(p_sat_arr)
        return components[heavy_key_index]

    def get_LK_HK_avg_relative_volatility_wrt_HK(self, temperature_top, temperature_bottom, components_top, components_bottom):
        """Calculate average relative volatility with respect to the heavy key.
        Average = \sqrt{top, bottom}"""
        light_key = self.identify_light_key(components_top, temperature_top)
        heavy_key = self.identify_heavy_key(components_bottom, temperature_bottom)
        all_components = list(set(components_top + components_bottom))
        alpha_avg = {}
        for component in all_components:
            alpha_top = self.get_vapor_pressure(component, temperature_top) / self.get_vapor_pressure(heavy_key, temperature_top)
            alpha_bottom = self.get_vapor_pressure(component, temperature_bottom) / \
                self.get_vapor_pressure(heavy_key, temperature_bottom)
            alpha_avg[component] = np.sqrt(alpha_top * alpha_bottom)
        return light_key, heavy_key, alpha_avg

    def get_relative_volatility_wrt_HK(self, temperature_top, temperature_bottom, components_top, components_bottom):
        """Calculate relative volatility wrt HK"""
        all_components = list(set(components_top + components_bottom))
        alpha = {}
        heavy_key = self.identify_heavy_key(components_bottom, temperature_bottom)
        for component in all_components:
            alpha[component] = self.get_vapor_pressure(component, temperature_top) / \
                self.get_vapor_pressure(heavy_key, temperature_top)
        return alpha
    
# # Example:
# # Initialize PhysicalProperties with the component data
phys_props = PhysicalProperties(nist_data.Antoine_parameters, nist_data.Heat_vap_parameters)
# # Example usage
print('Vapor pressure',phys_props.get_vapor_pressure('C', 371.1))
# print(phys_props.get_heat_of_vaporization('Heptane', 333))
