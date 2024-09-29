import numpy as np
import os

cwd = os.getcwd()

def planets_list():
    planets_list = np.load(cwd +'/assets/exoplanets_array.npy')
    print(planets_list)
    return {"planets_list":list(planets_list)}, 200