# column pressure finder 
from physical_properties import PhysicalProperties
from component_settings import Components
from column import Column
import nist_data # This imports the NIST parameters

components = Components(nist_data.components_data, nist_data.Antoine_parameters, nist_data.Heat_vap_parameters)
phys_props = PhysicalProperties(nist_data.Antoine_parameters, nist_data.Heat_vap_parameters)


# -----------1 bar ------------------
# activatedColumns = {
#     'column_k2' : {'col_obj': Column(['A', 'B'], ['C', 'D']), 'tau_C': 350.65, 'tau_R': 398.98},
#     'column_k8' : {'col_obj': Column(['A'], ['B']), 'tau_C': 308.00, 'tau_R': 340.65},
#     'column_k10' : {'col_obj': Column(['C'], ['D']), 'tau_C': 408.98, 'tau_R': 436.24}
# }

# for column_name, column_val in activatedColumns.items():
#     vapor_pressure_top = phys_props.get_sum_vapor_pressures(column_val['col_obj'].components_top, column_val['tau_C'])
#     vapor_pressure_bottom = phys_props.get_sum_vapor_pressures(column_val['col_obj'].components_bottom, column_val['tau_R'])
#     print(f'Column {column_name} Top Pressure: {vapor_pressure_top:.2f} bar; Bottom Pressure: {vapor_pressure_bottom:.2f} bar')


# ----------5 bar ------------------
activatedColumns = {
    'column_k2' : {'col_obj': Column(['A', 'B'], ['C', 'D']), 'tau_C':  308.00, 'tau_R': 362.24},
    'column_k8' : {'col_obj': Column(['A'], ['B']), 'tau_C': 413.26, 'tau_R': 451.34},
    'column_k10' : {'col_obj': Column(['C'], ['D']), 'tau_C': 372.24, 'tau_R': 403.26}
}

for column_name, column_val in activatedColumns.items():
    vapor_pressure_top = phys_props.get_sum_vapor_pressures(column_val['col_obj'].components_top, column_val['tau_C'])
    vapor_pressure_bottom = phys_props.get_sum_vapor_pressures(column_val['col_obj'].components_bottom, column_val['tau_R'])
    print(f'Column {column_name} Top Pressure: {vapor_pressure_top:.2f} bar; Bottom Pressure: {vapor_pressure_bottom:.2f} bar')
# ----------5 bar ------------------

