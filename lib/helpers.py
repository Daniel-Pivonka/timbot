import numpy as np
import json

def utc_to_est(utc_time):
	return str((int(utc_time[:2]) - 5) % 24) + ':' + utc_time[-2:]

def choose_lunchcation():
	places = ['pauls', 'asian plus', 'moes', 'the 99', 'chilis']
	weights = [0.5, 0.3, 0.1, 0.05, 0.05]
	choice = np.random.choice(places, p=weights)
	return choice
