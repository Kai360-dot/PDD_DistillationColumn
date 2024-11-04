"""Note to the user: Alter the flow rates and the params. in all *three* locations below. """
# !Initialize below!
components_data = {
    'A': {'compound_name': 'Pentane', 'flowrate': 12},
    'B': {'compound_name': 'Hexane', 'flowrate': 36},
    'C': {'compound_name': 'Heptane', 'flowrate': 48},
    'D': {'compound_name': 'Octane', 'flowrate': 24}
}

Antoine_parameters = {
    'Pentane' : {'A': 67.2281, 'B': -5420.3 , 'C': 0  , 'D': 0 ,  'E':-8.8253  , 'F':9.6171e-6  , 'G': 2, 'T_lo': 143, 'T_up': 470 }, 
    'Hexane' : {'A':93.1371 , 'B':-6995.5 , 'C': 0, 'D': 0,  'E':-12.702 , 'F': 1.2381e-05, 'G': 2, 'T_lo':178, 'T_up':508}, 
    'Heptane' : {'A': 76.3161, 'B': -6996.4, 'C': 0, 'D': 0,  'E': -9.8802, 'F':7.2099e-06 , 'G':2 , 'T_lo': 183, 'T_up':540 }, 
    'Octane' : {'A': 84.5711, 'B':-7900.2 , 'C': 0, 'D': 0,  'E': -11.003, 'F': 7.1802e-06, 'G': 2, 'T_lo': 216, 'T_up':569}, 
}

Heat_vap_parameters = {
    'Pentane': {'A': 37.01, 'B': 0.4121, 'C': -0.1238, 'Tc': 469.6, 'T_lo': 269, 'T_up': 341},
    'Hexane': {'A': 43.85, 'B': 0.3970, 'C': -0.0390, 'Tc': 507.4, 'T_lo': 286, 'T_up': 343},
    'Heptane': {'A': 53.66, 'B': 0.2831, 'C': 0.2831, 'Tc': 540.2, 'T_lo': 299, 'T_up': 372},
    'Octane': {'A': 58.46, 'B': 0.3324, 'C': 0.1834, 'Tc': 568.8, 'T_lo': 326, 'T_up': 400},
}
