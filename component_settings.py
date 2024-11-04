import numpy as np
import nist_data
# Note: Use this snippet to initialize:
# components = Components(nist_data.components_data, nist_data.Antoine_parameters, nist_data.Heat_vap_parameters)

class Component:
    def __init__(self, name, alias, flowrate, antoine_params, heat_vap_params):
        self.name = name
        self.alias = alias
        self.flowrate = flowrate
        self.antoine_params = antoine_params
        self.heat_vap_params = heat_vap_params

class Components:
    def __init__(self, components_data, antoine_params, heat_vap_params):
        """Below creates a dictionary:
        'A' : ClassItem(ComponentClass) with name, alias, flowrate, params."""
        self.components = {
            alias: Component(
                name=data['compound_name'],
                alias=alias,
                flowrate=data['flowrate'],
                antoine_params=antoine_params[data['compound_name']],
                heat_vap_params=heat_vap_params[data['compound_name']]
            )
            for alias, data in components_data.items()
        }
    
    def get_component(self, alias):
        """Retrieve a component by its alias."""
        return self.components.get(alias)
    
    def get_chemical_name(self, alias):
        """Retrieve the chemical name of a single component by its alias.
        Pass a single alias to this method: .get_chemical_name('A')"""
        component = self.get_component(alias)
        if component:
            return component.name
        else:
            raise ValueError(f"Component with alias '{alias}' not found.")

    def get_all_components(self):
        """Return all components."""
        return self.components.values()
    
    def total_section_flowrate(self, components_present):
        """Calculate the total flowrate of all components.
        Pass a list to this method: ['A', 'B']"""
        return sum([self.components[alias].flowrate for alias in components_present])
    
    def get_single_flowrate(self, alias):
        """Retrieve the flowrate of a single component by its alias.
        Pass a single alias to this function: .get_flowrate('A')"""
        component = self.get_component(alias)
        if component:
            return component.flowrate
        else:
            raise ValueError(f"Component with alias '{alias}' not found.")



# # Example usage to obtain partial flowrate:
# components = Components(nist_data.components_data, nist_data.Antoine_parameters, nist_data.Heat_vap_parameters)
# species_present = ['A', 'B', 'C'] # Replace with actual aliases present in your data
# total_flowrate = components.total_section_flowrate(species_present)
# print(f'Total flowrate for species {species_present}: {total_flowrate}')
# print(components.get_single_flowrate('C'))
# print(components.get_chemical_name('D'))