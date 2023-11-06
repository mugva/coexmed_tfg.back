import pandas as pd
import numpy as np
import scipy.io as sio
from tqdm import tqdm
import pickle
import matplotlib.pyplot as plt

# import h5py
# import glob # per llegir tots els arxius d'un directori
# import datetime as dt
# import seaborn as sns # par anàlisi estadístic
# from icecream import ic # per fer debug


# funcions ___________________________________________________________________________________________________________

def reforma(data, keys=None):
    """
    Reforma els arrays de les variables de data per tal que tinguin una única dimensió
    :param data: dict amb les variables a reformar
    :param keys: keys del dict data que es volen reformar (si no s'indica, es reformen totes. Must be iterable)
    :return: dict amb les variables reformades
    """
    if keys is None:
        keys = data.keys()

    for key in keys:
        data[key] = np.reshape(data[key], -1)  # -1 indica que es calculi automàticament la dimensió
    del keys, key
    return data


# flags ______________________________________________________________________________________________________________
Crea_csv_coords = False  # creació de csv amb les coordenades dels punts de malla
Lector_costa = False  # lectura de la costa de les Balears
Lector_batimetria = False  # lectura de la batimetria de les Balears
Percentils_temp = False  # càlcul dels percentils 95 i 99 de l'altura significativa


# main _______________________________________________________________________________________________________________
if Crea_csv_coords:
    path = r"E:\tfg\Data_CoExMed_Balears\1950.mat"

    coords = sio.loadmat(path, variable_names=('lat', 'lon'))
    coords = reforma(data=coords, keys=('lat', 'lon'))
    # guardam únicament les coordenades
    coords = pd.DataFrame({key: coords[key] for key in coords.keys() if key in ['lat', 'lon']})

    # guardam dict en un csv
    res = input('Vols guardar les coordenades en un csv? (s/[n])')
    if res in ('s', 'S'):
        coords.to_csv(r'E:\tfg\coords.csv', index=True, index_label='index')
    del path

    # ara cercam ses coordenades des nostros punts d'interés
    punts = [353, 764, 912, 1021, 1291, 1319, 1339, 1366]
    coords_punts_int = coords.iloc[punts, :]
    res = input('Vols guardar les coordenades dels punts d\'interés en un csv? (s/[n])')
    if res in ('s', 'S'):
        coords_punts_int.to_csv(r'E:\tfg\coords_punts_int.csv', index=True, index_label='index')
    del coords, punts

elif Lector_costa:  # no funciona
    # llegim arxiu matlab v7.3
    import h5py
    path = r"E:\tfg\Costas_Islas_Baleares.mat"
    f = h5py.File(path, 'r')
    # guardam les variables en un dict
    costa = {}
    for key in f.keys():
        costa[key] = f[key][:]


elif Lector_batimetria:  # no funciona
    # llegiu arxiu en format csv
    path = r"E:\tfg\Mean depth in multi colour (no land)\Mean depth in multi colour (no land).csv"
    batimetria = pd.read_csv(path, sep=',', header=0, index_col=0, encoding='charmap')


elif Percentils_temp:
    # calculam es percentils 95 i 99 de cada any de l'altura significativa
    # per fer-ho recorrem cada arxiu del 1950 fins 2020
    percentils = {}
    # empleam sa llibraria tqdm per fer una barra de progrés
    for year in tqdm(range(1950, 2023), desc='Càlcul percentils per any'):
        path = r"E:\tfg\Data_CoExMed_Balears\{}.mat".format(year)
        var_names = ('elev_hydro', 'elev_wavedpt', 'Hs_wavedpt', 'Tp_wavedpt', 'Dp_wavedpt')
        data_raw = sio.loadmat(path, variable_names=var_names)
        # cream diccionari de dataframes
        df = {}
        for key in var_names:
            df[key] = pd.DataFrame(data=data_raw[key])
        # mos quedam només amb les columnes (punts espaials) d'interés
        punts = [353, 764, 912, 1021, 1291, 1319, 1339, 1366]
        df_punts = {}
        for key in df.keys():
            df_punts[key] = df[key].iloc[:, punts]
        # calculam els percentils
        percentils_i = {}
        for key in df_punts.keys():
            percentils_i[key] = df_punts[key].quantile(q=[0.95, 0.99], axis=0)
        # guardam dins un dict
        percentils[year] = percentils_i
        del year, key, path, var_names, data_raw, df, punts, df_punts, percentils_i

    # guardam sa variable percentils en format .py
    res = input('Vols guardar els percentils en un fitxer .pkl? (s/[n])')
    if res in ('s', 'S'):
        with open(r"E:\tfg\percentils.pkl", 'wb') as f:
            pickle.dump(percentils, f)
    del f


# main end ___________________________________________________________________________________________________________
flag = False
if flag:
    # ara llegim sa variable percentils
    with open(r"E:\tfg\percentils.pkl", 'rb') as f:
        percentils = pickle.load(f)
    del f

    # reformatejam el diccionari percentils perquè les keys siguin els punts de malla
    percentils_reformat = {}
    for punt in [353, 764, 912, 1021, 1291, 1319, 1339, 1366]:
        percentils_reformat[punt] = {}
        for year in percentils.keys():
            percentils_reformat[punt][year] = percentils[year]['Hs_wavedpt'][punt]
    del punt, year

    # representam en un gràfic els percentils de cada punt de malla
    # volem fixar l'altura vertical a valors vixes compresos entre els 1 i 5 metres
    fig, ax = plt.subplots(2, 4, figsize=(10, 5))
    for i, punt in enumerate(percentils_reformat.keys()):
        ax[i // 4, i % 4].plot(percentils_reformat[punt].keys(), percentils_reformat[punt].values())
        ax[i // 4, i % 4].set_title('Punt {}'.format(punt))
        ax[i // 4, i % 4].set_xlabel('Any')
        ax[i // 4, i % 4].set_ylabel('Hs (m)')
        ax[i // 4, i % 4].grid()
        ax[i // 4, i % 4].set_ylim(1, 5.5)
    del i, punt
    plt.tight_layout()
    plt.show()

flag = False
if flag:
    # llegim arxiu i representam punts d'interés
    coords_punts_int = pd.read_csv(r'E:\tfg\coords_punts_int.csv', sep=',', header=0, index_col=0)
    # plot
    fig, ax = plt.subplots(figsize=(6, 6))
    for idx in coords_punts_int.index:
        ax.scatter(coords_punts_int.loc[idx, 'lon'], coords_punts_int.loc[idx, 'lat'], s=10, label=idx)
        # escrivim l'idx del punt devora sa seva posició
        ax.text(coords_punts_int.loc[idx, 'lon'], coords_punts_int.loc[idx, 'lat'], idx, fontsize=10)
    del idx
    ax.legend()
    ax.set_xlabel('Longitud')
    ax.set_ylabel('Latitud')
    ax.set_title('Punts d\'interés')
    plt.show()
    del fig, ax
