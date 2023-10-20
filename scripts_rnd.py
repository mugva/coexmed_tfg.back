import pandas as pd
import numpy as np
import scipy.io as sio


# import glob # per llegir tots els arxius d'un directori
# import datetime as dt
# import matplotlib.pyplot as plt
# import seaborn as sns # par anàlisi estadístic
# import tqdm


# funcions ___________________________________________________________________________________________________________

def reforma(data, keys=None):
    """
    Reforma els arrays de les variables de data per tal que tinguin una única dimensió
    :param data: dict amb les variables a reformar
    :param keys: keys del dict data que es volen reformar (si no s'indica, es reformen totes)
    :return: dict amb les variables reformades
    """
    keys = data.keys() if keys is None else keys

    for key in keys:
        data[key] = np.reshape(data[key], -1)  # -1 indica que es calculi automàticament la dimensió
        del key
    return data


# flags ______________________________________________________________________________________________________________
Crea_csv_coords = False

# main _______________________________________________________________________________________________________________

# creació de csv amb les coordenades dels punts de malla
if Crea_csv_coords:
    path = r"E:\tfg\Data_CoExMed_Balears\1950.mat"

    coords = sio.loadmat(path, variable_names=('lat', 'lon'))
    coords = reforma(coords, keys=('lat', 'lon'))
    # guardam únicament les coordenades
    coords = pd.DataFrame({key: coords[key] for key in coords.keys() if key in ['lat', 'lon']})

    # guardam dict en un csv
    coords.to_csv(r'E:\tfg\coordsmal.csv', index=False)
    del path
