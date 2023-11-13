import pickle
import matplotlib.pyplot as plt

flag = True
if flag:
    # ara llegim sa variable percentils
    with open(r"D:\tfg\percentils.pkl", 'rb') as f:
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
    del fig, ax
