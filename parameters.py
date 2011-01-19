params = {
	# Diode calibration parameters
	'a': -2.74893,     # intercept [mW]
	'b': 1.54921,      # slope [W/V]

	# Beam parameters
	# Waist sizes along x and y planes respectively [m]
	'w_x': 105.98e-6,
	'w_y': 101.02e-6,
	# Position of the sample relative to the waist (x and y planes) [m]
	'z_x': 11.8e-3,    
	'z_y': 8.34e-3,
	# Raleigh lenghts along x and y planes [m]
	'zR_x': 38.31e-3,
	'zR_y': 18.46e-3,
	# Angle of incidence [deg]
	'theta': 2.5,
	# Repetition rate [Hz]
	'f_rep': 500,
}

# The respective standart deviations
uncerts = {
	'da': 3.29513,
	'db': 0.02334,
	'dw_x': 0.48e-6,
	'dw_y': 0.31e-6,
	'dz_x': 1.14e-3,
	'dz_y': 0.29e-3,
	'dzR_x': 1.47e-3,
	'dzR_y': 0.47e-3,
	'dtheta': 1.5,
	'df_rep': 0,
}

