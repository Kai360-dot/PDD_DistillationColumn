import numpy as np
from column import Column
from AllColumns import ColumnManager

Cost_parameters_1bar = {
    # FIC: Fixed investment cost. [1000 $ / yr]
    # VIC: Variable investment cost. [1000 $ h / (yr kmol) ]
    "k1": {"FIC": 64.37, "VIC": 0.13},
    "k2": {"FIC": 98.44, "VIC": 0.12},
    "k3": {"FIC": 123.92, "VIC": 0.13},
    "k4": {"FIC": 63.44, "VIC": 0.16},
    "k5": {"FIC": 96.80, "VIC": 0.15},
    "k6": {"FIC": 100.31, "VIC": 0.13},
    "k7": {"FIC": 124.27, "VIC": 0.14},
    "k8": {"FIC": 59.25, "VIC": 0.30},
    "k9": {"FIC": 98.23, "VIC": 0.16},
    "k10": {"FIC": 116.63, "VIC": 0.19},
}

Cost_parameters_5bar = {
    # FIC: Fixed investment cost. [1000 $ / yr]
    # VIC: Variable investment cost. [1000 $ h / (yr kmol) ]
    "k1": {"FIC": 99.81, "VIC": 0.11},
    "k2": {"FIC": 156.08, "VIC": 0.12},
    "k3": {"FIC": 190.10, "VIC": 0.15},
    "k4": {"FIC": 97.66, "VIC": 0.13},
    "k5": {"FIC": 154.29, "VIC": 0.15},
    "k6": {"FIC": 158.02, "VIC": 0.14},
    "k7": {"FIC": 189.85, "VIC": 0.17},
    "k8": {"FIC": 89.78, "VIC": 0.26},
    "k9": {"FIC": 155.51, "VIC": 0.17},
    "k10": {"FIC": 179.21, "VIC": 0.23},
}


# Initialize all columns 
column_manager = ColumnManager()
column_manager.add_column('k1', ['A'], ['B', 'C', 'D'])
column_manager.add_column('k2', ['A', 'B'], ['C', 'D'])
column_manager.add_column('k3', ['A', 'B', 'C'], ['D'])
column_manager.add_column('k4', ['A'], ['B', 'C'])
column_manager.add_column('k5', ['A', 'B'], ['C'])
column_manager.add_column('k6', ['B'], ['C', 'D'])
column_manager.add_column('k7', ['B', 'C'], ['D'])
column_manager.add_column('k8', ['A'], ['B'])
column_manager.add_column('k9', ['B'], ['C'])
column_manager.add_column('k10', ['C'], ['D'])


class HeatIntegration:
    """Class for all calculations around the heat integration."""
    def __init__(self, pressure) -> None:
        """Enter pressure in bar."""
        self.gamma = 0.2
        self.delta_T = 10 # minimum exchange Temp. in K
        self.T_W = 298 # Temp. of cooling water in K
        self.pressure = pressure
        if self.pressure == 1:
            self.cost_params = Cost_parameters_1bar
        elif self.pressure == 5:
            self.cost_params = Cost_parameters_5bar
        else:
            print(f'Cost Data at pressure: {self.pressure} bar not available!')
        self.cc_k = self._get_cc_k()
    
    def _get_cc_k(self):
        cc_k = {}
        for column_name, column_obj in column_manager.columns.items():
            FC = self.cost_params[column_name]['FIC']
            gamma = self.gamma
            tau_C = column_obj.Temperature_top
            T_W = self.T_W
            Delta_T_min = self.delta_T
            cc_k[column_name] = FC * (1 + gamma*(tau_C - T_W - Delta_T_min) / (T_W + Delta_T_min))
        return cc_k
    
    def print_cc_k(self):
        for column in column_manager.columns:
            print(f'cc({column}) = {self.cc_k[column]}')


print('-----------------------------------')
print('1 BAR:')
heat_integration_1_bar = HeatIntegration(1)
heat_integration_1_bar.print_cc_k()
print('-----------------------------------')
print('-----------------------------------')
print('5 BAR:')
heat_integration_5_bar = HeatIntegration(5)
heat_integration_5_bar.print_cc_k()
print('-----------------------------------')