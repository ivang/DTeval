params = {
	# Diode calibration parameters
	'a': -2.87226,     # intercept [mW]
	'b':  1.38603,     # slope [mW/mV]

	# Beam parameters
	# Waist sizes along x and y planes respectively [m]
	'w_x': 132.34e-6,
	'w_y': 148.31e-6,
	# Position of the sample relative to the waist (x and y planes) [m]
	'z_x': 19.9e-3,    
	'z_y': 14.5e-3,
	# Raleigh lenghts along x and y planes [m]
	'zR_x': 20.60e-3,
	'zR_y': 19.72e-3,
	# Angle of incidence [deg]
	'theta': 1.5,
	# Repetition rate [Hz]
	'f_rep': 500,
}

# The respective standart deviations
uncerts = {
	'da': 0.19793,
	'db': 0.01174,
	'dw_x': 2.95e-6,
	'dw_y': 0.64e-6,
	'dz_x': 1.20e-3,
	'dz_y': 0.40e-3,
	'dzR_x': 0.32e-3,
	'dzR_y': 0.28e-3,
	'dtheta': 0.5,
	'df_rep': 0,
}

