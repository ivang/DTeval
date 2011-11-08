params = {
	# Diode calibration parameters
	'a': -2.87226,     # intercept [mW]
	'b':  1.38603,     # slope [mW/mV]

	# Mean waist size [m]
	'w': 50e-6,
	# Angle of incidence [deg]
	'theta': 1.5,
	# Repetition rate [Hz]
	'f_rep': 500,
}

# The respective standart deviations
uncerts = {
	'da': 0.19793,
	'db': 0.01174,
	'dw': 2.95e-6,
	'dtheta': 0.5,
	'df_rep': 0,
}

